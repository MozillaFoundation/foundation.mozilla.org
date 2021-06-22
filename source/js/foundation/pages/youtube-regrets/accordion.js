import {gsap} from "gsap";

class YoutubeRegretsAccordion {
  constructor(node) {
    this.accordion = node;
    this.openedCard;
    this.cards = [
      ...this.accordion.querySelectorAll("[data-accordion-drawer]"),
    ];
    this.expandableCards = this.cards.map(
      (card, index) => new ExpandableCard(card, index, this.cards.length)
    );

    this.expandableCards.forEach((card, index) => {
      if (this.openedCard) {
        card.openHeight = this.openedCard.element.clientHeight;
      }
      card.button.addEventListener('click', () => {
        if (!card.isOpen){
          this.openCard(card)
        }
      })
    });
  }

  openCard(cardInstance = null, speed = 1, scroll = true) {
    this.expandableCards.forEach((card, index) => {
      this.openedCard = cardInstance;
      card.openIndex = cardInstance.index;
      card.openHeight = cardInstance.card.clientHeight;
      if (card == cardInstance) {
        card.open(speed);
      } else {
        card.close();
      }
    });
  }
}

class ExpandableCard {
  constructor(node, index, length) {
    this.card = node;
    this.index = index;
    this.openIndex = -1;
    this.button = this.card.querySelector("[data-accordion-button]");
    this.content = this.card.querySelector("[data-accordion-content]");
    this.maskEl = this.card.querySelector("[data-expand-mask]");
    this.card.style.zIndex = length - index;
    this.tabHeight = 174;
    this.isOpen = false;

    this.content.style.visibility = "hidden";

    this.initEventListeners();

    this.tabOffset = ((this.index + 1) * this.tabHeight);
    if (this.isOpen) {
      this.open(0);
    } else {
      this.close(0);
    }
  }

  initEventListeners() {
    this.button.addEventListener("click", (e) => {
      this.card.setAttribute("aria-expanded", "true");
    });

    this.card.addEventListener("mouseenter", (e) => {
      gsap.to(this.maskEl, 0.3, {y: 10});
    });
    this.card.addEventListener("mouseleave", (e) => {
      gsap.to(this.maskEl, 0.3, {y: 0});
    });
  }

  open(speed = 1) {
    this.isOpen = true;
    const tabsAboveHeight =
      (this.index - (this.openIndex + 1)) * this.tabHeight;
    const y = tabsAboveHeight + this.tabOffset;
    this.content.style.visibility = "visible";
    gsap.to(this.maskEl, 0.25, {y: 0});
    gsap.to(this.card, speed, {
      y: y,
      ease: "Power4.easeInOut",
      onComplete: () => {
        this.card.classList.add("open");
        gsap.set(this.card, {y: 0, marginTop: y});
      },
    });

    gsap.to(this.content, 0.2, {
      autoAlpha: 1,
      delay: speed === 0 ? 0 : 0.5,
    });
  }

  close(speed = 1) {
    if (this.isOpen) {
      gsap.set(this.card, {
        marginTop: 0,
        y: parseInt(this.card.style.marginTop, 10),
      });
    }
    this.isOpen = false;
    let y = -this.card.clientHeight + this.tabOffset;
    if (this.openIndex > -1 && this.index > this.openIndex) {
      y += this.openHeight - this.tabHeight;
    }
    gsap.to(this.card, speed, {
      y: y,
      ease: "Power4.easeInOut",
      onComplete: () => {
        this.content.style.visibility = "hidden";
        this.card.classList.remove("open");
      },
    });
    gsap.to(this.content, 0.2, { autoAlpha: 0 });
  }
}

export const initYoutubeRegretsAccordions = () => {
  const accordions = [...document.querySelectorAll("#yt-regrets-accordion")];
  accordions.map((accordion) => new YoutubeRegretsAccordion(accordion));
};

export default YoutubeRegretsAccordion;
