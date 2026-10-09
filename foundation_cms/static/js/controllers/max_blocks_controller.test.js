import { beforeAll, beforeEach, describe, expect, it } from "vitest";

let MaxBlocksController;

beforeAll(async () => {
  window.StimulusModule = { Controller: class {} };
  ({ default: MaxBlocksController } =
    await import("./max_blocks_controller.js"));
});

const flushMutations = () => new Promise((resolve) => setTimeout(resolve, 0));

function blockMarkup(index, deleted = "") {
  return `
    <div class="child" data-index="${index}">
      <button data-streamfield-action="DUPLICATE"></button>
      <input type="hidden" name="pencil_link-${index}-deleted" value="${deleted}">
    </div>
  `;
}

function createController(max) {
  const element = document.querySelector("[data-root]");
  const controller = new MaxBlocksController();
  controller.element = element;
  controller.maxValue = max;
  controller.connect();
  return controller;
}

const addButtons = () => [
  ...document.querySelectorAll(
    '.c-sf-add-button, [data-streamfield-action="DUPLICATE"]',
  ),
];

describe("MaxBlocksController", () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div data-root>
        <input type="hidden" name="pencil_link-count" value="1">
        <button class="c-sf-add-button"></button>
        <div id="children">${blockMarkup(0)}</div>
        <button class="c-sf-add-button"></button>
      </div>
    `;
  });

  it("hides insert and duplicate buttons when the field is at its maximum", () => {
    createController(1);

    expect(addButtons().every((b) => b.style.display === "none")).toBe(true);
  });

  it("shows insert buttons again once the block is deleted", async () => {
    createController(1);

    const child = document.querySelector(".child");
    child.querySelector("input").value = "1";
    child.classList.add("deleted");
    await flushMutations();

    expect(addButtons().every((b) => b.style.display === "")).toBe(true);
  });

  it("ignores deleted blocks and leaves room below the maximum", () => {
    document.getElementById("children").innerHTML =
      blockMarkup(0, "1") + blockMarkup(1);
    createController(2);

    expect(addButtons().every((b) => b.style.display === "")).toBe(true);
  });

  it("hides insert buttons when a new block reaches the maximum", async () => {
    document.getElementById("children").innerHTML = "";
    createController(1);
    expect(addButtons().every((b) => b.style.display === "")).toBe(true);

    document
      .getElementById("children")
      .insertAdjacentHTML("beforeend", blockMarkup(0));
    await flushMutations();

    expect(addButtons().every((b) => b.style.display === "none")).toBe(true);
  });
});
