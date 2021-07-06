import { gsap } from "gsap";
import { ScrollToPlugin } from "gsap/all";

gsap.registerPlugin(ScrollToPlugin);

class ReadMoreCategories {
  constructor(node) {
    this.readMore = node;
    this.toggleButton = this.readMore.querySelector(
      "[data-yt-categories-toggle]"
    );
    this.readMoreText = this.readMore.querySelector(
      "[data-yt-categories-toggle-more]"
    );
    this.readLessText = this.readMore.querySelector(
      "[data-yt-categories-toggle-less]"
    );
    this.plusIcon = this.readMore.querySelector(
      "[data-yt-categories-plus-icon]"
    );
    this.minusIcon = this.readMore.querySelector(
      "[data-yt-categories-minus-icon]"
    );
    this.content = this.readMore.querySelector("[data-yt-categories-reveal]");
    this.animateSpeed = 0.5;

    this.bindEvents();
  }

  bindEvents() {
    this.toggleButton.addEventListener("click", () => {
      if (this.content.classList.contains("is-open")) {
        this.handleClose();
      } else {
        this.handleOpen();
      }
    });
  }

  handleOpen() {
    this.content.classList.add("is-open");
    this.readMoreText.classList.add("d-none");
    this.readLessText.classList.remove("d-none");
    this.plusIcon.classList.add("d-none");
    this.minusIcon.classList.remove("d-none");

    let timeline = gsap.timeline();

    timeline.to(this.content, { duration: this.animateSpeed, height: "auto" });
  }

  handleClose() {
    this.content.classList.remove("is-open");
    this.readMoreText.classList.remove("d-none");
    this.readLessText.classList.add("d-none");
    this.plusIcon.classList.add("d-none");
    this.minusIcon.classList.remove("d-none");

    let timeline = gsap.timeline();

    timeline.to(this.content, { duration: this.animateSpeed, height: "0px" });
  }
}

export const initYoutubeRegretsReadMoreCategories = () => {
  const categories = [...document.querySelectorAll("[data-yt-categories]")];
  categories.map((category) => new ReadMoreCategories(category));
};

export default ReadMoreCategories;
