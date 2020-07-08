const EmbedTypeform = {
  init: function () {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", () =>
        EmbedTypeform.setup()
      );
    } else {
      EmbedTypeform.setup();
    }
  },
  setup: function () {
    const formMeta = document.querySelector("meta[name=typeform-formurl]");

    if (!formMeta) {
      return;
    }

    if (window.typeformEmbed) {
      const popup = window.typeformEmbed.makePopup(
        formMeta.getAttribute("content"),
        {
          mode: "popup",
          hideHeaders: true,
          hideFooter: true,
          autoOpen: false,
        }
      );

      document
        .querySelector("#btn-typeform-popup")
        .addEventListener("click", () => popup.open());
    }
  },
};

export default EmbedTypeform;
