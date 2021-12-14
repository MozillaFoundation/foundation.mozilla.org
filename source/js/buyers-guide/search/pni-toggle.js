const toggle = document.querySelector(`#product-filter-pni-toggle`);
const categoryTitle = document.querySelector(`.category-title`);

export class PNIToggle {
  constructor(searchFilter) {
    this.searchFilter = searchFilter;

    if (!toggle) {
      return console.warn(
        `Could not find the PNI filter checkbox. PNI filtering will not be available.`
      );
    }

    toggle.addEventListener(`change`, (evt) => this.togglePrivacyOnly(evt));
  }

  togglePrivacyOnly(evt) {
    const filter = evt.target.checked;
    const { searchFilter } = this;

    // TODO: this might be an A/B testing opportunity to see
    //       whether users assume this toggle is a navigation
    //       action or not?
    history.replaceState(
      {
        ...history.state,
        filter,
      },
      searchFilter.getTitle(categoryTitle.value.trim()),
      location.href
    );

    const toggleFunction = filter ? `add` : `remove`;
    document.body.classList[toggleFunction](`show-ding-only`);

    if (searchFilter.searchInput.value.trim()) {
      searchFilter.searchInput.focus();
      searchFilter.checkForEmptyNotice();
    }
  }
}
