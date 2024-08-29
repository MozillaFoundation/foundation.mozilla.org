/**
 * Bind click handler to data-donate-header-button
 * ("Donate" button on primary nav)
 */
export default () => {
  const donateHeaderBtn = document.querySelectorAll(
    "[data-donate-header-button]"
  );
  if (donateHeaderBtn.length > 0) {
    donateHeaderBtn.forEach((element) => {
      element.addEventListener(`click`, () => {
        window.dataLayer.push({
          event: `donate_button_tap_header`,
          category: `donate`,
          action: `donate button tap`,
          label: `${document.title} header`,
        });
      });
    });
  }
};
