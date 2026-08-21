import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AccordionBlock, initAllAccordionBlocks } from "./accordion_block.js";

function createAccordion() {
  document.body.innerHTML = `
    <div class="accordion-block__items">
      <div class="accordion-item">
        <button
          class="accordion-item__button"
          aria-controls="first-panel"
          aria-expanded="true"
        >
          First
        </button>
        <div
          id="first-panel"
          class="accordion-item__panel"
          style="height: auto"
        ></div>
      </div>
      <div class="accordion-item">
        <button class="accordion-item__button" aria-expanded="false">
          Second
        </button>
        <div class="accordion-item__panel" hidden></div>
      </div>
      <button
        class="accordion-item__button accordion-item__button--missing"
        aria-expanded="false"
      >
        Missing panel
      </button>
    </div>
  `;

  const root = document.querySelector(".accordion-block__items");
  const triggers = root.querySelectorAll(".accordion-item__button");
  const panels = root.querySelectorAll(".accordion-item__panel");

  Object.defineProperty(panels[0], "scrollHeight", { value: 120 });
  Object.defineProperty(panels[1], "scrollHeight", { value: 80 });

  return { root, triggers, panels };
}

function dispatchTransitionEnd(element, propertyName = "height") {
  const event = new Event("transitionend", { bubbles: true });
  Object.defineProperty(event, "propertyName", { value: propertyName });
  element.dispatchEvent(event);
}

describe("AccordionBlock", () => {
  beforeEach(() => {
    vi.stubGlobal("CSS", { escape: vi.fn((value) => value) });
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn((callback) => callback()),
    );
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
  });

  it("finds panels by aria-controls or the surrounding accordion item", () => {
    const { root, triggers, panels } = createAccordion();
    const accordion = new AccordionBlock(root);

    expect(accordion.getPanelForTrigger(triggers[0])).toBe(panels[0]);
    expect(accordion.getPanelForTrigger(triggers[1])).toBe(panels[1]);
    expect(accordion.getPanelForTrigger(triggers[2])).toBeUndefined();
  });

  it("initializes panels and switches the expanded item on click", () => {
    const { root, triggers, panels } = createAccordion();
    const accordion = new AccordionBlock(root);

    accordion.init();
    triggers[1].click();

    expect(panels[0].style.transition).toBe("height 300ms ease-in-out");
    expect(panels[1].style.transition).toBe("height 300ms ease-in-out");
    expect(triggers[0].getAttribute("aria-expanded")).toBe("false");
    expect(panels[0].style.height).toBe("0px");
    expect(triggers[1].getAttribute("aria-expanded")).toBe("true");
    expect(panels[1].hidden).toBe(false);
    expect(panels[1].style.height).toBe("80px");

    dispatchTransitionEnd(panels[0]);
    dispatchTransitionEnd(panels[1]);

    expect(panels[0].hidden).toBe(true);
    expect(panels[1].style.height).toBe("auto");

    triggers[1].click();
    dispatchTransitionEnd(panels[1]);

    expect(triggers[1].getAttribute("aria-expanded")).toBe("false");
    expect(panels[1].hidden).toBe(true);
  });

  it("leaves panels unchanged when they already have the requested state", () => {
    const { root, triggers, panels } = createAccordion();
    const accordion = new AccordionBlock(root);
    accordion.openAccordion(triggers[0], panels[0]);
    accordion.closeAccordion(triggers[1], panels[1]);

    expect(requestAnimationFrame).not.toHaveBeenCalled();
    expect(panels[0].style.height).toBe("auto");
    expect(panels[1].hidden).toBe(true);
  });

  it("only completes height transitions dispatched by the panel itself", () => {
    const { root, triggers, panels } = createAccordion();
    const accordion = new AccordionBlock(root);
    const child = document.createElement("span");
    panels[1].appendChild(child);

    accordion.openAccordion(triggers[1], panels[1]);
    dispatchTransitionEnd(panels[1], "opacity");
    dispatchTransitionEnd(child);

    expect(panels[1].style.height).toBe("80px");

    dispatchTransitionEnd(panels[1]);

    expect(panels[1].style.height).toBe("auto");
  });

  it("initializes every accordion block on the page", () => {
    const first = createAccordion();
    document.body.insertAdjacentHTML(
      "beforeend",
      `
        <div class="accordion-block__items">
          <div class="accordion-item">
            <button class="accordion-item__button" aria-expanded="false"></button>
            <div class="accordion-item__panel"></div>
          </div>
        </div>
      `,
    );

    initAllAccordionBlocks();

    expect(first.panels[0].style.transition).toBe("height 300ms ease-in-out");
    expect(
      document.querySelectorAll(".accordion-item__panel")[2].style.transition,
    ).toBe("height 300ms ease-in-out");
  });
});
