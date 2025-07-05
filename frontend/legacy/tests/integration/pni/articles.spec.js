const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("../../wait-for-images.js");
const { foundationDomain, pniBaseUrl } = require("../../base-urls.js");

test.describe("PNI articles", () => {
  test(`"load more" button`, async ({ page }) => {
    page.on(`console`, console.log);
    await page.goto(`${pniBaseUrl("en")}/articles`);
    await page.locator(`body.react-loaded`);
    await waitForImagesToLoad(page);

    const articleList = page.locator(`#items-list`);
    expect(await articleList.count()).toEqual(1);

    const articles = articleList.locator(`li`);
    const numArticles = articles.count();
    expect(await numArticles).toBeGreaterThan(1);

    const loadMoreButton = page.locator(
      `#load-more button[data-hx-get][data-hx-push-url]`
    );
    expect(await loadMoreButton.count()).toBe(1);
    expect(await loadMoreButton.isVisible()).toBe(true);

    let getUrl = await loadMoreButton.getAttribute(`data-hx-get`);
    let pushUrl = await loadMoreButton.getAttribute(`data-hx-push-url`);
    // these need to be full URL for the following assertion to work
    getUrl = `${foundationDomain}${getUrl}`;
    pushUrl = `${foundationDomain}${pushUrl}`;

    const requestPromise = page.waitForRequest(getUrl);
    // htmx uses History API to update the URL.
    // Using this function to wait for the URL to change instead of waitForNavigation or waitForUrl
    // ensures our assertion below happens after the URL has been updated.
    const pushPromise = page.waitForFunction(
      (expectedUrl) => window.location.href === expectedUrl,
      pushUrl
    );
    await loadMoreButton.click();
    await requestPromise;
    await pushPromise;

    // The number of articles should increase
    expect(await articles.count()).toBeGreaterThan(await numArticles);
  });
});
