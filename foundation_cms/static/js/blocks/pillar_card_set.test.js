import { describe, it, expect, vi, beforeEach } from "vitest";
import { initPillarCardLinks } from "./pillar_card_set.js";

describe("initPillarCardLinks", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
  });

  it("sets a pointer cursor on matching cards", () => {
    document.body.innerHTML = `<div class="pillar-card-set__card" data-href="/example"></div>`;

    initPillarCardLinks();

    const card = document.querySelector(".pillar-card-set__card");
    expect(card.style.cursor).toBe("pointer");
  });

  it("opens the href in a new tab when data-target is _blank", () => {
    document.body.innerHTML = `
      <div class="pillar-card-set__card" data-href="/example" data-target="_blank"></div>
    `;
    const card = document.querySelector(".pillar-card-set__card");
    const openSpy = vi.spyOn(window, "open").mockImplementation(() => {});

    initPillarCardLinks();
    card.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(openSpy).toHaveBeenCalledWith(
      "/example",
      "_blank",
      "noopener,noreferrer",
    );

    openSpy.mockRestore();
  });

  // Ensure we don't have a double-navigate problem: a click on the inner
  // link bubbles to the card's own listener, which would otherwise navigate
  // again. See the `e.target.closest(...)` guard in pillar_card_set.js.
  it("does not navigate when the click originates from the nested link", () => {
    document.body.innerHTML = `
      <div class="pillar-card-set__card" data-href="/example" data-target="_blank">
        <a class="pillar-card-set__card-link" href="#">Read more</a>
      </div>
    `;
    const link = document.querySelector(".pillar-card-set__card-link");
    const openSpy = vi.spyOn(window, "open").mockImplementation(() => {});

    initPillarCardLinks();
    link.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(openSpy).not.toHaveBeenCalled();

    openSpy.mockRestore();
  });
});
