import { gsap } from "gsap";
let tl = gsap.timeline({ paused: true });

/**
 * Animating buttons in the "Share this" section of the youtube regrets reporter extension landing page.
 * Uses GSAP to provide the animations.
 */

class regretsReporterShareButtons {
  constructor() {
    this.shareButtonsActive = false;
    this.bindEvents();
    this.buildTimeLine();
  }

  bindEvents() {
    const shareDisplayButton = document.getElementById("share-display-button");
    const shareFacebookButton = document.getElementById("share-fb-button");
    const shareTwitterButton = document.getElementById("share-twitter-button");
    const shareEmailButton = document.getElementById("share-email-button");
    const shareLinkButton = document.getElementById("share-link-button");

    shareDisplayButton.addEventListener("click", () => {
      if (!tl.isActive()) {
        this.updateShareButtons();
      }
    });

    shareFacebookButton.addEventListener("click", (e) => {
      this.shareButtonClicked(e, "share-progress-fb");
    });

    shareTwitterButton.addEventListener("click", (e) => {
      this.shareButtonClicked(e, "share-progress-tw");
    });

    shareEmailButton.addEventListener("click", (e) => {
      this.shareButtonClicked(e, "share-progress-em");
    });

    shareLinkButton.addEventListener("click", (e) => {
      this.shareButtonClicked(e);
    });
  }

  buildTimeLine() {
    tl.to("#share-display-text", {
      autoAlpha: 0,
      duration: 0,
    });
    tl.set("#share-display-text", { display: "none" });
    tl.set(".btn-share", { display: "block" });
    tl.fromTo(
      ".btn-share",
      { y: 10, autoAlpha: 0 },
      {
        autoAlpha: 1,
        stagger: 0.1,
        duration: 0.5,
        ease: "bounce.out",
        y: 0,
      }
    );
  }

  // Clicks the hidden Shareprogress buttons on extension_hero.html,
  // or copies URL to clipboard.
  shareButtonClicked(event, shareProgressButtonId) {
    if (shareProgressButtonId) {
      let shareProgressButton = document.querySelector(
        `#${shareProgressButtonId} a`
      );

      if (shareProgressButton) {
        shareProgressButton.click();
      }
    } else {
      navigator.clipboard.writeText(window.location.href);
      event.target.classList.remove("before:tw-bg-[url('../_images/youtube-regrets/regrets-reporter/landing-page/share-link.svg')]");
      event.target.classList.add("before:tw-bg-[url('../_images/youtube-regrets/regrets-reporter/landing-page/share-link-copied.svg')]");      
    }
  }

  updateShareButtons() {
    if (this.shareButtonsActive) {
      this.hideShareButtons();
    } else {
      this.displayShareButtons();
    }
    this.shareButtonsActive = !this.shareButtonsActive;
  }

  // Display share buttons and hide "Share This" text
  displayShareButtons() {
    // Callback is to remove the tw-hidden class from the share buttons, which was added to prevent them being visible while page loads.
    tl.eventCallback('onStart', Array.from(document.querySelectorAll('.btn-share')).forEach((el) => el.classList.remove('tw-hidden')))
    tl.play();
  }

  // Hide share buttons and display "Share This" text
  hideShareButtons() {
    tl.reverse();
  }
}

export default regretsReporterShareButtons;
