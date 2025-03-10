let content, currentTab;

/**
 * Highlight the given tab by updating its class list and aria attribute
 * @param {HTMLElement} target tab to be highlighted
 * @returns {HTMLElement} highlighted tab with updated class list and aria attribute
 */
function setHighlight(target) {
  let button = target.querySelector("button");
  button.classList.remove(
    "tw-bg-white",
    "tw-text-black",
    "hover:tw-text-blue-80"
  );
  button.classList.add("tw-bg-black", "tw-text-white");
  button.setAttribute("aria-selected", "true");
  return target;
}

/**
 * Remove highlight from the given tab by updating its class list and aria attribute
 * @param {*} target tab to be unhighlighted
 * @returns {HTMLElement} unhighlighted tab with updated class list and aria attribute
 */
function removeHighlight(target) {
  let button = target.querySelector("button");
  button.classList.remove("tw-bg-black", "tw-text-white");
  button.classList.add("tw-bg-white", "tw-text-black", "hover:tw-text-blue-80");
  button.setAttribute("aria-selected", "false");
  return target;
}

/**
 * Show corresponding tab content by shifting its location in the viewport
 * @param {HTMLElement} tab Tab to show
 * @param {number} position Index of the tab in the tab group
 */
function scrollTabButtons(tab, position) {
  const tabContent = document.querySelector("#product-tab-group");
  tabContent.scrollLeft = tab.offsetWidth * position - tab.offsetWidth / 2;
}

/**
 * Switch to tab of choice
 * @param {HTMLElement} tab Tab to switched to
 * @param {number} position Index of the tab in the tab group
 */
function switchToTab(tab, position) {
  let contentContainer;

  removeHighlight(currentTab);
  currentTab = setHighlight(tab);
  scrollTabButtons(tab, position);

  content.querySelectorAll(`div[data-product-label]`).forEach((container) => {
    if (container.getAttribute("data-product-label") == position) {
      container.classList.remove("tw-invisible");
      contentContainer = container;
    } else {
      container.classList.add("tw-invisible");
    }
  });

  content.style.setProperty(`--x-offset`, `${position * -100}%`);
  content.style.setProperty(`height`, `${contentContainer.clientHeight}px`);
}

/**
 * Add tab group functionality and styling to #product-tab and children
 */
export default () => {
  const productTab = document.getElementById(`product-tab`);
  if (!productTab) return;

  content = document.getElementById(`product-tab-content`);
  if (!content) return;

  const allTabs = productTab.querySelectorAll("li[data-product-label]");
  if (allTabs.length === 0) return;

  // First tab is active by default
  currentTab = setHighlight(allTabs[0]);

  allTabs.forEach((tab, position) => {
    tab.addEventListener("click", () => {
      if (currentTab === tab) return;
      switchToTab(tab, position);
    });
  });
};
