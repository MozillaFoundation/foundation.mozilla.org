/**
 * Filtering functionality for the pulse directory component.
 */

(function () {
  // start of function

  const profileCache = {};
  const labels = document.querySelectorAll(
    `.fellowships-directory-filter .filter-option button`
  );
  const profileContainer = document.querySelector(`.profiles .tw-row`);
  const { profileType, programType } =
    document.querySelector(`.profiles`).dataset;
  const API_ENDPOINT =
    document.querySelector(`[data-api-endpoint]`).dataset.apiEndpoint;

  /**
   * We're reasonably sure that profiles are sane already, but
   * let's make sure we're _absolutely_ sure because we're relying
   * on innerHTML for this code to work.
   */
  function preprocessProfiles(profiles) {
    profiles.forEach((profile) => {
      // the id has to be an int
      profile.profile_id = parseInt(profile.profile_id);

      // URL fields should be actual URLs
      [`thumbnail`, `twitter`, `linkedin`].forEach((type) => {
        if (!profile[type]) return;

        let a = document.createElement(`a`);
        a.href = profile[type];

        try {
          let url = new URL(a);
          let protocol = url.protocol;
          if (protocol.indexOf(`http`) !== 0) {
            throw new Error(`non-web link found for profile.${type}`);
          }
          profile[type] = url.toString();
        } catch (e) {
          profile[type] = false;
        }
      });

      let sanitizer = document.createElement(`div`);

      // Freeform fields may not contain HTML
      [`name`, `location`, `user_bio`].forEach((type) => {
        sanitizer.textContent = profile[type];
        profile[type] = sanitizer.innerHTML;
      });
    });

    return profiles;
  }

  /**
   * After initial page load, the filter buttons are responsible for
   * fetching results "per filter entry".
   */
  function getData(programYear) {
    // set up a url for performing an API call:
    let url = API_ENDPOINT;

    // build and append the query arguments
    let query = [
      profileType ? `profile_type=${profileType}` : false,
      programType ? `program_type=${programType}` : false,
      programYear ? `program_year=${programYear}` : false,
    ]
      .filter((v) => v)
      .join("&");

    // and then perform our API call using the Fetch API
    return new Promise((resolve, reject) => {
      return (
        fetch(`${url}&${query}`)
          // conver the resonse from JSON to real data
          .then((response) => response.json())
          // all went well? resolve.
          .then((obj) => resolve(obj))
          // errors? reject.
          .catch((error) => reject(error))
      );
    });
  }

  /**
   * Load an array of profiles into the profile car container.
   * We first map the profiles array, turning profile objects
   * into templated HTML. using the same HTML as we have in
   * templates/wagtailepages/blocks/profile_block.html
   */
  function loadResults(year, bypassState) {
    const profiles = profileCache[year];

    if (!bypassState) {
      history.pushState({ year: year }, document.title);
    }

    let cards = profiles.map((profile) => {
      return `
      <div class="tw-px-4 tw-w-full large:tw-w-1/2 tw-mb-6">
        <div class="person-card tw-border-t tw-border-black medium:tw-relative medium:tw-min-h-[160px]">
          <div class="tw-float-left medium:tw-absolute">
            <a href="https://www.mozillapulse.org/profile/${
              profile.profile_id
            }" class="tw-block headshot-container tw-w-[92px] tw-h-[92px] tw-mr-[14px] tw-mb-[14px] medium:tw-w-[160px] medium:tw-h-[160px] medium:tw-mr-[0px] medium:tw-mb-[0px]">
              <img
                src="${
                  profile.thumbnail
                    ? profile.thumbnail
                    : `/_images/fellowships/headshot/placeholder.jpg`
                }"
                class="tw-object-cover tw-w-full tw-h-full tw-object-center"
                alt="Headshot">
            </a>
          </div>

          <div class="short-meta-wrapper tw-pt-[10px] medium:tw-ml-[174px]">
            <a class="h5-heading medium:tw-w-[calc(100%-70px)] tw-mb-0 tw-block"
                href="https://www.mozillapulse.org/profile/${
                  profile.profile_id
                }">
                  ${profile.name}
            </a>
            ${
              profile.location &&
              `<p class="tw-flex tw-items-center meta-block-location body-small tw-my-2">${profile.location}</p>`
            }
            <div class="medium:tw-absolute medium:tw-right-0 medium:tw-top-4">
              ${
                profile.twitter
                  ? `<a href="${profile.twitter}" class="twitter twitter-glyph small"></a>`
                  : ``
              }
              ${
                profile.linkedin
                  ? `<a href="${profile.linkedin}" class="linkedIn linkedIn-glyph small"></a>`
                  : ``
              }
            </div>
          </div>

          <div class="tw-clear-both medium:tw-ml-[174px]">
            <p class="tw-m-0">${profile.user_bio}</p>
          </div>
        </div>
      </div>
      `;
    });

    // And then we update the content that the user sees:
    profileContainer.style.removeProperty(`height`);
    profileContainer.innerHTML = cards.join("\n");
    document.dispatchEvent(new CustomEvent("profiles:list-updated"));
  }

  function showLoadSpinner() {
    profileContainer.style.height = `${profileContainer.offsetHeight}px`;
    profileContainer.innerHTML = `
      <div class="col-12 mx-auto my-5 text-center">
        <div class="loading-indicator d-inline-block">
          <div class="dot"></div>
          <div class="dot"></div>
          <div class="dot"></div>
        </div>
      </div>
    `;
  }

  function loadForYear(year, bypassState) {
    // if we have a cache, use it, but if we don't:
    if (!profileCache[year]) {
      // initiate an API call to fetch all data
      // associated with a particular year:
      showLoadSpinner();
      getData(year)
        .then((data) => {
          // catch that data, and then load the results.
          profileCache[year] = preprocessProfiles(data);
          loadResults(year, bypassState);
        })
        .catch((error) => {
          // TODO: what do we want to do in this case?
          console.error(error);
        });
    } else {
      // if we already had the data cached, load immediately:
      loadResults(year, bypassState);
    }
  }

  /**
   * Set focus and class-mark as active.
   */
  function selectLabel(label) {
    labels.forEach((label) => label.classList.remove("active"));
    label.classList.add("active");
    label.focus();
  }

  /**
   * This function grabs all buttons, and adds click
   * event handling, to load up all profiles for the
   * associated year (for now)
   */
  function bindEventsToLabels() {
    labels.forEach((label) => {
      label.addEventListener("click", (evt) => {
        let year = label.textContent;
        selectLabel(label);
        loadForYear(year);
      });
    });
  }

  // make sure that "back" does the right thing.
  window.addEventListener("popstate", (evt) => {
    const state = evt.state || { year: labels[0].textContent };
    const year = state.year;
    const label = Array.from(labels).find((l) => l.textContent == year);
    selectLabel(label);
    loadForYear(year, true);
  });

  // and finally, kick everything off by
  // invoking the filter binding function
  bindEventsToLabels();

  // end of function
})();
