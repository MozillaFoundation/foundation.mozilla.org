const THRESHOLD = 300; // px

const SELECTORS = {
  backToTopButton: ".back-to-top",
};

export default function initBackToTopButton() {
  const btn = document.querySelector(SELECTORS.backToTopButton);
  if (!btn) return;

  // Create sentinel at very top of <body>
  let sentinel = document.getElementById("back-to-top-sentinel");
  if (!sentinel) {
    sentinel = document.createElement("span");
    sentinel.id = "back-to-top-sentinel";
    sentinel.setAttribute("aria-hidden", "true");
    sentinel.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      width: 1px;
      height: 1px;
      pointer-events: none;
    `;
    document.body.prepend(sentinel);
  }

  // Observe the sentinel to toggle visibility of the button
  const io = new IntersectionObserver(
    ([entry]) => {
      btn.classList.toggle("visible", !entry.isIntersecting);
    },
    {
      root: null,
      threshold: 0,
      rootMargin: `${THRESHOLD}px 0px 0px 0px`,
    },
  );

  io.observe(sentinel);

  // Smooth scroll to top
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    const reduce = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
  });
}
