const SELECTORS = {
  primaryNav: ".primary-nav",
  hamburger: ".primary-nav .hamburger",
};

export function initPrimaryNav() {
  console.log("Initializing primary navigation...");

  const hamburger = document.querySelector(SELECTORS.hamburger);
  const nav = document.querySelector(SELECTORS.primaryNav);
  if (!nav || !hamburger) return;

  document.body.classList.add("has-primary-nav");

  hamburger.addEventListener("click", () => {
    nav.classList.toggle("open");
    hamburger.classList.toggle("active");
  });

  console.log(
    "Primary navigation initialized. Click the hamburger icon to toggle the menu.",
  );
}
