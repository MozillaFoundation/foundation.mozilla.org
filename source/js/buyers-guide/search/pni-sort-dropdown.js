const SPACEBAR_KEY_CODE = [0, 32];
const ENTER_KEY_CODE = 13;
const DOWN_ARROW_KEY_CODE = 40;
const UP_ARROW_KEY_CODE = 38;
const ESCAPE_KEY_CODE = 27;

/**
 * Dropdown component for sorting products on PNI
 */
export class PNISortDropdown {
  constructor(searchFilter) {
    this.searchFilter = searchFilter;

    this.dropdown = document.querySelector("[data-pni-sort-dropdown]");
    this.dropdownButton = document.querySelector(
      "[data-pni-sort-dropdown-button]"
    );
    this.dropdownButtonContent = document.querySelector(
      "[data-pni-sort-dropdown-button-content]"
    );
    this.dropdownButtonArrow = document.querySelector(
      "[data-pni-sort-dropdown-button-arrow]"
    );

    this.listContainer = document.querySelector(
      "[data-pni-sort-dropdown-list-container]"
    );
    this.listItems = document.querySelectorAll(
      "[data-pni-sort-dropdown-list-item]"
    );
    this.listItemIds = [];

    if (!this.dropdown) {
      return console.error(
        `Could not find the PNI Creepiness Dropdown. PNI Creepiness Dropdown will not be available.`
      );
    }

    this.dropdownButton.addEventListener("click", (e) => {
      this.toggleListVisibility(e);
    });
    this.dropdownButton.addEventListener("keydown", (e) => {
      this.toggleListVisibility(e);
    });

    this.listItems.forEach((item) => this.listItemIds.push(item.id));

    this.listItems.forEach((item) => {
      item.addEventListener("click", (e) => {
        this.setSelectedListItem(e);
        this.closeList();
      });

      item.addEventListener("keydown", (e) => {
        if (
          SPACEBAR_KEY_CODE.includes(e.keyCode) ||
          e.keyCode === ENTER_KEY_CODE
        ) {
          e.preventDefault();
          this.setSelectedListItem(e);
          this.closeList();
        } else if (e.keyCode === DOWN_ARROW_KEY_CODE) {
          e.preventDefault();
          this.focusNextListItem(DOWN_ARROW_KEY_CODE);
        } else if (e.keyCode === UP_ARROW_KEY_CODE) {
          e.preventDefault();
          this.focusNextListItem(UP_ARROW_KEY_CODE);
        } else if (e.keyCode === ESCAPE_KEY_CODE) {
          this.closeList();
        }
      });
    });

    const url = new URLSearchParams(window.location.search);
    const searchParameter = url.get("search");
    // TODO need an inactive state for this dropdown when the search text is being applied
    // Update sort selected state on initialization but not when a search parameter is mentioned on the starting url
    if (history.state?.sort && !searchParameter) {
      document
        .querySelector(
          `[data-pni-sort-dropdown-list-item][data-value=${history.state.sort}]`
        )
        .click();
    }
  }

  /**
   * Sets the selected list item and updates the dropdown button content.
   * @param {Event} e - The event (e.g., click, keydown)
   * @param {boolean} [pushUpdate=true] - Whether to push the update to the history state.
   */
  setSelectedListItem(e, pushUpdate = true) {
    this.listItems.forEach((item) => {
      const itemDiv = item.querySelector("div");
      itemDiv.classList.remove("tw-text-black");
      itemDiv.classList.add("tw-text-gray-40");
    });
    const targetContent = e.target.querySelector("div");
    targetContent.classList.add("tw-text-black");
    targetContent.classList.remove("tw-text-gray-40");

    this.listContainer.setAttribute("aria-activedescendant", e.target.id);

    this.dropdownButtonContent.innerHTML = targetContent.innerHTML;
    if (pushUpdate) {
      this.searchFilter.updateSortHistoryState(e.target.dataset.value);
    }
  }

  /**
   * Closes the dropdown list.
   */
  closeList() {
    this.listContainer.classList.add("tw-hidden");
    this.dropdownButton.setAttribute("aria-expanded", false);
    this.dropdownButtonArrow.classList.remove("tw-rotate-180");
  }

  /**
   * Opens the dropdown list.
   *
   * @param {boolean} [withFocus=false] - Whether to focus on the first list item.
   */
  openList(withFocus = false) {
    this.listContainer.classList.remove("tw-hidden");
    this.dropdownButton.setAttribute("aria-expanded", true);
    this.dropdownButtonArrow.classList.add("tw-rotate-180");

    if (withFocus) {
      if (this.listItems.length > 0) {
        const firstOption = this.listItems[0];
        firstOption.focus();
      }
    }
  }

  /**
   * Toggle the visibility of the dropdown list
   *
   * @param {Event} e The event (e.g., click, keydown)
   */
  toggleListVisibility(e) {
    const isExpanded =
      this.dropdownButton.getAttribute("aria-expanded") === "true";

    if (
      e.keyCode === ESCAPE_KEY_CODE ||
      e.keyCode === UP_ARROW_KEY_CODE ||
      (e.type === "click" && isExpanded)
    ) {
      e.preventDefault();
      this.closeList();
    } else if (
      SPACEBAR_KEY_CODE.includes(e.keyCode) ||
      e.keyCode === ENTER_KEY_CODE ||
      e.keyCode === DOWN_ARROW_KEY_CODE ||
      (e.type === "click" && !isExpanded)
    ) {
      e.preventDefault();
      this.openList(true);
    }
  }

  /**
   * Focus on the next list item based on the given direction.
   *
   * @param {number} direction The key code of the direction to move the focus (e.g., key code for up arrow / down arrow)
   */
  focusNextListItem(direction) {
    const activeElementId = document.activeElement.id;
    const currentIndex = this.listItemIds.indexOf(activeElementId);

    // return early if active element is not in the list
    if (currentIndex < 0) return;

    // handle focus based on direction
    if (direction === DOWN_ARROW_KEY_CODE) {
      this.focusNextItem(currentIndex);
    } else if (direction === UP_ARROW_KEY_CODE) {
      this.focusPreviousItem(currentIndex);
    }
  }

  /**
   * Focus the next list item if it's not the last one.
   *
   * @param {number} currentIndex The index of the current active element in the list
   */
  focusNextItem(currentIndex) {
    const isNotLastItem = currentIndex < this.listItemIds.length - 1;
    if (isNotLastItem) {
      this.focusItem(currentIndex + 1);
    }
  }

  /**
   * Focus the previous list item if it's not the first, or focus the dropdown button.
   *
   * @param {number} currentIndex The index of the current active element in the list
   */
  focusPreviousItem(currentIndex) {
    if (currentIndex > 0) {
      this.focusItem(currentIndex - 1);
    } else {
      this.dropdownButton.focus();
    }
  }

  /**
   * Focus the list item at the specified index.
   *
   * @param {number} index The index of the item to focus
   */
  focusItem(index) {
    const nextListItemId = this.listItemIds[index];
    document.querySelector(`#${nextListItemId}`).focus();
  }
}
