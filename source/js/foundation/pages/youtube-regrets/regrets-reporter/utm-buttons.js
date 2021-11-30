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

    const updatedEmailBtnUrls =
      emailReminderButton.href +
      `%0D%0A%0D%0Ahttps://addons.mozilla.org/en-us/firefox/addon/regretsreporter/${params}%0D%0Ahttps://chrome.google.com/webstore/detail/regretsreporter/obpoeflheeknapimliioeoefbfaakefn${params}`;

    emailReminderButton.href = updatedEmailBtnUrls;
  }
}

export default regretsReporterUtmButtons;
