/**
 * Bind click handler to #donate-footer-btn
 * ("Donate" button on footer)
 */
export default () => {
  let donateFooterBtn = document.getElementById("donate-footer-btn");

  if (donateFooterBtn) {
    donateFooterBtn.addEventListener("click", () => {
      window.dataLayer.push({
        event: "donate_button_click",
        category: "donate",
        action: "donate button tap",
        label: `${document.title} footer`,
      });
    });
  }
};
