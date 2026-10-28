import { beforeAll, beforeEach, describe, expect, it } from "vitest";

let ListLimitController;

beforeAll(async () => {
  window.StimulusModule = { Controller: class {} };
  ({ default: ListLimitController } =
    await import("./list_limit_controller.js"));
});

// Mirrors Wagtail's list markup: an add button before each item and one after
// the last. Deleting an item marks it and the add button before it aria-hidden.
function item({ deleted = false } = {}) {
  const hidden = deleted ? 'aria-hidden="true"' : "";
  return `
    <button type="button" data-streamfield-list-add ${hidden}></button>
    <div data-streamfield-child ${hidden}>
      <button type="button" data-streamfield-action="DUPLICATE"></button>
      <button type="button" data-streamfield-action="DELETE"></button>
    </div>
  `;
}

function createController(items, { min = 2, max = 4 } = {}) {
  document.body.innerHTML = `
    <div data-controller="list-limit">
      <input type="hidden" data-streamfield-list-count value="${items.length}">
      <div data-streamfield-list-container>
        ${items.join("")}
        <button type="button" data-streamfield-list-add></button>
      </div>
    </div>
  `;

  const controller = new ListLimitController();
  controller.element = document.querySelector("[data-controller]");
  controller.minValue = min;
  controller.maxValue = max;
  controller.connect();
  return controller;
}

const list = () => document.querySelector("[data-streamfield-list-container]");
const liveAddButtons = () => [
  ...document.querySelectorAll(
    "[data-streamfield-list-add]:not([aria-hidden])",
  ),
];
const actionButtons = (action) => [
  ...document.querySelectorAll(
    `[data-streamfield-child]:not([aria-hidden]) [data-streamfield-action='${action}']`,
  ),
];
const counterText = () => document.querySelector("p.help").textContent;

describe("ListLimitController", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
  });

  it("shows how many items the list holds out of its max", () => {
    createController([item(), item(), item()]);

    expect(counterText()).toBe("3 of 4");
  });

  it("hides the add buttons and disables duplicate once the list is full", () => {
    createController([item(), item(), item(), item()]);

    expect(liveAddButtons().every((button) => button.hidden)).toBe(true);
    expect(actionButtons("DUPLICATE").every((button) => button.disabled)).toBe(
      true,
    );
  });

  it("disables delete at the minimum", () => {
    createController([item(), item()]);

    expect(actionButtons("DELETE").every((button) => button.disabled)).toBe(
      true,
    );
    expect(liveAddButtons().some((button) => button.hidden)).toBe(false);
  });

  it("updates when Wagtail adds an item", async () => {
    createController([item(), item(), item()]);

    list().insertAdjacentHTML("beforeend", item());
    await Promise.resolve();

    expect(counterText()).toBe("4 of 4");
    expect(liveAddButtons().every((button) => button.hidden)).toBe(true);
  });

  it("updates when Wagtail deletes an item from a full list", async () => {
    createController([item(), item(), item(), item()]);

    const deleted = list().querySelectorAll("[data-streamfield-child]")[3];
    deleted.previousElementSibling.setAttribute("aria-hidden", "true");
    deleted.setAttribute("aria-hidden", "true");
    await Promise.resolve();

    expect(counterText()).toBe("3 of 4");
    expect(liveAddButtons().some((button) => button.hidden)).toBe(false);
    expect(deleted.previousElementSibling.hidden).toBe(true);
  });

  it("does not count deleted items", () => {
    createController([item(), item(), item(), item({ deleted: true })]);

    expect(counterText()).toBe("3 of 4");
  });

  it("removes its counter on disconnect", () => {
    const controller = createController([item(), item()]);

    controller.disconnect();

    expect(document.querySelector("p.help")).toBeNull();
  });
});
