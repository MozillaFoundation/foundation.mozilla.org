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

    window.typeformEmbed.makeWidget(
      formElement,
      formMeta.getAttribute("content"),
      {
        hideFooter: true,
        hideHeader: true,
        opacity: 0
      }
    );
  }
};

export default EmbedTF;
