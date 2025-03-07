import Accordion from "../../components/accordion/accordion.js";
import NavDesktopDropdown from "../../components/nav/desktop-dropdown.js";
import NavMobileDropdown from "../../components/nav/mobile-dropdown.js";

function initComponent(ComponentClass) {
  const items = document.querySelectorAll(ComponentClass.selector());
  items.forEach((item) => new ComponentClass(item));
}

/**
 * SiteNav object for handling site navigation related functionality.
 */
let SiteNav = {
  /**
   * The session storage key to store the nav link clicked.
   */
  SESSION_STORAGE_KEY_NAV_LINK: "navLinkClicked",
  /**
   * The session storage key to store the dropdown id of the nav link clicked.
   */
  SESSION_STORAGE_KEY_DROPDOWN_ID: "navLinkDropdownId",
  /**
   * Initializes the SiteNav object
   */
  init() {
    this.setupNavLinkEventHandlers();
    this.findNavLinkClicked();

    initComponent(Accordion);
    initComponent(NavDesktopDropdown);
    initComponent(NavMobileDropdown);
  },
  /**
   * Set up the event handlers for the nav links in the nav dropdowns.
   */
  setupNavLinkEventHandlers() {
    document
      .querySelectorAll(
        `.primary-nav-container [data-mobile-dropdown] a[href]:not([href=""]),
         .primary-nav-container [data-desktop-dropdown] a[href]:not([href=""])`
      )
      .forEach((link) => {
        link.addEventListener("click", (e) => {
          e.preventDefault();

          sessionStorage.setItem(
            this.SESSION_STORAGE_KEY_NAV_LINK,
            link.textContent
          );
          sessionStorage.setItem(
            this.SESSION_STORAGE_KEY_DROPDOWN_ID,
            link.closest("[data-dropdown-id]").dataset.dropdownId
          );

          // navigate to the clicked link
          window.location.href = link.href;
        });
      });
  },
  /**
   * Find the nav link that was clicked to get to the current page and
   *   highlight the dropdown that nav link belongs to.
   */
  findNavLinkClicked() {
    const navLinkClicked = sessionStorage.getItem(
      this.SESSION_STORAGE_KEY_NAV_LINK
    );
    const navLinkDropdownId = sessionStorage.getItem(
      this.SESSION_STORAGE_KEY_DROPDOWN_ID
    );

    if (navLinkClicked && navLinkDropdownId) {
      // if we know what nav link the user clicked to get to the current page,
      //     highlight the dropdown that nav link belongs to

      // querySelectorAll because there are two dropdowns with the same dropdown id,
      //     one for mobile nav, one for desktop nav
      const dropdowns = document.querySelectorAll(
        `.primary-nav-container [data-dropdown-id="${navLinkDropdownId}"]`
      );

      dropdowns.forEach((dropdown) => {
        dropdown.dataset.shouldWayfindingBeActive = "true";
      });
    } else {
      // highlight the first dropdown that has the matching wayfinding link

      const mobileMatchingDropdown = document.querySelector(
        `.primary-nav-container [data-mobile-dropdown][data-dropdown-id][data-can-wayfinding-be-active="true"]`
      );
      const desktopMatchingDropdown = document.querySelector(
        `.primary-nav-container [data-desktop-dropdown][data-can-wayfinding-be-active="true"]`
      );

      if (mobileMatchingDropdown) {
        mobileMatchingDropdown.dataset.shouldWayfindingBeActive = "true";
      }

      if (desktopMatchingDropdown) {
        desktopMatchingDropdown.dataset.shouldWayfindingBeActive = "true";
      }
    }

    sessionStorage.removeItem(this.SESSION_STORAGE_KEY_NAV_LINK);
    sessionStorage.removeItem(this.SESSION_STORAGE_KEY_DROPDOWN_ID);
  },
};

export default SiteNav;
