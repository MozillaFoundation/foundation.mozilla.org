const SELECTORS = {
  item: ".gallery-strip__item",
  navItem: ".gallery-nav__item",
};


const CLASS_NAMES = {
  active: "is-active",
};

export default function initGalleryScrollspy() {
  const items = document.querySelectorAll(SELECTORS.item);
  const navLinks = document.querySelectorAll(SELECTORS.navItem);

  if (!items.length || !navLinks.length) return;

  const itemList = Array.from(items);

  function setActive(index) {
    navLinks.forEach((link, i) => {
      link.classList.toggle(CLASS_NAMES.active, i === index);
    });
    navLinks[index]?.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  // Highlight the nav item whose image enters the middle 30% of the viewport
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          setActive(itemList.indexOf(entry.target));
        }
      });
    },
    {
      rootMargin: "-35% 0px -35% 0px",
      threshold: 0,
    },
  );

  items.forEach((item) => observer.observe(item));

  navLinks.forEach((btn, i) => {
    btn.addEventListener("click", () => {
      itemList[i]?.scrollIntoView({ behavior: "smooth" });
    });
  });
}

initGalleryScrollspy();
