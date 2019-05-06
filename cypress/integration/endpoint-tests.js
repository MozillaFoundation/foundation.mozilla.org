const FIXED_DATE = new Date(2019, 1, 1).getTime();

describe(`Visual regression testing for foundation.mozilla.org`, () => {
  beforeEach(function() {
    cy.clock(FIXED_DATE);
  });

  // Main pages

  it(`Foundation homepage`, function() {
    cy.visit(`/`);
    cy.window()
      .its(`main-js:react:finished`)
      .should(`equal`, true);
    cy.wait(500);
    cy.percySnapshot();
  });

  it(`Participate page`, function() {
    cy.visit(`/en/participate/`);
    cy.window()
      .its(`main-js:react:finished`)
      .should(`equal`, true);
    cy.wait(500);
    cy.percySnapshot();
  });

  it(`About page`, function() {
    cy.visit(`/en/about`);
    cy.window()
      .its(`main-js:react:finished`)
      .should(`equal`, true);
    cy.wait(500);
    cy.percySnapshot();
  });

  // Opportunity page tests (single and multi-page)

  it(`Single-page opportunity`, function() {
    cy.visit(`/en/opportunity/single-page/`);
    cy.window()
      .its(`main-js:react:finished`)
      .should(`equal`, true);
    cy.wait(500);
    cy.percySnapshot();
  });

  it(`Multi-page opportunity`, function() {
    cy.visit(`/en/opportunity/multi-page/`);
    cy.window()
      .its(`main-js:react:finished`)
      .should(`equal`, true);
    cy.wait(500);
    cy.percySnapshot();
  });

  // Campaign page tests (single and multi-page)

  it(`Single-page campaign`, function() {
    cy.visit(`/en/campaigns/single-page/`);
    cy.window()
      .its(`main-js:react:finished`)
      .should(`equal`, true);
    cy.wait(500);
    cy.percySnapshot();
  });

  it(`Multi-page campaign`, function() {
    cy.visit(`/en/campaigns/multi-page/`);
    cy.window()
      .its(`main-js:react:finished`)
      .should(`equal`, true);
    cy.wait(500);
    cy.percySnapshot();
  });

  // Pages specific to the "Privacy Not Included" Buyers Guide

  it(`PNI homepage`, function() {
    cy.visit(`/en/privacynotincluded`);
    cy.window()
      .its(`bg-main-js:react:finished`)
      .should(`equal`, true);
    cy.wait(500);
    cy.percySnapshot();
  });

  it(`PNI category page`, function() {
    cy.visit(`/en/privacynotincluded/categories/toys-games/`);
    cy.window()
      .its(`bg-main-js:react:finished`)
      .should(`equal`, true);
    cy.wait(500);
    cy.percySnapshot();
  });

  it(`PNI product page`, function() {
    cy.visit(`/en/privacynotincluded/products/percy-cypress/`);
    cy.window()
      .its(`bg-main-js:react:finished`)
      .should(`equal`, true);
    cy.wait(500);
    cy.percySnapshot();
  });
});
