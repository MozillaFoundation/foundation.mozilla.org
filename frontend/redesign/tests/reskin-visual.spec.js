import { test, expect } from "@playwright/test";
import percySnapshot from "@percy/playwright";
import { foundationBaseUrl } from "./base-urls.js";

const runTime = Date.now();

const fixtures = [
  { slug: "visual-regression-empty", title: "Visual regression: empty page" },
  {
    slug: "visual-regression-components",
    title: "Visual regression: components",
  },
];

async function capture(page, name) {
  await page.mouse.move(0, 0);
  await page.evaluate(() => window.scrollTo({ top: 0, behavior: "instant" }));
  await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(0);
  await expect
    .poll(
      () =>
        page.evaluate(() => {
          const nav = document
            .querySelector("nav.primary-nav-ns")
            .getBoundingClientRect();
          const heading = document
            .querySelector(".general-page h1")
            .getBoundingClientRect();
          return heading.top >= nav.bottom;
        }),
      { message: "Navigation must not obscure the page heading" },
    )
    .toBe(true);
  // Each state is exercised at its real viewport before Percy serializes it.
  await percySnapshot(page, name, { widths: [page.viewportSize().width] });
  await page.screenshot({
    path: `tests/screenshots/${runTime}/${name}.png`,
    fullPage: true,
    animations: "disabled",
  });
}

for (const viewport of [
  { name: "desktop", width: 1280, height: 900 },
  { name: "mobile", width: 375, height: 844 },
]) {
  test.describe(`Cosmos reskin ${viewport.name}`, () => {
    test.use({
      viewport: { width: viewport.width, height: viewport.height },
      deviceScaleFactor: 1,
      locale: "en-US",
      timezoneId: "UTC",
      colorScheme: "light",
      reducedMotion: "reduce",
    });

    for (const fixture of fixtures) {
      test(fixture.slug, async ({ page }) => {
        const origin = new URL(foundationBaseUrl()).origin;
        // Exclude third-party widgets/analytics, retaining real first-party
        // markup, styles, scripts, images and fonts. No fixture-body mocking.
        await page.route("**/*", (route) => {
          const request = route.request();
          if (
            request.resourceType() === "script" &&
            new URL(request.url()).origin !== origin
          ) {
            return route.abort();
          }
          return route.continue();
        });
        await page.clock.setFixedTime(new Date("2026-01-15T12:00:00Z"));

        const assetFailures = [];
        const isRequiredAsset = (request) =>
          new URL(request.url()).origin === origin &&
          ["stylesheet", "script", "font", "image"].includes(
            request.resourceType(),
          );
        page.on("requestfailed", (request) => {
          if (isRequiredAsset(request)) assetFailures.push(request.url());
        });
        page.on("response", (response) => {
          if (isRequiredAsset(response.request()) && !response.ok())
            assetFailures.push(response.url());
        });

        const url = `${foundationBaseUrl()}/${fixture.slug}/`;
        const response = await page.goto(url);
        expect(response?.status(), "Fixture must return HTTP 200").toBe(200);
        await expect(page).toHaveURL(url);
        await expect(page).toHaveTitle(new RegExp(fixture.title));
        await expect(page.locator("body")).toHaveAttribute(
          "data-site-type",
          "redesign",
        );
        await expect(page.locator(".general-page h1")).toHaveText(
          fixture.title,
        );
        await expect(page.locator(".hero__wrapper")).toHaveCount(0);
        await expect(page.locator("nav.primary-nav-ns")).toBeVisible();
        await expect(page.locator("footer.site-footer-ns")).toBeVisible();
        await expect(
          page.locator("footer.site-footer-ns a").first(),
        ).toBeVisible();

        await page.locator("footer").scrollIntoViewIfNeeded();
        await page.evaluate(async () => {
          for (const element of [document.body, document.querySelector("h1")]) {
            const style = getComputedStyle(element);
            const faces = await document.fonts.load(
              `${style.fontWeight} ${style.fontSize} ${style.fontFamily}`,
            );
            if (!faces.length)
              throw new Error(`Expected a web font for ${style.fontFamily}`);
          }
          await document.fonts.ready;
          await Promise.all(
            [...document.images]
              .filter((image) => image.getClientRects().length)
              .map((image) => image.decode()),
          );
        });
        await expect(page.locator(".general-page h1")).toHaveCSS(
          "font-family",
          /Mozilla Headline/,
        );
        expect(
          assetFailures,
          "First-party assets must load successfully",
        ).toEqual([]);
        expect(
          await page.evaluate(() => document.documentElement.scrollWidth),
        ).toBeLessThanOrEqual(viewport.width);

        const name = `Cosmos ${fixture.slug} ${viewport.name}`;
        if (fixture.slug === "visual-regression-empty") {
          await expect(
            page.locator(".general-page .streamfield-block-wrapper"),
          ).toHaveCount(0);
          await expect(
            page.locator(".general-page__body > .container"),
          ).toBeEmpty();
          await capture(page, name);
          return;
        }

        const section = page.locator("#visual-components.mzf-c-section");
        await expect(section).toBeVisible();
        // Values are from the ported LP section master (Figma 9470:11913),
        // not sampled from the first screenshot we happen to produce.
        await expect(section).toHaveCSS("display", "grid");
        await expect(section).toHaveCSS(
          "row-gap",
          viewport.name === "mobile" ? "48px" : "72px",
        );
        await expect(section).toHaveCSS(
          "padding-top",
          viewport.name === "mobile" ? "64px" : "200px",
        );
        await expect(section).toHaveCSS(
          "padding-left",
          viewport.name === "mobile" ? "20px" : "148px",
        );
        await expect(
          section.locator('[data-block-type="link_button_block"]'),
        ).toHaveCount(2);
        await expect(
          section.locator("a.link-button.btn-primary"),
        ).toContainText("Explore the empty page");
        await expect(
          section.locator("a.link-button.btn-primary"),
        ).toHaveAttribute("href", "/en/visual-regression-empty/");
        const items = section.locator("details.mzf-c-accordion-item");
        await expect(items).toHaveCount(2);
        await expect(items.nth(0)).not.toHaveAttribute("open");
        await expect(items.nth(1)).not.toHaveAttribute("open");
        await capture(page, `${name} closed`);

        await items
          .nth(0)
          .locator("summary.mzf-c-accordion-item__summary")
          .click();
        await expect(items.nth(0)).toHaveAttribute("open");
        const panel = items.nth(0).locator(".mzf-c-accordion-item__reveal");
        await expect(panel).toBeVisible();
        // Wait for the row to settle with its inline height cleared, not a
        // fixed delay.
        await expect
          .poll(() => panel.evaluate((element) => element.style.height))
          .toBe("");
        await expect(panel).toContainText(
          "Page layout, links and accordion content.",
        );
        await capture(page, `${name} open`);
      });
    }
  });
}
