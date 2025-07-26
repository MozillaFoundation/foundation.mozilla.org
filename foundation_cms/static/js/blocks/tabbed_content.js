export function initTabbedContent() {
  const SELECTORS = {
    tabbedContent: ".tabbed-content",
    tabButtons: ".tabbed-content__tab-button",
    tabPanels: ".tabbed-content__tab-panel",
  };

  const tabbedContents = document.querySelectorAll(SELECTORS.tabbedContent);

  tabbedContents.forEach((container) => {
    const buttons = container.querySelectorAll(SELECTORS.tabButtons);
    const panels = container.querySelectorAll(SELECTORS.tabPanels);

    // Refer content panels by index instead of ID to allow for multiple instances in one page.
    buttons.forEach((button, tabIndex) => {
      button.addEventListener("click", (event) => {
        panels.forEach((panel) => panel.classList.remove("is-active"));
        panels[tabIndex].classList.add("is-active");
        button.scrollIntoView({
          behavior: "smooth",
          block: "nearest",
          inline: "start",
        });
      });
    });
  });
}
