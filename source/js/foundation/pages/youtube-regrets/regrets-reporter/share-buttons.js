import { gsap } from "gsap";
let tl = gsap.timeline();

class regretsReporterShareButtons {
  constructor() {
    this.shareButtonsActive = false;
    this.bindEvents();
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
      event.target.classList.add(`copied`);
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

  // Hide share buttons and display "Share This" text
  hideShareButtons() {
    tl.fromTo(
      ".btn-share",
      {
        autoAlpha: 1,
        y: 0,
      },
      {
        y: 10,
        autoAlpha: 0,
        stagger: -0.1,
        duration: 0.4,
      }
    );
    tl.set(".btn-share", { display: "none" });
    tl.set("#share-display-text", { display: "block" });
    tl.to("#share-display-text", {
      autoAlpha: 1,
      duration: 0.1,
    });
  }
}

export default regretsReporterShareButtons;
