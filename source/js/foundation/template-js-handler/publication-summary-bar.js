/**
 * Summary bar on the publication page shows up when scrolled passed the hero.
 */
export default () => {
  const summaryBlock = document.querySelector(".article-navbar-container");
  if (summaryBlock) {
    const marginOffset = window
      .getComputedStyle(summaryBlock)
      .getPropertyValue("--top-offset");
    const dropDownMenu = document.querySelector(".article-summary-menu");
    const articleSummaryToggle = document.querySelector(
      ".article-summary-toggle"
    );

    // sticky nav toggle for scrolling past the header
    const summaryObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.intersectionRatio === 0) {
          // Toggle summary block off
          summaryBlock.style.top = "0";
          summaryBlock.setAttribute("aria-hidden", true);
        } else {
          // Toggle summary block on
          summaryBlock.style.top = marginOffset;
          summaryBlock.setAttribute("aria-hidden", false);
          dropDownMenu.classList.remove("d-block");
          articleSummaryToggle.classList.remove("show");
          document.querySelector(".toggle-text").innerText = document
            .querySelector(".toggle-text")
            .getAttribute("data-open");
        }
      });
    });

    // update the title based on the header in the article in past by
    const titleObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const title = entry.target.innerText;
        if (entry.intersectionRatio > 0) {
          document.querySelector(
            ".dropdown-toggle.article-summary-toggle span"
          ).innerText = title;
        }
      });
    });

    summaryObserver.observe(
      document.querySelector(".publication-hero-container")
    );

    document.querySelectorAll(".rich-text h2").forEach((section) => {
      titleObserver.observe(section);
    });

    // accordion button toggle
    document.querySelectorAll(".article-header-button").forEach((button) => {
      button.addEventListener("click", () => {
        console.log(
          document.querySelectorAll(
            `.article-child-menu[data-expand="${button.dataset.expand}"]`
          )
        );
        document
          .querySelector(
            `.article-child-menu[data-expand="${button.dataset.expand}"]`
          )
          .classList.toggle("tw-hidden");
        button
          .querySelector("img[data-state='open']")
          .classList.toggle("tw-hidden");
        button
          .querySelector("img[data-state='close']")
          .classList.toggle("tw-hidden");
      });
    });

    // child button toggle
    document.querySelectorAll(".article-child-button").forEach((button) => {
      button.addEventListener("click", () => {
        if (!button.dataset.expand) {
          document
            .querySelector(`.article-child-container:not(.tw-hidden)`)
            .classList.add("tw-hidden");
          document
            .querySelector(".article-container")
            .classList.remove("tw-hidden");

          return;
        }

        document
          .querySelector(
            `.article-child-container[data-child="${button.dataset.expand}"]`
          )
          .classList.remove("tw-hidden");
        document
          .querySelector(".article-container")
          .classList.toggle("tw-hidden");
      });
    });

    // we need to calculate the height for the new dropdown menu since it is a absolute element with sticky elements in the way
    function calcSummaryMenuHeight() {
      const stickyContent = document.querySelector(
        ".wrapper > .sticky-top.d-print-none"
      );

      if (window.matchMedia("(min-width: 992px)").matches) {
        dropDownMenu.style.maxHeight = `calc(100vh - ${stickyContent.offsetHeight}px)`;
        dropDownMenu.style.height = `auto`;
      } else {
        // accordion should always be max remaining height on tablet and mobile
        dropDownMenu.style.maxHeight = `calc(100vh - ${stickyContent.offsetHeight}px)`;
        dropDownMenu.style.height = `calc(100vh - ${stickyContent.offsetHeight}px)`;
      }
    }

    calcSummaryMenuHeight();

    window.onresize = calcSummaryMenuHeight;
  }
};
