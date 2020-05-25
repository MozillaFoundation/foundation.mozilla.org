let EmbedTF = {
  init: function() {
    document.addEventListener("DOMContentLoaded", () => EmbedTF.setup());
  },
  setup: function() {
    let formMeta = document.querySelector("meta[name=typeform-formurl]");

    if (!formMeta) {
      return;
    }

    let formElement = document.querySelector("div#typeform-embed");

    let popup = window.typeformEmbed.makePopup(
      // formElement,
      formMeta.getAttribute("content"),
      {
        hideFooter: true,
        hideHeaders: true,
        opacity: 0,
        mode: "popup",
        // autoOpen: true
      }
    );

    document.querySelector("#btn-typeform-popup").addEventListener("click", () => {
      popup.open();
    });
  }
};

export default EmbedTF;
