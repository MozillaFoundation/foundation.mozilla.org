/**
 * Adding a UTM string to the download/share buttons on the youtube regrets extension landing page.
 * 
 * If there are UTM parameters in the URL bar, which means they got directed to the page through a
 * marketing effort, we append those to the link buttons so the params get carried over to the download page.
 * If there are none, we are appending a default UTM param to the button links.
 */

class regretsReporterUtmButtons {
  constructor() {
    this.checkForUtmParams();
  }

  checkForUtmParams() {
    // Default UTM Parameters, if none are set.
    let utmParams =
      "?utm_medium=website&utm_source=landing_page&utm_campaign=youtuberr2021";

    // If there are UTM parameters in URL, update string.
    if (window.location.search) {
      utmParams = window.location.search;
    }

    this.updateButtonURLs(utmParams);
  }

  updateButtonURLs(params) {
    const downloadExtensionButtons = document.querySelectorAll(
      `.download-link-button--firefox, .download-link-button--chrome`
    );
    const emailReminderButton = document.querySelector(
      `.download-link-button--email`
    );

    downloadExtensionButtons.forEach(function (downloadBtn) {
      downloadBtn.href += params;
    });

    // Encoding UTM params for mailto: links
    const newParams = encodeURIComponent(params);

    const updatedEmailBtnUrls =
      emailReminderButton.href +
      `%0D%0A%0D%0Ahttps://addons.mozilla.org/en-us/firefox/addon/regretsreporter/${newParams}%0D%0Ahttps://chrome.google.com/webstore/detail/regretsreporter/obpoeflheeknapimliioeoefbfaakefn${newParams}`;

    emailReminderButton.href = updatedEmailBtnUrls;
  }
}

export default regretsReporterUtmButtons;
