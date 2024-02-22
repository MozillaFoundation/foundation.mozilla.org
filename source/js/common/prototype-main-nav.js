import navData from "./prototype-main-nav-data";

class DesktopPrimaryNav {
  constructor() {
    this.WIDE_SCREEN_NAV_LINKS_WRAPPER = document.querySelector(
      ".wide-screen-menu-container .nav-links"
    );
    this.LINK_ACTIVE_CLASS = "active";
    this.LINK_GRAYED_OUT_CLASS = "grayed-out";
  }

  renderCompiledTemplate(data) {
    const template = _.template(
      document.getElementById("prototype-nav-links-template").innerHTML
    );

    const html = template(data);
    this.WIDE_SCREEN_NAV_LINKS_WRAPPER.innerHTML = html;
  }

  setActiveNavLink() {
    const currentPath = window.location.pathname;

    if (currentPath === "/" || currentPath === "/en/") {
      return;
    }

    this.WIDE_SCREEN_NAV_LINKS_WRAPPER.querySelector(
      `a.primary[data-name="${navData.primaryNavLookUp[currentPath]}"]`
    ).classList.add(this.LINK_ACTIVE_CLASS);
  }

  grayOutAllLinks(grayOut = false, onHoverLink = null) {
    this.WIDE_SCREEN_NAV_LINKS_WRAPPER.querySelectorAll("a.primary").forEach(
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
    this.WIDE_SCREEN_NAV_LINKS_WRAPPER.querySelectorAll(
      ".nav-item-wrapper"
    ).forEach((wrapper) => {
      wrapper.addEventListener("mouseenter", () => {
        this.grayOutAllLinks(true, wrapper.querySelector("a.primary"));
      });

      wrapper.addEventListener("focusin", () => {
        this.grayOutAllLinks(true, wrapper.querySelector("a.primary"));
      });

      wrapper.addEventListener("mouseleave", () => {
        this.grayOutAllLinks(false, wrapper.querySelector("a.primary"));
      });

      wrapper.addEventListener("focusout", () => {
        this.grayOutAllLinks(false, wrapper.querySelector("a.primary"));
      });
    });
  }

  init(data) {
    this.renderCompiledTemplate(data);
    this.setActiveNavLink();
    this.setEventHandlers();
  }
}

const desktopPrimaryNav = new DesktopPrimaryNav();
desktopPrimaryNav.init(navData);
