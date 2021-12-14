import { gsap } from "gsap";
let tl = gsap.timeline();

class regretsReporterShareButtons {
  constructor() {
    this.shareButtonsActive = false;
    this.bindEvents();
  }

  bindEvents() {
    const shareDisplayButton = document.getElementById("share-display-button");

    shareDisplayButton.addEventListener("click", () => {
      if (!tl.isActive()) {
        this.updateShareButtons();
      }
    });
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
      display: "none",
      opacity: 0,
      duration: 0,
    });
    tl.fromTo(
      ".btn-share",
      { y: 10, opacity: 0, display: "none" },
      {
        opacity: 1,
        display: "block",
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
        opacity: 1,
        display: "block",
        y: 0,
      },
      {
        y: 10,
        display: "none",
        opacity: 0,
        stagger: -0.1,
        duration: 0.4,
      }
    );
    tl.to("#share-display-text", {
      display: "block",
      opacity: 1,
      duration: 0.1,
    });
  }
}

export default regretsReporterShareButtons;
