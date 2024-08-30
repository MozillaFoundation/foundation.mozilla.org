/**
 * Bind click handler to
 * ".profile-directory .fellowships-directory-filter .filter-option button"
 * (filter buttons on fellowships' Pulse directory)
 */

export default () => {
  document
    .querySelectorAll(
      `.profile-directory .fellowships-directory-filter .filter-option button`
    )
    .forEach((filter) => {
      let year = filter.textContent.trim();
      filter.addEventListener(`click`, () => {
        window.dataLayer.push({
          event: `profiles_directory_filter`,
          category: `profiles`,
          action: `directory filter`,
          label: `${document.title} ${year}`,
        });
      });
    });
};
