import navData from "./prototype-main-nav-data";

class WidePrimaryNav {
  constructor() {
    this.TEMPALTE_SELECTOR = "#prototype-nav-links-template";
    this.NAV_LINKS_WRAPPER = document.querySelector(
      ".wide-screen-menu-container .nav-links"
    );
    this.LINK_ACTIVE_CLASS = "active";
    this.LINK_GRAYED_OUT_CLASS = "grayed-out";
  }

  renderCompiledTemplate(data) {
    const template = _.template(
      document.querySelector(this.TEMPALTE_SELECTOR).innerHTML
    );

    const html = template(data);
    this.NAV_LINKS_WRAPPER.innerHTML = html;
  }

  setActiveNavLink() {
    const currentPath = window.location.pathname;

    if (currentPath === "/" || currentPath === "/en/") {
      return;
    }

    this.NAV_LINKS_WRAPPER.querySelector(
      `.tw-primary-nav[data-name="${navData.primaryNavLookUp[currentPath]}"]`
    ).classList.add(this.LINK_ACTIVE_CLASS);
  }

  grayOutAllLinks(grayOut = false, onHoverLink = null) {
    this.NAV_LINKS_WRAPPER.querySelectorAll("a.tw-primary-nav").forEach(
      (link) => {
        if (link === onHoverLink) {
          return;
        }

        if (grayOut) {
          link.classList.add(this.LINK_GRAYED_OUT_CLASS);
        } else {
          link.classList.remove(this.LINK_GRAYED_OUT_CLASS);
        }
      }
    );
  }

  setEventHandlers() {
    this.NAV_LINKS_WRAPPER.querySelectorAll(".nav-item-wrapper").forEach(
      (wrapper) => {
        wrapper.addEventListener("mouseenter", () => {
          this.grayOutAllLinks(true, wrapper.querySelector("a.tw-primary-nav"));
        });

        wrapper.addEventListener("focusin", () => {
          this.grayOutAllLinks(
            true,
            wrapper.querySelector("a.primatw-primary-navry")
          );
        });

        wrapper.addEventListener("mouseleave", () => {
          this.grayOutAllLinks(
            false,
            wrapper.querySelector("a.tw-primary-nav")
          );
        });

        wrapper.addEventListener("focusout", () => {
          this.grayOutAllLinks(
            false,
            wrapper.querySelector("a.tw-primary-nav")
          );
        });
      }
    );
  }

  init(data) {
    this.renderCompiledTemplate(data);
    this.setActiveNavLink();
    this.setEventHandlers();
  }
}

const widePrimaryNav = new WidePrimaryNav();
widePrimaryNav.init(navData);

class NarrowPrimaryNav extends WidePrimaryNav {
  constructor() {
    super();

    this.TEMPALTE_SELECTOR = "#prototype-nav-links-mobile-template";
    this.NAV_LINKS_WRAPPER = document.querySelector(
      ".narrow-screen-menu-container .nav-links"
    );
  }

  setActiveNavLink() {
    const currentPath = window.location.pathname;

    if (currentPath === "/" || currentPath === "/en/") {
      return;
    }

    let activeNavSection = this.NAV_LINKS_WRAPPER.querySelector(
      `.nav-item-wrapper[data-name="${navData.primaryNavLookUp[currentPath]}"]`
    );

    if (!activeNavSection) {
      return;
    }

    activeNavSection.classList.add(this.LINK_ACTIVE_CLASS);
    activeNavSection
      .querySelectorAll("a.tw-secondary-nav-link")
      .forEach((link) => {
        if (link.getAttribute("href") === window.location.pathname) {
          link.classList.add(this.LINK_ACTIVE_CLASS);
        }
      });
  }

  slide(element, direction = "down") {
    if (direction === "down") {
      element.style.height = `${element.scrollHeight}px`;
    } else {
      element.style.height = "0";
    }
  }

  setEventHandlers() {
    this.NAV_LINKS_WRAPPER.querySelectorAll("button.tw-primary-nav").forEach(
      (btn) => {
        btn.addEventListener("click", () => {
          // flip the boolean value of aria-expanded
          btn.attributes["aria-expanded"].value =
            btn.attributes["aria-expanded"].value === "true" ? "false" : "true";

          if (btn.attributes["aria-expanded"].value === "true") {
            this.slide(btn.nextElementSibling, "down");
          } else {
            this.slide(btn.nextElementSibling, "up");
          }
        });
      }
    );
  }

  collapseAllSubmenus() {
    this.NAV_LINKS_WRAPPER.querySelectorAll(".submenu").forEach((submenu) => {
      this.slide(submenu, "up");
    });
  }

  init(data) {
    this.renderCompiledTemplate(data);
    this.setEventHandlers();
    this.setActiveNavLink();
    this.collapseAllSubmenus();

    console.log(data);
  }
}

const narrowPrimaryNav = new NarrowPrimaryNav();
narrowPrimaryNav.init(navData);
