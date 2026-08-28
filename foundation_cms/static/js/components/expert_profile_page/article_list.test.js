import { afterEach, expect, it } from "vitest";

import { initExpertProfileArticleList } from "./article_list";

afterEach(() => {
  document.body.innerHTML = "";
});

it("reveals mixed CMS and manual article rows within its section", () => {
  document.body.innerHTML = `
    <section class="expert-profile-section--articles">
      <ul data-expert-profile-article-list data-visible-count="2">
        <li>CMS one</li>
        <li class="expert-profile-article-list__manual">Manual two</li>
        <li>CMS three</li>
      </ul>
      <button data-expert-profile-show-articles>Show more</button>
    </section>
  `;

  initExpertProfileArticleList();

  const items = document.querySelectorAll("li");
  const button = document.querySelector("button");
  expect(items[2].hidden).toBe(true);

  button.click();
  expect(items[2].hidden).toBe(false);
  expect(button.hidden).toBe(true);
});
