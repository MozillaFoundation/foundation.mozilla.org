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
    const typeformLink = document.getElementById("btn-typeform-popup");

    if (!typeformLink) {
      return;
    }

    if (!window.typeformEmbed) {
      return;
    }

    // turn this into a button instead of a link if JS is all good.
    const typeformButton = document.createElement(`button`);
    typeformButton.setAttribute(`class`, typeformLink.getAttribute(`class`));
    typeformButton.textContent = typeformLink.textContent;
    typeformLink.parentNode.replaceChild(typeformButton, typeformLink);

    const popup = window.typeformEmbed.makePopup(typeformLink.href, {
      mode: "popup",
      hideHeaders: true,
      hideFooter: true,
      autoOpen: false,
    });

    const open = () => popup.open();
    ["touchstart", "click"].forEach((evtType) =>
      typeformButton.addEventListener(evtType, open)
    );
  },
};

export default EmbedTypeform;
