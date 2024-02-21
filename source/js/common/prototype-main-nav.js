import navData from "./prototype-main-nav-data";

const WIDE_SCREEN_NAV_LINKS_WRAPPER = document.querySelector(
  "#wide-screen-nav-links"
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

function grayOutLink(navLink) {
  navLink.classList.add(LINK_GRAYED_OUT_CLASS);
}

function setActiveNavLink() {
  const currentPath = window.location.pathname;

  if (currentPath === "/" || currentPath === "/en/") {
    return;
  }

  WIDE_SCREEN_NAV_LINKS_WRAPPER.querySelectorAll("a.primary").forEach(
    (link) => {
      if (link.pathname === currentPath) {
        link.classList.add(LINK_ACTIVE_CLASS);
      } else {
        grayOutLink(link);
      }
    }
  );
}

function grayOutActiveLink(grayOut = false) {
  const activeLink =
    WIDE_SCREEN_NAV_LINKS_WRAPPER.querySelector("a.primary.active");

  if (!activeLink) {
    return;
  }

  if (grayOut) {
    activeLink.classList.add(LINK_GRAYED_OUT_CLASS);
  } else {
    activeLink.classList.remove(LINK_GRAYED_OUT_CLASS);
  }
}

function setEventHandlers() {
  WIDE_SCREEN_NAV_LINKS_WRAPPER.querySelectorAll(
    "a.primary:not(.active)"
  ).forEach((link) => {
    link.addEventListener("mouseover", () => {
      grayOutActiveLink(true);
    });

    link.addEventListener("focus", () => {
      grayOutActiveLink(true);
    });

    link.addEventListener("mouseout", () => {
      grayOutActiveLink(false);
    });

    link.addEventListener("blur", () => {
      grayOutActiveLink(false);
    });
  });
}

renderCompiledTemplate(navData);
setActiveNavLink();
setEventHandlers();
