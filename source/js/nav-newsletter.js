import React from "react";
import ReactGA from "react-ga";
import ReactDOM from "react-dom";
import JoinUs from "./components/join/join.jsx";

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
      container.removeEventListener("transitionend", handleTransitionend);
      buttonDismiss.textContent = "No thanks";
    };
    container.addEventListener("transitionend", handleTransitionend);
  }

  // For desktop+ version:
  // transition section to its close state,
  // remove the global 'closeFormClickHandler' click event handler
  // and reset the form
  closeDesktopNewsletter(event) {
    container.classList.remove("expanded");
    buttonDesktop.classList.remove("active");
    document.removeEventListener("click", this.closeFormClickHandler);
    document.removeEventListener("scroll", this.closeFormClickHandler);
    this.resetForm();
    this.isShown = false;
  }

  // For desktop+ version:
  // transition newsletter section to its expanded state
  expandDesktopNewsletter(event) {
    container.style.top = `${primaryNav.offsetHeight}px`;
    container.classList.add("expanded");
    buttonDesktop.classList.add("active");
    document.addEventListener(`click`, this.closeFormClickHandler);
    document.addEventListener("scroll", this.closeFormClickHandler);
    this.isShown = true;
  }

  // For mobile version:
  // transition newsletter section to its close state,
  // remove the global 'closeFormClickHandler' click event handler,
  // and reset the form
  closeMobileNewsletter() {
    narrowMenuContainer.classList.remove("d-none");
    container.classList.remove("faded-in");
    this.resetForm();
    this.isShown = false;
  }

  // For mobile version:
  // transition section to its expanded state
  expandMobileNewsletter() {
    narrowMenuContainer.classList.add(`d-none`);
    container.classList.add("faded-in");
    this.isShown = true;
  }

  // For desktop+ version:
  // create click handler to detect clicking event outside of the newsletter section
  closeFormClickHandler(event) {
    // close newsletter section if clicking anywhere outside of the section
    if (!container.contains(event.target) && event.target !== container) {
      navNewsletter.closeDesktopNewsletter();
    }
  }

  init(foundationSiteURL, csrfToken) {
    if (!joinUs) return;

    console.log(`.join-us.on-nav exists`);

    var props = joinUs.dataset;
    props.apiUrl = `${foundationSiteURL}/api/campaign/signups/${props.signupId ||
      0}/`;
    props.csrfToken = props.csrfToken || csrfToken;
    props.isHidden = false;
    this.form = ReactDOM.render(<JoinUs {...props} />, joinUs);

    // For desktop+ version:
    // make 'buttonDesktop' the trigger to open newsletter section
    buttonDesktop.addEventListener("click", event => {
      if (!this.isShown) {
        event.stopPropagation();
        this.expandDesktopNewsletter();
      } else {
        this.closeDesktopNewsletter();
      }
    });

    // For mobile version:
    // make 'buttonDismiss' the trigger to close newsletter section
    buttonDismiss.addEventListener("click", () => {
      this.closeMobileNewsletter();
    });

    // For mobile version:
    // make 'buttonMobile' the trigger to show newsletter section
    buttonMobile.addEventListener("click", () => {
      navNewsletter.expandMobileNewsletter();
    });
  }
}

const navNewsletter = new NavNewsletter();

export default navNewsletter;
