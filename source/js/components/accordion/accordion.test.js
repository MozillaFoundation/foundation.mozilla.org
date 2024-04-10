import Accordion from "./accordion";

describe("Accordion", () => {
  /* eslint-disable no-new */

  beforeEach(() => {
    document.body.innerHTML = `
            <div class="accordion" data-accordion>
                <a class="accordion__title" data-accordion-title aria-expanded="false" tabindex="0">What goes on and on and has an i in the middle?</a>
                <div class="accordion__content" data-accordion-content aria-hidden="true">
                    An Onion
                </div>
            </div>
        `;
  });

  it("does not show the content by default", () => {
    new Accordion(document.querySelector(Accordion.selector()));
    expect(
      document
        .querySelector("[data-accordion-content]")
        .getAttribute("aria-hidden")
    ).toBe("true");
  });

  it("shows the content when the title is clicked", () => {
    new Accordion(document.querySelector(Accordion.selector()));

    const title = document.querySelector("[data-accordion-title]");

    title.dispatchEvent(new Event("click"));
    expect(
      document
        .querySelector("[data-accordion-content]")
        .getAttribute("aria-hidden")
    ).toBe("false");
  });

  it("hides the content when the title is clicked if already open", () => {
    new Accordion(document.querySelector(Accordion.selector()));

    const title = document.querySelector("[data-accordion-title]");

    title.dispatchEvent(new Event("click"));
    expect(
      document
        .querySelector("[data-accordion-content]")
        .getAttribute("aria-hidden")
    ).toBe("false");

    title.dispatchEvent(new Event("click"));
    expect(
      document
        .querySelector("[data-accordion-content]")
        .getAttribute("aria-hidden")
    ).toBe("true");
  });
});
