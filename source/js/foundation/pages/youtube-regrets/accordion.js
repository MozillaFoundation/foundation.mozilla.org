import {gsap} from "gsap";
import {ScrollToPlugin} from "gsap/all";

gsap.registerPlugin(ScrollToPlugin);

class YoutubeRegretsAccordion {
  constructor(node) {
    this.accordion = node;
    this.openedCard = null;
    this.tabHeight = 174;
    this.cards = [
      ...this.accordion.querySelectorAll("[data-accordion-drawer]"),
    ];
    this.expandableCards = this.cards.map(
      (card, index) =>
        new ExpandableCard(card, index, this.cards.length, this.tabHeight)
    );
    this.totalTabHeight = `${this.expandableCards.length * this.tabHeight}`;
    this.lastCardIndex = this.expandableCards.length - 1;

    // Set height on load
    this.setAccordionHeight();

    this.expandableCards.forEach((card, index) => {
      card.button.addEventListener("click", () => {
        if (!card.isOpen) {
          this.openCard(card, 0.3);
        }
      });

      card.closeButton.addEventListener("click", () => {
        this.expandableCards.forEach((card) => {
          card.openIndex = -1;
          card.close(0.2);
          this.setAccordionHeight();
        });
      });
    });
  }

  openCard(cardInstance = null, speed = 1, scroll = true) {
    this.expandableCards.forEach((card, index) => {
      this.openedCard = cardInstance;
      card.openIndex = cardInstance.index;
      card.openHeight = cardInstance.card.clientHeight;
      if (card === cardInstance) {
        card.open(speed);
        this.setAccordionHeight(card);
        if (scroll) {
          gsap.to(window, speed, {
            scrollTo: {
              y:
                window.pageYOffset +
                this.accordion.getBoundingClientRect().top -
                80 +
                cardInstance.index * cardInstance.tabHeight,
            },
          });
        } else {
          this.openCardComplete();
        }
      } else {
        card.close(0.3);
      }
    });
  }

  closeCards() {
    this.expandableCards.forEach((card, index) => {
      const y = -card.card.clientHeight + card.tabOffset;
      gsap.to(card.card, 0.3, {y: y,})
      gsap.set(card.card, {
        marginTop: 0,
        onComplete: () => {
          card.content.style.visibility = "hidden";
          card.card.classList.remove("open");
          if (card.closeButton) {
            card.closeButton.classList.add("d-none");
          }
        },
      });
      gsap.to(card.button, 0.3, {
        autoAlpha: 1,
      });
      this.setAccordionHeight();
    });
  }

  setAccordionHeight(card) {
    if (card) {
      const tabsTotalHeight =
        (this.expandableCards.length - 1) * this.tabHeight;
      let height = card.openHeight + tabsTotalHeight;
      const heightAmount = `${height}px`;
      gsap.to(this.accordion, 0.2, {height: heightAmount});
    } else {
      gsap.to(this.accordion, 0.2, {height: this.totalTabHeight + 'px'});
    }
  }
}

class ExpandableCard {
  constructor(node, index, length, tabHeight) {
    this.card = node;
    this.index = index;
    this.openIndex = -1;
    this.openHeight = 0;
    this.button = this.card.querySelector("[data-accordion-button]");
    this.closeButton = this.card.querySelector("[data-accordion-close-button]");
    this.content = this.card.querySelector("[data-accordion-content]");
    this.maskEl = this.card.querySelector("[data-expand-mask]");
    this.card.style.zIndex = length - index;
    this.tabHeight = tabHeight;
    this.isOpen = false;
    this.initEventListeners();
    this.tabOffset = (this.index + 1) * this.tabHeight;

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
    this.content.classList.remove("invisible");

    if (this.closeButton) {
      this.closeButton.classList.remove("d-none");
    }

    gsap.to(this.maskEl, 0.25, {y: 0});
    gsap.to(this.card, speed, {
      y: y,
      onComplete: () => {
        this.card.classList.add("open");
        gsap.set(this.card, {y: 0, marginTop: y});
      },
    });
    gsap.to(this.content, speed, {
      autoAlpha: 1,
    });
    gsap.to(this.button, speed, {
      autoAlpha: 0,
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
    // If the card is below the current open card set the y transform accordion to the openHeight
    if (this.openIndex > -1 && this.index > this.openIndex) {
      y += this.openHeight - this.tabHeight;
    }

    gsap.to(this.card, speed, {
      y: y,
      onComplete: () => {
        this.content.classList.add("invisible");
        this.card.classList.remove("open");
        if (this.closeButton) {
          this.closeButton.classList.add("d-none");
        }
      },
    });
    gsap.to(this.content, speed, {autoAlpha: 0});
    gsap.to(this.button, speed, {
      autoAlpha: 1,
    });
  }
}

export const initYoutubeRegretsAccordions = () => {
  const accordions = [...document.querySelectorAll("#yt-regrets-accordion")];
  accordions.map((accordion) => new YoutubeRegretsAccordion(accordion));
};

export default YoutubeRegretsAccordion;
