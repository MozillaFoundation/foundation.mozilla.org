let EmbedTF = {
  init: function() {
    document.addEventListener("DOMContentLoaded", () => EmbedTF.setup());
  },
  setup: function() {
    let formMeta = document.querySelector("meta[name=typeform-formurl]");

    if (!formMeta) {
      return;
    }

    let popup = window.typeformEmbed.makePopup(
      formMeta.getAttribute("content"),
      {
        mode: "popup",
        hideHeaders: true,
        hideFooter: true
      }
    );

    document
      .querySelector("#btn-typeform-popup")
      .addEventListener("click", () => {
        popup.open();
      });
  }
};

export default EmbedTF;
