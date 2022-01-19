import copyToClipboard from "../../copy-to-clipboard.js";

(function () {
  "use strict";

  const cta = document.querySelector(`.callpower-cta`);
  if (!cta) return;

  // Callpower response codes
  const BAD_ARGUMENTS = 400;
  const RATE_LIMIT_ERROR = 429;

  // Form field coloring
  const INVALID_FORM_FIELD = `tw-border-red-dark`;
  const VALID_FORM_BORDER = `tw-border-gray-20`;

  // all the elements we'll need to work with.
  const get = cta.querySelector.bind(cta);
  const elements = {
    campaignId: get(`input[name="campaignId"]`),
    userPhoneInput: get(`input[name="userPhone"]`),
    userZipCode: get(`input[name="userZipCode"]`),
    mainForm: get(`.cta-form`),
    success: get(`.success`),
    unknownError: get(`.unknown.error-section`),
    limitError: get(`.limit.error-section`),
    callButton: get(`.make-the-call`),
    badWarning: get(`.error-400`),
  };

  /**
   * Either toggle or explicitly reveal an element on the page
   * @param {*} element
   * @param {*} hide
   */
  function toggleVisible(element, hide) {
    const fname = hide === true ? `add` : `toggle`;
    element.classList[fname](`tw-hidden`);
  }

  /**
   * Validate a form element and flag it as "bad" if it does
   * not pass validation.
   * @param {*} element
   */
  function validate(element) {
    toggleWarning(element, false);
    const regexp = new RegExp(element.dataset.pattern);
    const value = element.value.trim();
    const matches = value.match(regexp);
    if (!matches) toggleWarning(element, true);
  }

  /**
   * Mark a field as invalid and reveal its error guide text.
   * @param {*} element
   * @param {*} active
   */
  function toggleWarning(element, active) {
    element.classList[active ? `add` : `remove`](INVALID_FORM_FIELD);
    element.classList[active ? `remove` : `add`](VALID_FORM_BORDER);
    let next = element;
    do {
      next = next.nextSibling;
    } while (next && next.nodeType !== Node.ELEMENT_NODE);
    next.classList[active ? `remove` : `add`](`tw-hidden`);
  }

  /**
   * Perform a callpower POST.
   */
  function makeTheCall() {
    fetch(`https://mozilla.callpower.org/call/create`, {
      method: `POST`,
      body: buildFormData(),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) throw new Error(JSON.stringify(data));
        showSuccess();
      })
      .catch(processError);
  }

  /**
   * Create a POST form payload
   */
  function buildFormData() {
    const { campaignId, userPhoneInput, userZipCode } = elements;
    const form = new FormData();
    form.append("campaignId", campaignId.value);
    form.append("userPhone", userPhoneInput.value);
    form.append("userLocation", userZipCode.value);
    return form;
  }

  /**
   * When everything went right, swap the CTA content
   * over to the success content.
   */
  function showSuccess() {
    const { mainForm, success } = elements;
    toggleVisible(mainForm);
    toggleVisible(success);
  }

  /**
   *
   */
  function shareButtonClicked(event, shareProgressButtonId) {
    if (globalThis.ga && typeof globalThis.ga === `function`) {
      globalThis.ga("send", {
        hitType: "event",
        category: `petition`,
        action: `share tap`,
        label: `${document.title} - share tap`,
      });
    }

    if (shareProgressButtonId) {
      let shareProgressButton = document.querySelector(
        `#${shareProgressButtonId} a`
      );

      if (shareProgressButton) {
        shareProgressButton.click();
      }
    } else {
      copyToClipboard(event.target, window.location.href);
    }
  }

  /**
   * When an error occurs during callpower POSTing,
   * figure out what to present the user based on
   * the type of error.
   * @param {*} err
   * @param {num} status, defaults to 500
   */
  function processError(_err, status = 500) {
    try {
      // is this our error, packed as JSON string?
      const data = JSON.parse(_err.message);
      status = parseInt(data.status);
    } catch (e) {
      // No, this was a "real" Fetch error.
    }
    showError(status);
  }

  /**
   * Part 2 of processError(), which swaps out the CTA
   * content as needed, based on the status code passed.
   */
  function showError(status) {
    const { mainForm, unknownError, badWarning, limitError } = elements;
    let element = unknownError;
    if (status === BAD_ARGUMENTS) {
      element = badWarning;
    } else if (status === RATE_LIMIT_ERROR) {
      element = limitError;
    }
    if (status !== BAD_ARGUMENTS) {
      toggleVisible(mainForm);
    }
    toggleVisible(element);
  }

  return {
    /**
     * Bootstrap the user interaction for our Callpower CTA
     */
    init: () => {
      const { userPhoneInput, userZipCode, mainForm, badWarning, callButton } =
        elements;

      // I really wish that the `pattern` attribute worked properly, but it doesn't.
      [userPhoneInput, userZipCode].forEach((e) => {
        e.addEventListener(`input`, () => {
          toggleVisible(badWarning, true);
          validate(e);
        });
      });

      // intercept the form submit, so we can run process the POST without a page navigation.
      mainForm.addEventListener(`submit`, (evt) => {
        evt.preventDefault();

        let form_is_valid = true;
        [userPhoneInput, userZipCode].forEach((element) => {
          validate(element);
          if (element.classList.contains(INVALID_FORM_FIELD)) {
            form_is_valid = false;
          }
        });
        if (form_is_valid) makeTheCall();
      });

      callButton.removeAttribute(`disabled`);

      // also make sure the social share buttons work on success
      document
        .querySelectorAll(`.share-button-group .btn`)
        .forEach((element) => {
          const { target } = element.dataset;
          element.addEventListener(`click`, (evt) =>
            shareButtonClicked(evt, target)
          );
        });
    },
  };
})().init();
