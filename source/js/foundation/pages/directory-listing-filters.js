(function () {
  // start of function

  const profileCache = {};
  const labels = document.querySelectorAll(
    `[data-profile-type-filters] button`
  );
  const profileContainer = document.querySelector(`.profiles .row`);
  const { programYear, programType } =
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
  function getData(profileType) {
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
  function loadResults(type, bypassState) {
    const profiles = profileCache[type];

    if (!bypassState) {
      history.pushState({ type: type }, document.title);
    }
    let cards = profiles.map((profile) => {
      return `
        <div class="tw-grid tw-grid-cols-4 tw-grid-rows-3 large:tw-grid-cols-5 tw-gap-x-3 tw-gap-y-2 tw-border-t tw-border-black">

        <!-- Image -->
        <a href="https://www.mozillapulse.org/profile/${profile.profile_id}"
           class="tw-block tw-row-span-1 large:tw-row-span-4 tw-col-span-1 tw-relative tw-min-h-[160px] tw-h-[100%] tw-w-full tw-overflow-hidden">
          <img src="${
            profile.thumbnail
              ? profile.thumbnail
              : `/_images/fellowships/headshot/placeholder.jpg`
          }"
               class="tw-w-auto tw-h-full tw-absolute tw-left-50 tw-top-50 tw-min-w-full tw-object-cover"
               alt="Headshot">
        </a>

        <!-- Right card -->
        <div class="tw-row-span-1 large:tw-row-span-1 tw-col-span-3 large:tw-col-span-4">

          <!--Card top -->
          <div class="tw-flex tw-flex-row tw-justify-between tw-items-center tw-mt-2">
            <a class="h5-heading tw-mb-1 tw-font-sans tw-font-normal" href="https://www.mozillapulse.org/profile/${
              profile.profile_id
            }">${profile.name}</a>

            <!-- Social Icons -->
            <div class="tw-flex tw-flex-row tw-space-x-2">
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

        <!-- Profile Location -->
          ${
            profile.location &&
            `<p class="tw-flex-row tw-flex tw-items-center tw-justify-start">
              <img class="tw-w-[12px] tw-h-[12px] tw-block tw-mr-1" src="{% static '_images/glyphs/map-marker-icon.svg' %}" alt="">
              ${profile.location}
            </p>`
          }
         </div>

        <!-- Short bio block -->
        <div class="large:tw-row-span-2 tw-col-span-4 large:tw-col-start-2 large:tw-col-span-4">
          <p class="tw-text-gray-60">${profile.user_bio}</p>

          <!-- Issues -->
            ${
              profile.issues &&
              `<div class="issues-list tw-flex tw-flex-wrap tw-mt-auto">
                     ${profile.issues
                       .map(
                         (issue) =>
                           `<span class="tw-text-blue tw-text-sm tw-font-bold first:tw-ml-0 tw-ml-2">${issue}</span>`
                       )
                       .join("")}
              </div>`
            }
        </div>
      </div>`;
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

  function loadForType(type, bypassState) {
    // if we have a cache, use it, but if we don't:
    if (!profileCache[type]) {
      // initiate an API call to fetch all data
      // associated with a particular year:
      showLoadSpinner();
      getData(type)
        .then((data) => {
          // catch that data, and then load the results.
          console.log(data);
          profileCache[type] = preprocessProfiles(data);
          loadResults(type, bypassState);
        })
        .catch((error) => {
          // TODO: what do we want to do in this case?
          console.error(error);
        });
    } else {
      // if we already had the data cached, load immediately:
      loadResults(type, bypassState);
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
        let type = label.textContent;
        selectLabel(label);
        loadForType(type);
      });
    });
  }

  // make sure that "back" does the right thing.
  window.addEventListener("popstate", (evt) => {
    const state = evt.state || { type: labels[0].textContent };
    const type = state.type;
    const label = Array.from(labels).find((l) => l.textContent == type);
    selectLabel(label);
    loadForType(type, true);
  });

  // and finally, kick everything off by
  // invoking the filter binding function
  bindEventsToLabels();

  // end of function
})();
