const SPACEBAR_KEY_CODE = [0, 32];
const ENTER_KEY_CODE = 13;
const DOWN_ARROW_KEY_CODE = 40;
const UP_ARROW_KEY_CODE = 38;
const ESCAPE_KEY_CODE = 27;

export class PNISortDropdown {
  constructor(searchFilter) {
    this.searchFilter = searchFilter;
    this.dropdown = document.querySelector(`#pni-creepiness`);
    this.list = document.querySelector(".pni-creepiness__list");
    this.listContainer = document.querySelector(
      ".pni-creepiness__list-container"
    );
    this.dropdownArrow = document.querySelector(".pni-creepiness__arrow");
    this.listItems = document.querySelectorAll(".pni-creepiness__list-item");
    this.dropdownSelectedNode = document.querySelector(
      "#pni-creepiness__selected"
    );
    this.listItemIds = [];

    if (!this.dropdown) {
      return console.error(
        `Could not find the PNI Creepiness Dropdown. PNI Creepiness Dropdown will not be available.`
      );
    }

    this.dropdownSelectedNode.addEventListener("click", (e) =>
      this.toggleListVisibility(e)
    );
    this.dropdownSelectedNode.addEventListener("keydown", (e) =>
      this.toggleListVisibility(e)
    );

    this.listItems.forEach((item) => this.listItemIds.push(item.id));

    this.listItems.forEach((item) => {
      item.addEventListener("click", (e) => {
        this.setSelectedListItem(e);
        this.closeList();
      });

      item.addEventListener("keydown", (e) => {
        switch (e.keyCode) {
          case ENTER_KEY_CODE:
            this.setSelectedListItem(e);
            this.closeList();
            return;

          case DOWN_ARROW_KEY_CODE:
            this.focusNextListItem(DOWN_ARROW_KEY_CODE);
            return;

          case UP_ARROW_KEY_CODE:
            this.focusNextListItem(UP_ARROW_KEY_CODE);
            return;

          case ESCAPE_KEY_CODE:
            this.closeList();
            return;

          default:
            return;
        }
      });
    });

    // Update sort selected state on initialization
    if (history.state?.sort) {
      document
        .querySelector(
          `li.pni-creepiness__list-item[data-value=${history.state.sort}]`
        )
        .click();
    }
  }

  setSelectedListItem(e, pushUpdate = true) {
    this.listItems.forEach((item) => {
      const itemDiv = item.querySelector("div");
      itemDiv.classList.remove("tw-text-black");
      itemDiv.classList.add("tw-text-gray-40");
    });
    const targetContent = e.target.querySelector("div");
    targetContent.classList.add("tw-text-black");
    targetContent.classList.remove("tw-text-gray-40");
    const content = this.dropdownSelectedNode.querySelector("div");
    content.innerHTML = targetContent.innerHTML;
    if (pushUpdate) {
      this.searchFilter.updateSort(e.target.dataset.value);
    }
  }

  closeList() {
    this.listContainer.classList.add("tw-hidden");
    this.listContainer.setAttribute("aria-expanded", false);
  }

  toggleListVisibility(e) {
    let openDropDown =
      SPACEBAR_KEY_CODE.includes(e.keyCode) || e.keyCode === ENTER_KEY_CODE;

    if (e.keyCode === ESCAPE_KEY_CODE) {
      this.closeList();
    }

    if (e.type === "click" || openDropDown) {
      this.listContainer.classList.remove("tw-hidden");

      this.listContainer.setAttribute(
        "aria-expanded",
        this.listContainer.classList.contains("tw-hidden")
      );
    }

    if (e.keyCode === DOWN_ARROW_KEY_CODE) {
      this.focusNextListItem(DOWN_ARROW_KEY_CODE);
    }

    if (e.keyCode === UP_ARROW_KEY_CODE) {
      this.focusNextListItem(UP_ARROW_KEY_CODE);
    }
  }

  focusNextListItem(direction) {
    const activeElementId = document.activeElement.id;
    if (activeElementId === "pni-creepiness__selected") {
      document.querySelector(`#${this.listItemIds[0]}`).focus();
    } else {
      const currentActiveElementIndex =
        this.listItemIds.indexOf(activeElementId);
      if (direction === DOWN_ARROW_KEY_CODE) {
        const currentActiveElementIsNotLastItem =
          currentActiveElementIndex < this.listItemIds.length - 1;
        if (currentActiveElementIsNotLastItem) {
          const nextListItemId =
            this.listItemIds[currentActiveElementIndex + 1];
          document.querySelector(`#${nextListItemId}`).focus();
        }
      } else if (direction === UP_ARROW_KEY_CODE) {
        const currentActiveElementIsNotFirstItem =
          currentActiveElementIndex > 0;
        if (currentActiveElementIsNotFirstItem) {
          const nextListItemId =
            this.listItemIds[currentActiveElementIndex - 1];
          document.querySelector(`#${nextListItemId}`).focus();
        }
      }
    }
  }
}
