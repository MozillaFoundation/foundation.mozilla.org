import { SearchFilter as SearchFilterObject } from "./search/search-filter.js";

const categoryTitle = document.querySelector(`.category-title`);
const toggle = document.querySelector(`#product-filter-pni-toggle`);


// TODO: turn this into a static class rather than plain JS object.
const SearchFilter = new SearchFilterObject();


// TODO: turn this into a static class as well
const PNIToggle = {
  init: () => {
    if (!toggle) {
      return console.warn(
        `Could not find the PNI filter checkbox. PNI filtering will not be available.`
      );
    }

    toggle.addEventListener(`change`, (evt) => {
      const filter = evt.target.checked;

      // TODO: this might be an A/B testing opportunity to see
      //       whether users assume this toggle is a navigation
      //       action or not?
      history.replaceState(
        {
          ...history.state,
          filter,
        },
        SearchFilter.getTitle(categoryTitle.value.trim()),
        location.href
      );

      if (filter) {
        document.body.classList.add(`show-ding-only`);
      } else {
        document.body.classList.remove(`show-ding-only`);
      }

      if (SearchFilter.searchInput.value.trim()) {
        SearchFilter.searchInput.focus();
        SearchFilter.checkForEmptyNotice();
      }
    });
  },
};

// bootstrap both searching and privacy-ding-filtering
PNIToggle.init();
