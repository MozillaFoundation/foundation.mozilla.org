import { afterEach, expect, it } from "vitest";

import { initExpertProfileArticleList } from "./article_list";

afterEach(() => {
  document.body.innerHTML = "";
});

it("collapses overflow before revealing the initialized control", () => {
  document.body.innerHTML = `
    <section class="expert-profile-section--articles">
      <ul data-expert-profile-article-list data-visible-count="2">
        <li>CMS one</li>
        <li class="expert-profile-article-list__manual">Manual two</li>
        <li>CMS three</li>
      </ul>
      <button data-expert-profile-show-articles hidden>Show more</button>
    </section>
  `;

  const items = document.querySelectorAll("li");
  const button = document.querySelector("button");
  expect(Array.from(items).every((item) => item.hidden === false)).toBe(true);
  expect(button.hidden).toBe(true);

  initExpertProfileArticleList();

  expect(items[2].hidden).toBe(true);
  expect(button.hidden).toBe(false);

  button.click();
  expect(items[2].hidden).toBe(false);
  expect(button.hidden).toBe(true);
});

it("keeps an unnecessary control hidden for a short list", () => {
  document.body.innerHTML = `
    <section class="expert-profile-section--articles">
      <ul data-expert-profile-article-list data-visible-count="3">
        <li>CMS one</li>
        <li>Manual two</li>
      </ul>
      <button data-expert-profile-show-articles hidden>Show more</button>
    </section>
  `;

  initExpertProfileArticleList();

  expect(
    Array.from(document.querySelectorAll("li")).every(
      (item) => item.hidden === false,
    ),
  ).toBe(true);
  expect(document.querySelector("button").hidden).toBe(true);
});
