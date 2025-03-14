import { set } from "react-ga";

/**
 * ExternalLinks object for handling external links.
 */
const ExternalLinks = {
  /**
   * Initializes the ExternalLinks object.
   */
  init() {
    this.configure();
  },
  /**
   * Set up the event handlers for the external links.
   */
  configure() {
    document
      .querySelectorAll(
        `a[href^="http"]:not([href*="${window.location.host}"]):not([href^="mailto:"])`
      )
      .forEach((link) => {
        link.target = "_blank";
        link.rel = "noopener noreferrer";
      });
  },
};

export default ExternalLinks;
