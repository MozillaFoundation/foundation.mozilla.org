function initProductReviewMetaToggle() {
  const SELECTORS = {
    toggle: ".intro-section__who-am-i-toggle",
  };

  const toggleLinks = document.querySelectorAll(SELECTORS.toggle);

  toggleLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();

      const targetClass = link.getAttribute("data-toggles");
      const targetElement = document.querySelector(`.${targetClass}`);

      targetElement.classList.toggle("is-active");

      // Toggle with grow animation using maxheight + scrollHeight
      if (targetElement.classList.contains("is-active")) {
        link.textContent = gettext("Less details -");
        targetElement.style.maxHeight = targetElement.scrollHeight + "px";
      } else {
        link.textContent = gettext("More details +");
        targetElement.style.maxHeight = null;
      }
    });

    // Hide the target element by default
    const targetClass = link.getAttribute("data-toggles");
    const targetElement = document.querySelector(`.${targetClass}`);
    targetElement.style.maxHeight = null;
  });
}

initProductReviewMetaToggle();
