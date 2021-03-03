const FIXED_DATE = new Date(2019, 1, 1).getTime();
const MOZFEST_BASE_URL = Cypress.env("mozfest-baseurl");

describe(`URL verification tests`, () => {
  beforeEach(function () {
    cy.clock(FIXED_DATE);
  });

  it(`Foundation homepage`, function () {
    cy.visit(`/`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`What can you do page`, function () {
    cy.visit(`/en/what-you-can-do/`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Who We Are page`, function () {
    cy.visit(`/en/who-we-are`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Blog index page`, function () {
    cy.visit(`/en/blog`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Blog index filtered on tag`, function () {
    cy.visit(`/en/blog/tags/iot`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Blog index with non-existent tag`, function () {
    cy.visit(`/en/blog/tags/randomnonsensetagthatdoesntexist`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Blog index filtered on category`, function () {
    cy.visit(`/en/blog/category/mozilla-festival`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Fixed blog post page`, function () {
    cy.visit(`/en/blog/initial-test-blog-post-with-fixed-title`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Campaign index page`, function () {
    cy.visit(`/en/campaigns`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Single-page campaign`, function () {
    cy.visit(`/en/campaigns/single-page/`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Multi-page campaign`, function () {
    cy.visit(`/en/campaigns/multi-page/`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Bannered Campaign Page`, function () {
    cy.visit(`/en/campaigns/initial-test-bannered-campaign-with-fixed-title`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Publication Page with Child Article Pages`, function () {
    cy.visit(`/en/publication-page-with-child-article-pages`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Publication Page with Child Chapter Pages`, function () {
    cy.visit(`/en/publication-page-with-chapter-pages`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Publication Page as Chapter Page`, function () {
    cy.visit(
      `/en/publication-page-with-chapter-pages/fixed-title-chapter-page`
    );
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`Article Page`, function () {
    cy.visit(
      `/en/publication-page-with-chapter-pages/fixed-title-chapter-page/fixed-title-article-page`
    );
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`PNI homepage`, function () {
    cy.visit(`/en/privacynotincluded/`);
    cy.window().its(`bg-main-js:react:finished`).should(`equal`, true);
  });

  it(`PNI category page`, function () {
    cy.visit(`/en/privacynotincluded/categories/toys-games/`);
    cy.window().its(`bg-main-js:react:finished`).should(`equal`, true);
  });

  it(`PNI general product page`, function () {
    cy.visit(`/en/privacynotincluded/general-percy-product/`);
    cy.window().its(`bg-main-js:react:finished`).should(`equal`, true);
  });

  it(`PNI software product page`, function () {
    cy.visit(`/en/privacynotincluded/software-percy-product/`);
    cy.window().its(`bg-main-js:react:finished`).should(`equal`, true);
  });

  it(`Styleguide page`, function () {
    cy.visit(`/en/style-guide/`);
  });

  it(`YouTube Regrets page`, function () {
    cy.visit(`/en/campaigns/youtube-regrets/`);
  });

  it(`YouTube RegretsReporter page`, function () {
    cy.visit(`/en/campaigns/regrets-reporter/`);
  });

  it(`Dear Internet page`, function () {
    cy.visit(`/en/campaigns/dearinternet/`);
  });

  it(`MozFest homepage`, function () {
    cy.visit(`${MOZFEST_BASE_URL}`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });

  it(`MozFest primary page`, function () {
    cy.visit(`${MOZFEST_BASE_URL}/spaces`);
    cy.window().its(`main-js:react:finished`).should(`equal`, true);
  });
});
