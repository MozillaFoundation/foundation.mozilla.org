import React from "react";
import ReactGA from "react-ga";
import ReactDOM from "react-dom";
import JoinUs from "./components/join/join.jsx";

let isShown = false;
let foundationSiteURL, csrfToken;
let primaryNav = document.querySelector(`#primary-nav-container`);
let narrowMenuContainer = primaryNav.querySelector(
  ".narrow-screen-menu-container"
);
let wideMenuContainer = primaryNav.querySelector(".wide-screen-menu-container");
let container = document.querySelector("#nav-newsletter-form-wrapper");
let buttonDesktop = wideMenuContainer.querySelector(".btn-newsletter");
let buttonMobile = narrowMenuContainer.querySelector(".btn-newsletter");
let joinUs = container.querySelector(`.join-us.on-nav`);
let buttonDismiss = container.querySelector(".form-dismiss");

let navNewsletter = {
  getShownState: () => {
    return isShown;
  },

  // Inject a new <JoinUs> component each time so we can show <JoinUs> with its initial state
  injectForm: () => {
    if (joinUs) {
      var props = joinUs.dataset;

      props.apiUrl = `${foundationSiteURL}/api/campaign/signups/${props.signupId ||
        0}/`;

      props.csrfToken = props.csrfToken || csrfToken;
      props.isHidden = false;

      ReactDOM.render(<JoinUs {...props} />, joinUs);
    }
  },

  // We can't simply reset the form as we don't
  // have access to trigger <JoinUs> React component's state or lifecycle.
  // Instead, we unmount <JoinUs> from DOM.
  unmountForm: () => {
    // unmount form after newsletter section has transitioned back to the previous view
    let handleTransitionend = () => {
      container.removeEventListener("transitionend", handleTransitionend);
      ReactDOM.unmountComponentAtNode(container.querySelector(".join-us"));
    };
    container.addEventListener("transitionend", handleTransitionend);
  },

  // For desktop+ version:
  // transition section to its close state,
  // remove the global 'closeFormClickHandler' click event handler
  // and unmount the form from DOM
  closeDesktopNewsletter: event => {
    container.classList.remove("expanded");
    buttonDesktop.classList.remove("active");
    document.removeEventListener("click", navNewsletter.closeFormClickHandler);
    navNewsletter.unmountForm();
    isShown = false;
  },

  // For desktop+ version:
  // inject a new sign up form then transition section to its expanded state
  expandDesktopNewsletter: event => {
    navNewsletter.injectForm();
    container.classList.add("expanded");
    buttonDesktop.classList.add("active");
    document.addEventListener(`click`, navNewsletter.closeFormClickHandler);
    isShown = true;
  },

  // For mobile version:
  // transition section to its close state,
  // remove the global 'closeFormClickHandler' click event handler
  // and unmount the form from DOM
  closeMobileNewsletter: () => {
    narrowMenuContainer.classList.remove("d-none");
    container.classList.remove("faded-in");
    navNewsletter.unmountForm();
    isShown = false;
  },

  // For mobile version:
  // inject a new sign up form then transition section to its expanded state
  expandMobileNewsletter: () => {
    navNewsletter.injectForm();
    narrowMenuContainer.classList.add(`d-none`);
    container.classList.add("faded-in");
    isShown = true;
  },

  // For desktop+ version:
  // create click handler to detect clicking event outside of the newsletter section
  closeFormClickHandler: event => {
    // close newsletter section if clicking anywhere outside of the section
    if (!container.contains(event.target) && event.target !== container) {
      navNewsletter.closeDesktopNewsletter();
    }
  },

  init: (siteUrl, token) => {
    foundationSiteURL = siteUrl;
    csrfToken = token;

    // let newsletterInput = document.getElementById("newsletter-input");

    // For desktop+ version:
    // make 'buttonDesktop' the trigger to open newsletter section
    buttonDesktop.addEventListener("click", event => {
      if (!isShown) {
        event.stopPropagation();
        navNewsletter.expandDesktopNewsletter();
      } else {
        navNewsletter.closeDesktopNewsletter();
      }
    });

    // For mobile version:
    // make 'buttonDismiss' the trigger to close newsletter section
    buttonDismiss.addEventListener("click", () => {
      navNewsletter.closeMobileNewsletter();
    });

    // For mobile version:
    // make 'buttonMobile' the trigger to show newsletter section
    buttonMobile.addEventListener("click", () => {
      navNewsletter.expandMobileNewsletter();
    });
  }
};

export default navNewsletter;
