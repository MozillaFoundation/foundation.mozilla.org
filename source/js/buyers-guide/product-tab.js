let content, currentTab;

function setHighlight(target) {
  target.classList.remove(
    "tw-bg-white",
    "tw-text-black",
    "hover:tw-text-blue-80"
  );
  target.classList.add("tw-bg-black", "tw-text-white");
  return target;
}

function removeHighlight(target) {
  target.classList.remove("tw-bg-black", "tw-text-white");
  target.classList.add("tw-bg-white", "tw-text-black", "hover:tw-text-blue-80");
  return target;
}

function scrollTabButtons(tab, position) {
  const tabContent = document.querySelector("#product-tab-group");
  tabContent.scrollLeft = tab.offsetWidth * position - tab.offsetWidth / 2;
}

function switchToTab(tab, position) {
  removeHighlight(currentTab);
  currentTab = setHighlight(tab);
  scrollTabButtons(tab, position);
  const contentContainer = document.querySelector(
    `div[data-product-label="${position}"`
  );

  content.style.setProperty(`--x-offset`, `${position * -100}%`);
  content.style.setProperty(`height`, `${contentContainer.clientHeight}px`);
}

export default () => {
  const productTab = document.getElementById(`product-tab`);
  if (!productTab) return;

  content = document.getElementById(`product-tab-content`);
  if (!content) return;

  const allTabs = productTab.querySelectorAll("span[data-product-label]");
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
