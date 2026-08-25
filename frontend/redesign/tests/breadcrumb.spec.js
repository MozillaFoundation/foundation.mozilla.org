import { expect, test } from "@playwright/test";
import { foundationBaseUrl } from "./base-urls.js";

const galleryIndexUrl = `${foundationBaseUrl()}/gallery/`;
const galleryProjectUrl = `${foundationBaseUrl()}/gallery/gallery-project-1/`;
const viewports = [
  { name: "mobile", width: 375, height: 812 },
  { name: "desktop", width: 1280, height: 720 },
];

async function expectSingleLineLabels(trail) {
  const lineCounts = await trail
    .locator(".breadcrumb__link, .breadcrumb__current")
    .evaluateAll((labels) =>
      labels.map((label) => {
        const range = document.createRange();
        range.selectNodeContents(label);
        return range.getClientRects().length;
      }),
    );

  expect(lineCounts).toEqual(lineCounts.map(() => 1));
}

async function focusWithKeyboard(page, target) {
  await page.evaluate(() => {
    document.body.tabIndex = -1;
    document.body.focus();
  });

  for (let index = 0; index < 100; index += 1) {
    await page.keyboard.press("Tab");
    if (
      await target.evaluate((element) => document.activeElement === element)
    ) {
      return;
    }
  }

  throw new Error("Breadcrumb ancestor link was not reachable by keyboard");
}

async function dismissCookieDialog(page) {
  const closeButton = page.getByRole("button", { name: "Close" });

  try {
    await closeButton.waitFor({ state: "visible", timeout: 5000 });
    await closeButton.click();
  } catch {
    // The consent dialog is not displayed in every environment.
  }
}

test.describe("Breadcrumb navigation", () => {
  for (const viewport of viewports) {
    test(`is absent from the top-level Gallery page at ${viewport.name} width`, async ({
      page,
    }) => {
      await page.setViewportSize(viewport);
      await page.goto(galleryIndexUrl);

      await expect(page.locator(".breadcrumb")).toHaveCount(0);
    });

    test(`renders and focuses the child project trail at ${viewport.name} width`, async ({
      page,
    }) => {
      await page.setViewportSize(viewport);
      await page.goto(galleryProjectUrl);
      await dismissCookieDialog(page);

      const breadcrumb = page.locator(".breadcrumb");
      const desktopTrail = breadcrumb.locator(".breadcrumb__list--desktop");
      const mobileTrail = breadcrumb.locator(".breadcrumb__list--mobile");
      const visibleTrail =
        viewport.name === "mobile" ? mobileTrail : desktopTrail;
      const hiddenTrail =
        viewport.name === "mobile" ? desktopTrail : mobileTrail;

      await expect(breadcrumb).toBeVisible();
      await expect(visibleTrail).toBeVisible();
      await expect(hiddenTrail).toBeHidden();
      await expect(
        mobileTrail.locator(".breadcrumb__link, .breadcrumb__current"),
      ).toHaveText(["Gallery", "Project Page"]);
      await expect(
        visibleTrail.locator('.breadcrumb__current[aria-current="page"]'),
      ).toHaveCount(1);
      await expect(visibleTrail.locator("a.breadcrumb__current")).toHaveCount(
        0,
      );
      await expect(visibleTrail.locator(".breadcrumb__link")).toHaveAttribute(
        "href",
        "/en/gallery/",
      );
      await expectSingleLineLabels(visibleTrail);

      const breadcrumbBox = await breadcrumb.boundingBox();
      const heroBox = await page.locator(".hero-carousel").boundingBox();
      expect(breadcrumbBox.y + breadcrumbBox.height).toBeLessThanOrEqual(
        heroBox.y,
      );

      const ancestorLink = visibleTrail.locator(".breadcrumb__link");
      await focusWithKeyboard(page, ancestorLink);
      await expect(ancestorLink).toBeFocused();
      await expect
        .poll(async () =>
          ancestorLink.evaluate(
            (link) => getComputedStyle(link, "::after").width,
          ),
        )
        .not.toBe("0px");
    });
  }
});
