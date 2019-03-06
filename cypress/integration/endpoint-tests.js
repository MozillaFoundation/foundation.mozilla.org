const FIXED_DATE = new Date(2019, 1, 1).getTime()

describe('Visual regression testing for campaigns/multi-page', () => {
  beforeEach(function () {
    cy.clock(FIXED_DATE);
  });

  it('Foundation homepage', function() {
    cy.visit(`/`);
    cy.window().its('main-js:react:finished').should('equal', true);
    cy.wait(500);
    cy.percySnapshot();
  });

  it('About page', function() {
    cy.visit(`/en/about`);
    cy.window().its('main-js:react:finished').should('equal', true);
    cy.wait(500);
    cy.percySnapshot();
  });

  it('Multi-page campaign', function() {
    cy.visit(`/en/campaigns/multi-page/`);
    cy.window().its('main-js:react:finished').should('equal', true);
    cy.wait(500);
    cy.percySnapshot();
  });

  it('PNI homepage', function() {
    cy.visit(`/en/privacynotincluded`);
    cy.window().its('bg-main-js:react:finished').should('equal', true);
    cy.wait(500);
    cy.percySnapshot();
  });

  it('PNI category page', function() {
    cy.visit(`/en/privacynotincluded/categories/toys-games/`);
    cy.window().its('bg-main-js:react:finished').should('equal', true);
    cy.wait(500);
    cy.percySnapshot();
  });
});
