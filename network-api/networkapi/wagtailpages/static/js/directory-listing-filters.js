(function() {
  // start of function

  const profileCache = {};
  const labels = document.querySelectorAll(
    `.profile-directory .fellowships-directory-filter .filter-option button`
  );
  const profileContainer = document.querySelector(`.profiles .row`);
  const { profileType, programType } = document.querySelector(
    `.profiles`
  ).dataset;
  const API_ENDPOINT = document.querySelector(`[data-api-endpoint]`).dataset
    .apiEndpoint;

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
      programYear ? `program_year=${programYear}` : false
    ]
      .filter(v => v)
      .join("&");

    // and then perform our API call using the Fetch API
    return new Promise((resolve, reject) => {
      return (
        fetch(`${url}&${query}`)
          // conver the resonse from JSON to real data
          .then(response => response.json())
          // all went well? resolve.
          .then(obj => resolve(obj))
          // errors? reject.
          .catch(error => reject(error))
      );
    });
  }

  /**
   * Load an array of profiles into the profile car container.
   * We first map the profiles array, turning profile objects
   * into templated HTML using the same HTML as we have in
   * profile_blocks.html
   */
  function loadResults(year, bypassState) {
    const profiles = profileCache[year];

    if (!bypassState) {
      history.pushState({ year: year }, document.title);
    }

    let cards = profiles.map(profile => {
      return `
      <div class="col-lg-6 col-12 mb-5">
        <div class="person-card">
          <div class="thumbnail-wrapper">
            <a href="https://www.mozillapulse.org/profile/${
              profile.profile_id
            }" class="d-block headshot-container">
              <img
                src="${
                  profile.thumbnail
                    ? profile.thumbnail
                    : `/_images/fellowships/headshot/placeholder.jpg`
                }"
                class="headshot"
                alt="Headshot">
            </a>
          </div>

          <div class="short-meta-wrapper">
            <a class="h5-heading meta-block-name mb-0 d-block"
                href="https://www.mozillapulse.org/profile/${
                  profile.profile_id
                }">
                  ${profile.name}
            </a>
            ${profile.location &&
              `<p class="d-flex align-items-center meta-block-location body-small my-2">${profile.location}</p>`}
            <div class="social-icons">
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

          <div class="bio-wrapper">
            <p class="m-0">${profile.user_bio}</p>
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
      </div>`;
  }

  function loadForYear(year, bypassState) {
    // if we have a cache, use it, but if we don't:
    if (!profileCache[year]) {
      // initiate an API call to fetch all data
      // associated with a particular year:
      showLoadSpinner();
      getData(year)
        .then(data => {
          // catch that data, and then load the results.
          profileCache[year] = data;
          loadResults(year, bypassState);
        })
        .catch(error => {
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
    labels.forEach(label => label.classList.remove("active"));
    label.classList.add("active");
    label.focus();
  }

  /**
   * This function grabs all buttons, and adds click
   * event handling, to load up all profiles for the
   * associated year (for now)
   */
  function bindEventsToLabels() {
    labels.forEach(label => {
      label.addEventListener("click", evt => {
        let year = label.textContent;
        selectLabel(label);
        loadForYear(year);
      });
    });
  }

  // make sure that "back" does the right thing.
  window.addEventListener("popstate", evt => {
    const state = evt.state || { year: labels[0].textContent };
    const year = state.year;
    const label = Array.from(labels).find(l => l.textContent == year);
    selectLabel(label);
    loadForYear(year, true);
  });

  // and finally, kick everything off by
  // invoking the filter binding function
  bindEventsToLabels();

  // end of function
})();
