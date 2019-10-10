import React from "react";
import ReactGA from "react-ga";
import ReactDOM from "react-dom";
import JoinUs from "./components/join/join.jsx";

const elements = {
  primaryNav: `#primary-nav-container`,
  narrowMenuContainer: `#primary-nav-container .narrow-screen-menu-container`,
  wideMenuContainer: `#primary-nav-container .wide-screen-menu-container`,
  buttonMobile: `#primary-nav-container .narrow-screen-menu-container .btn-newsletter`,
  buttonDesktop: `#primary-nav-container .wide-screen-menu-container .btn-newsletter`,
  container: `#nav-newsletter-form-wrapper`,
  joinUs: `#nav-newsletter-form-wrapper .join-us.on-nav`,
  buttonDismiss: `#nav-newsletter-form-wrapper .form-dismiss`
};

class NavNewsletter {
  constructor() {
    this.isShown = false;
    this.form = null;
  }

  getShownState() {
    return this.isShown;
  }

  // Reset form
  resetForm() {
    this.form.reset();

    let handleTransitionend = () => {
      elements.container.removeEventListener(
        "transitionend",
        handleTransitionend
      );
      elements.buttonDismiss.textContent = "No thanks";
    };
    elements.container.addEventListener("transitionend", handleTransitionend);
  }

  // For desktop+ version:
  // transition section to its close state,
  // remove the global 'closeFormClickHandler' click event handler
  // and reset the form
  closeDesktopNewsletter(event) {
    elements.container.classList.remove("expanded");
    elements.buttonDesktop.classList.remove("active");
    document.removeEventListener("click", this.closeFormClickHandler);
    document.removeEventListener("scroll", this.closeFormClickHandler);
    this.resetForm();
    this.isShown = false;
  }

  // For desktop+ version:
  // transition newsletter section to its expanded state
  expandDesktopNewsletter(event) {
    elements.container.style.top = `${elements.primaryNav.offsetHeight}px`;
    elements.container.classList.add("expanded");
    elements.buttonDesktop.classList.add("active");
    document.addEventListener(`click`, this.closeFormClickHandler);
    document.addEventListener("scroll", this.closeFormClickHandler);
    this.isShown = true;
  }

  // For mobile version:
  // transition newsletter section to its close state,
  // remove the global 'closeFormClickHandler' click event handler,
  // and reset the form
  closeMobileNewsletter() {
    elements.narrowMenuContainer.classList.remove("d-none");
    elements.container.classList.remove("faded-in");
    this.resetForm();
    this.isShown = false;
  }

  // For mobile version:
  // transition section to its expanded state
  expandMobileNewsletter() {
    elements.narrowMenuContainer.classList.add(`d-none`);
    elements.container.classList.add("faded-in");
    this.isShown = true;
  }

  // For desktop+ version:
  // create click handler to detect clicking event outside of the newsletter section
  closeFormClickHandler(event) {
    // close newsletter section if clicking anywhere outside of the section
    if (
      !elements.container.contains(event.target) &&
      event.target !== elements.container
    ) {
      navNewsletter.closeDesktopNewsletter();
    }
  }

  /**
   * Find and bind all necessary DOM nodes, returning "false" if not all DOM nodes were found.
   */
  checkDomNodes() {
    return Object.keys(elements).every(key => {
      // if this element already resolved to a DOM node, move on to the next
      let value = elements[key];
      if (typeof value !== "string") return true;

      // find this DOM node, and report on the result (binding it if found for later use)
      let element = document.querySelector(value);
      if (element) elements[key] = element;
      return !!element;
    });
  }

  buttonDesktopClickHandler(event) {
    if (!this.isShown) {
      event.stopPropagation();
      this.expandDesktopNewsletter();
    } else {
      this.closeDesktopNewsletter();
    }
  }

  init(foundationSiteURL, csrfToken) {
    // some DOM nodes do not exist, return
    if (!this.checkDomNodes()) return;

    var props = elements.joinUs.dataset;
    props.apiUrl = `${foundationSiteURL}/api/campaign/signups/${props.signupId ||
      0}/`;
    props.csrfToken = props.csrfToken || csrfToken;
    props.isHidden = false;
    this.form = ReactDOM.render(<JoinUs {...props} />, elements.joinUs);

    // For desktop+ version:
    // make 'buttonDesktop' the trigger to open newsletter section
    elements.buttonDesktop.addEventListener(`click`, event => {
      this.buttonDesktopClickHandler(event);
    });

    // For mobile version:
    // make 'buttonDismiss' the trigger to close newsletter section
    elements.buttonDismiss.addEventListener("click", () => {
      this.closeMobileNewsletter();
    });

    // For mobile version:
    // make 'buttonMobile' the trigger to show newsletter section
    elements.buttonMobile.addEventListener("click", () => {
      this.expandMobileNewsletter();
    });
  }
}

const navNewsletter = new NavNewsletter();

export default navNewsletter;
