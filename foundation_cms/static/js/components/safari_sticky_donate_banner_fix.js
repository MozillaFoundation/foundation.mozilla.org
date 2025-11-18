const SELECTORS = {
  pushdownDonateBanner: ".donate-banner[data-banner-style='pushdown']",
  siteNav: ".primary-nav-ns",
  mainContent: ".main-content-wrapper",
};

export function initSafariStickyFix() {
  const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);

  if (isSafari) {
    const banner = document.querySelector(SELECTORS.pushdownDonateBanner);
    const nav = document.querySelector(SELECTORS.siteNav);
    const mainContent = document.querySelector(SELECTORS.mainContent);

    if (banner && nav && mainContent) {
      const SCROLL_THRESHOLD = 10;
      const BANNER_Z_DISTANCE = -9999;
      const CONTENT_Z_DISTANCE = 1;

      // Force Safari to recalculate stacking on scroll
      window.addEventListener(
        "scroll",
        () => {
          // Safari sticky fix:
          //   Create massive 3D separation between layers.
          //   Banner at far back can't paint over nav/content at front.
          //   This overrides Safari's buggy sticky element rendering.
          if (window.scrollY > SCROLL_THRESHOLD) {
            const bannerTransZ = `translateZ(${BANNER_Z_DISTANCE}px)`;
            const navTransZ = `translateZ(${CONTENT_Z_DISTANCE}px)`;
            const mainContentTransZ = navTransZ;

            // Hide banner by moving it way back
            banner.style.transform = bannerTransZ;
            banner.style.webkitTransform = bannerTransZ;

            // Bring nav and content forward
            nav.style.transform = navTransZ;
            nav.style.webkitTransform = navTransZ;
            mainContent.style.transform = mainContentTransZ;
            mainContent.style.webkitTransform = mainContentTransZ;
          } else {
            // Reset when at top
            banner.style.transform = "";
            banner.style.webkitTransform = "";
            nav.style.transform = "";
            nav.style.webkitTransform = "";
            mainContent.style.transform = "";
            mainContent.style.webkitTransform = "";
          }
        },
        { passive: true },
      );
    }
  }
}
