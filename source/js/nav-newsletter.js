import React from "react";
import ReactGA from "react-ga";
import ReactDOM from "react-dom";
import JoinUs from "./components/join/join.jsx";

let isShown = false;
let navNewsletter = {
  init: function(env, networkSiteURL, csrfToken) {
    let primaryNav = document.querySelector(`#primary-nav-container`);
    let narrowMenuContainer = primaryNav.querySelector(
      ".narrow-screen-menu-container"
    );
    let wideMenuContainer = primaryNav.querySelector(
      ".wide-screen-menu-container"
    );
    let container = document.querySelector("#nav-newsletter-form-wrapper");
    let buttonDesktop = wideMenuContainer.querySelector(".btn-newsletter");
    let buttonMobile = narrowMenuContainer.querySelector(".btn-newsletter");
    let joinUs = container.querySelector(`.join-us.on-nav`);
    let buttonDismiss = container.querySelector(".form-dismiss");
    // let newsletterInput = document.getElementById("newsletter-input");

    // Inject a new <JoinUs> component each time so we can show <JoinUs> with its initial state
    function injectForm() {
      if (joinUs) {
        var props = joinUs.dataset;

        props.apiUrl = `${networkSiteURL}/api/campaign/signups/${props.signupId ||
          0}/`;

        props.csrfToken = props.csrfToken || csrfToken;
        props.isHidden = false;

        ReactDOM.render(<JoinUs {...props} />, joinUs);
      }
    }

    // We can't simply reset the form as we don't
    // have access to trigger <JoinUs> React component's state or lifecycle.
    // Instead, we unmount <JoinUs> from DOM.
    function unmountForm() {
      // unmount form after newsletter section has transitioned back to the previous view
      let handleTransitionend = () => {
        container.removeEventListener("transitionend", handleTransitionend);
        ReactDOM.unmountComponentAtNode(container.querySelector(".join-us"));
      };
      container.addEventListener("transitionend", handleTransitionend);
    }

    // For desktop+ version:
    // create click handler to detect clicking event outside of the newsletter section
    let closeFormClickHandler = event => {
      // close newsletter section if clicking anywhere outside of the section
      if (!container.contains(event.target) && event.target !== container) {
        closeDesktopNewsletter();
      }
    };

    // For desktop+ version:
    // transition section to its close state,
    // remove the global 'closeFormClickHandler' click event handler
    // and unmount the form from DOM
    function closeDesktopNewsletter() {
      container.classList.remove("expanded");
      buttonDesktop.classList.remove("active");
      document.removeEventListener("click", closeFormClickHandler);
      unmountForm();
      isShown = false;
    }

    // For desktop+ version:
    // inject a new sign up form then transition section to its expanded state
    function expandDesktopNewsletter() {
      injectForm();
      container.classList.add("expanded");
      buttonDesktop.classList.add("active");
      document.addEventListener(`click`, closeFormClickHandler);
      isShown = true;
    }

    // For desktop+ version:
    // make 'buttonDesktop' the trigger to open newsletter section
    buttonDesktop.addEventListener("click", event => {
      if (!isShown) {
        event.stopPropagation();

        expandDesktopNewsletter();
      } else {
        closeDesktopNewsletter();
      }
    });

    // For mobile version:
    // transition section to its close state,
    // remove the global 'closeFormClickHandler' click event handler
    // and unmount the form from DOM
    function closeMobileNewsletter() {
      narrowMenuContainer.classList.remove("d-none");
      container.classList.remove("faded-in");
      unmountForm();
      isShown = false;
    }

    // For mobile version:
    // inject a new sign up form then transition section to its expanded state
    function expandMobileNewsletter() {
      injectForm();
      narrowMenuContainer.classList.add(`d-none`);
      container.classList.add("faded-in");
      isShown = true;
    }

    // For mobile version:
    // make 'buttonDismiss' the trigger to close newsletter section
    buttonDismiss.addEventListener("click", () => {
      closeMobileNewsletter();
    });

    // For mobile version:
    // make 'buttonMobile' the trigger to show newsletter section
    buttonMobile.addEventListener("click", () => {
      expandMobileNewsletter();
    });
  }
};

export default navNewsletter;
