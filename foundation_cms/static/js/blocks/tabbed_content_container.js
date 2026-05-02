import { updateIndicators, SWIPE_THRESHOLD } from "./util/carousel.js";

export function initTabbedContent() {
  const SELECTORS = {
    tabbedContent: ".tabbed-content-container",
    tabButtons: ".tabbed-content-container__tab-button",
    tabPanels: ".tabbed-content-container__tab-panel",
  };

  const CLASSNAMES = {
    isActive: "is-active",
  };

  const tabbedContents = document.querySelectorAll(SELECTORS.tabbedContent);

  tabbedContents.forEach((container) => {
    const buttons = container.querySelectorAll(SELECTORS.tabButtons);
    const panels = container.querySelectorAll(SELECTORS.tabPanels);

    // Refer content panels by index instead of ID to allow for multiple instances in one page.
    buttons.forEach((button, tabIndex) => {
      button.addEventListener("click", (event) => {
        panels.forEach((panel) => panel.classList.remove(CLASSNAMES.isActive));
        panels[tabIndex].classList.add(CLASSNAMES.isActive);
        buttons.forEach((btn) => btn.classList.remove(CLASSNAMES.isActive));
        button.classList.add(CLASSNAMES.isActive);
        button.scrollIntoView({
          behavior: "smooth",
          block: "nearest",
          inline: "start",
        });
      });
    });
  });

  initTabbedContentCardSets();
}

export function initTabbedContentCardSets() {
  const SELECTORS = {
    tabbedContentCardSetPanels:
      ".tabbed-content-container__tab-panel:has(>.tab-card)",
    tabbedContentCard: ".tab-card",
  };

  const CLASSNAMES = {
    tabCardPage: "tab-card__page",
  };

  const cardSetPanels = document.querySelectorAll(
    SELECTORS.tabbedContentCardSetPanels,
  );

  const getPanelPageWidth = (panel) => {
    const firstPage = panel.querySelector(`.${CLASSNAMES.tabCardPage}`);
    const gap = parseInt(window.getComputedStyle(panel).gap || "0", 10);
    return firstPage ? firstPage.clientWidth + gap : 0;
  };

  cardSetPanels.forEach((panel) => {
    const cards = panel.querySelectorAll(SELECTORS.tabbedContentCard);
    const cardsPerPage = parseInt(panel.dataset.cardsPerPage, 10);

    // Wrap cards in pages
    const pages = Math.ceil(cards.length / cardsPerPage);
    for (let i = 0; i < pages; i++) {
      const page = document.createElement("div");
      page.classList.add(CLASSNAMES.tabCardPage);

      const start = i * cardsPerPage;
      const end = start + cardsPerPage;
      Array.from(cards)
        .slice(start, end)
        .forEach((card) => page.appendChild(card));

      panel.appendChild(page);
    }

    if (pages <= 1) {
      return;
    }

    const initialScrollLeft = panel.scrollLeft;
    const pageWidth = getPanelPageWidth(panel);
    const initialPageIndex =
      initialScrollLeft > 0 ? Math.floor(initialScrollLeft / pageWidth) : 0;

    updateIndicators(panel, initialPageIndex);

    panel.addEventListener("scroll", () => {
      const width = getPanelPageWidth(panel);
      if (width > 0) {
        updateIndicators(panel, Math.round(panel.scrollLeft / width));
      }
    });

    let touchStartX = 0;

    panel.addEventListener(
      "touchstart",
      (e) => {
        touchStartX = e.touches[0].clientX;
      },
      { passive: true },
    );

    panel.addEventListener(
      "touchend",
      (e) => {
        const delta = e.changedTouches[0].clientX - touchStartX;
        if (Math.abs(delta) < SWIPE_THRESHOLD) return;

        const width = getPanelPageWidth(panel);
        const currentIndex = Math.round(panel.scrollLeft / width);
        const newIndex =
          delta < 0
            ? Math.min(currentIndex + 1, pages - 1)
            : Math.max(currentIndex - 1, 0);

        panel.scrollTo({ left: newIndex * width, behavior: "smooth" });
      },
      { passive: true },
    );
  });
}
