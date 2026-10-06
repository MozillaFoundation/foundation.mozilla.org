import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  initAccordionItem,
  initAllAccordionBlocks,
} from "./accordion_block.js";

const ROW = `
  <details class="mzf-c-accordion-item">
    <summary class="mzf-c-accordion-item__summary">
      <span class="mzf-c-accordion-item__title">
        <span class="mzf-c-accordion-item__label">Row</span>
      </span>
      <span class="mzf-c-accordion-item__expand" aria-hidden="true"></span>
    </summary>
    <div class="mzf-c-accordion-item__reveal">
      <div class="mzf-c-accordion-item__description"><p>Body</p></div>
    </div>
  </details>
`;

function createAccordion(rows = 2, groups = 1) {
  const group = `
    <div class="mzf-c-accordion-group">
      <div class="mzf-c-accordion-group__items">${ROW.repeat(rows)}</div>
    </div>
  `;
  document.body.innerHTML = group.repeat(groups);

  return [...document.querySelectorAll(".mzf-c-accordion-item")].map(
    (details) => {
      const summary = details.querySelector(".mzf-c-accordion-item__summary");
      const reveal = details.querySelector(".mzf-c-accordion-item__reveal");
      Object.defineProperty(reveal, "scrollHeight", { value: 120 });
      return { details, summary, reveal };
    },
  );
}

function click(summary) {
  const event = new MouseEvent("click", { bubbles: true, cancelable: true });
  summary.dispatchEvent(event);
  return event;
}

function dispatchTransitionEnd(element, propertyName = "height") {
  const event = new Event("transitionend", { bubbles: true });
  Object.defineProperty(event, "propertyName", { value: propertyName });
  element.dispatchEvent(event);
}

function stubReducedMotion(matches) {
  vi.stubGlobal(
    "matchMedia",
    vi.fn(() => ({ matches })),
  );
}

describe("accordion rows", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    stubReducedMotion(false);
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn((callback) => callback()),
    );
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
  });

  it("opens a closed row by animating the reveal to its content height", () => {
    const [{ details, summary, reveal }] = createAccordion();
    initAllAccordionBlocks();

    const event = click(summary);

    // The script takes over the native toggle so it can animate.
    expect(event.defaultPrevented).toBe(true);
    expect(details.open).toBe(true);
    expect(details.classList).toContain("mzf-c-accordion-item--expanding");
    expect(reveal.style.height).toBe("120px");

    dispatchTransitionEnd(reveal);

    expect(details.open).toBe(true);
    expect(details.classList).not.toContain("mzf-c-accordion-item--expanding");
    expect(reveal.style.height).toBe("");
  });

  it("keeps an open row open until the close animation finishes", () => {
    const [{ details, summary, reveal }] = createAccordion();
    initAllAccordionBlocks();
    details.open = true;

    click(summary);

    // [open] stays set while the height animates to 0, so the copy stays visible.
    expect(details.open).toBe(true);
    expect(details.classList).toContain("mzf-c-accordion-item--collapsing");
    expect(reveal.style.height).toBe("0px");

    dispatchTransitionEnd(reveal);

    expect(details.open).toBe(false);
    expect(details.classList).not.toContain("mzf-c-accordion-item--collapsing");
    expect(reveal.style.height).toBe("");
  });

  it("ignores clicks while a row is closing", () => {
    const [{ details, summary, reveal }] = createAccordion();
    initAllAccordionBlocks();
    details.open = true;
    click(summary);

    const event = click(summary);

    expect(event.defaultPrevented).toBe(true);
    expect(details.classList).toContain("mzf-c-accordion-item--collapsing");

    dispatchTransitionEnd(reveal);

    expect(details.open).toBe(false);
  });

  it("closes a row that is still opening, settling the open first", () => {
    const [{ details, summary, reveal }] = createAccordion();
    initAllAccordionBlocks();

    click(summary);
    click(summary);

    expect(details.classList).not.toContain("mzf-c-accordion-item--expanding");
    expect(details.classList).toContain("mzf-c-accordion-item--collapsing");

    dispatchTransitionEnd(reveal);

    expect(details.open).toBe(false);
  });

  it("finishes on a timeout when transitionend never fires", () => {
    const [{ details, summary }] = createAccordion();
    initAllAccordionBlocks();

    click(summary);
    vi.advanceTimersByTime(500 + 48);

    expect(details.classList).not.toContain("mzf-c-accordion-item--expanding");
  });

  it("only finishes on the reveal's own height transition", () => {
    const [{ details, summary, reveal }] = createAccordion();
    initAllAccordionBlocks();

    click(summary);
    dispatchTransitionEnd(reveal, "opacity");
    dispatchTransitionEnd(reveal.firstElementChild);

    expect(details.classList).toContain("mzf-c-accordion-item--expanding");

    dispatchTransitionEnd(reveal);

    expect(details.classList).not.toContain("mzf-c-accordion-item--expanding");
  });

  it("closes the open row in the same group when another opens", () => {
    const [first, second] = createAccordion();
    initAllAccordionBlocks();

    click(first.summary);
    dispatchTransitionEnd(first.reveal);
    click(second.summary);

    // The first row closes with its own animation while the second opens.
    expect(first.details.classList).toContain(
      "mzf-c-accordion-item--collapsing",
    );
    expect(second.details.open).toBe(true);

    dispatchTransitionEnd(first.reveal);
    dispatchTransitionEnd(second.reveal);

    expect(first.details.open).toBe(false);
    expect(second.details.open).toBe(true);
  });

  it("closes a row that is still opening when another opens", () => {
    const [first, second] = createAccordion();
    initAllAccordionBlocks();

    click(first.summary);
    click(second.summary);

    expect(first.details.classList).not.toContain(
      "mzf-c-accordion-item--expanding",
    );
    expect(first.details.classList).toContain(
      "mzf-c-accordion-item--collapsing",
    );
  });

  it("leaves rows in other accordion groups open", () => {
    const [first, , third] = createAccordion(2, 2);
    initAllAccordionBlocks();

    click(first.summary);
    dispatchTransitionEnd(first.reveal);
    click(third.summary);
    dispatchTransitionEnd(third.reveal);

    expect(first.details.open).toBe(true);
    expect(third.details.open).toBe(true);
  });

  it("leaves the toggle to the browser when reduced motion is on", () => {
    stubReducedMotion(true);
    const [{ details, summary, reveal }] = createAccordion();
    initAllAccordionBlocks();

    const event = click(summary);

    expect(event.defaultPrevented).toBe(false);
    expect(details.classList).not.toContain("mzf-c-accordion-item--expanding");
    expect(reveal.style.height).toBe("");
  });

  it("closes the open row instantly when reduced motion is on", () => {
    stubReducedMotion(true);
    const [first, second] = createAccordion();
    initAllAccordionBlocks();
    second.details.open = true;

    click(first.summary);

    expect(second.details.open).toBe(false);
    expect(second.details.classList).not.toContain(
      "mzf-c-accordion-item--collapsing",
    );
  });

  it("wires each row only once", () => {
    const [{ details, summary }] = createAccordion(1);
    initAllAccordionBlocks();
    initAllAccordionBlocks();

    click(summary);

    // A second listener would see the row already open and start closing it.
    expect(details.classList).toContain("mzf-c-accordion-item--expanding");
    expect(details.classList).not.toContain("mzf-c-accordion-item--collapsing");
  });

  it("skips a row that is missing its reveal", () => {
    const [{ details, summary, reveal }] = createAccordion(1);
    reveal.remove();
    initAccordionItem(details);

    const event = click(summary);

    expect(event.defaultPrevented).toBe(false);
  });
});
