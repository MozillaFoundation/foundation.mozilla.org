class BaseLinkBlockDefinition extends window.wagtailStreamField.blocks
  .StructBlockDefinition {
  render(placeholder, prefix, initialState, initialError) {
    const block = super.render(placeholder, prefix, initialState, initialError);

    const linkToField = document.getElementById(prefix + "-link_to");

    // Iterate over choices and hide the fields that are not selected
    const updateStateInput = () => {
      const selectedValue = linkToField.value;
      for (let i = 0; i < linkToField.length; i += 1) {
        const choice = linkToField[i].value;
        if (choice) {
          const field = document.getElementById(prefix + "-" + choice);
          const fieldWrapper = field.closest(`[data-contentpath="${choice}"]`);
          if (choice === selectedValue) {
            field.removeAttribute("disabled");
            fieldWrapper.removeAttribute("hidden");
          } else {
            field.setAttribute("disabled", true);
            fieldWrapper.setAttribute("hidden", true);
          }
        }
      }
    };

    updateStateInput();
    linkToField.addEventListener("change", updateStateInput);

    return block;
  }
}
window.telepath.register(
  "foundation_cms.legacy_apps.wagtailpages.customblocks.BaseLinkBlock",
  BaseLinkBlockDefinition
);
