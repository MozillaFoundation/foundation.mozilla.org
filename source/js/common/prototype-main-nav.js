import navData from "./prototype-main-nav-data";

const WIDE_SCREEN_NAV_LINKS_WRAPPER = document.querySelector(
  ".wide-screen-menu-container .nav-links"
);
const LINK_ACTIVE_CLASS = "active";
const LINK_GRAYED_OUT_CLASS = "grayed-out";

function renderCompiledTemplate(data) {
  const template = _.template(
    document.getElementById("prototype-nav-links-template").innerHTML
  );

  const html = template(data);
  WIDE_SCREEN_NAV_LINKS_WRAPPER.innerHTML = html;
}

function setActiveNavLink() {
  const currentPath = window.location.pathname;

  if (currentPath === "/" || currentPath === "/en/") {
    return;
  }

  WIDE_SCREEN_NAV_LINKS_WRAPPER.querySelector(
    `a.primary[data-name="${navData.primaryNavLookUp[currentPath]}"]`
  ).classList.add(LINK_ACTIVE_CLASS);
}

function grayOutAllLinks(grayOut = false, onHoverLink = null) {
  WIDE_SCREEN_NAV_LINKS_WRAPPER.querySelectorAll("a.primary").forEach(
    (link) => {
      if (link === onHoverLink) {
        return;
      }

      if (grayOut) {
        link.classList.add(LINK_GRAYED_OUT_CLASS);
      } else {
        link.classList.remove(LINK_GRAYED_OUT_CLASS);
      }
    }
  );
}

function setEventHandlers() {
  WIDE_SCREEN_NAV_LINKS_WRAPPER.querySelectorAll(".nav-item-wrapper").forEach(
    (wrapper) => {
      wrapper.addEventListener("mouseenter", () => {
        grayOutAllLinks(true, wrapper.querySelector("a.primary"));
      });

      wrapper.addEventListener("focusin", () => {
        grayOutAllLinks(true, wrapper.querySelector("a.primary"));
      });

      wrapper.addEventListener("mouseleave", () => {
        grayOutAllLinks(false, wrapper.querySelector("a.primary"));
      });

      wrapper.addEventListener("focusout", () => {
        grayOutAllLinks(false, wrapper.querySelector("a.primary"));
      });
    }
  );
}

renderCompiledTemplate(navData);
setActiveNavLink();
setEventHandlers();
