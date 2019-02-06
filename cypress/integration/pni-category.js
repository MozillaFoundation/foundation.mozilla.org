const FIXED_DATE = new Date(2019, 1, 1).getTime()

describe('Visual regression testing for PNI category pages', () => {
  beforeEach(function () {
    cy.clock(FIXED_DATE);
  });

  it('Loads category page', function() {
    cy.visit(`/en/privacynotincluded/categories/toys-games/`);
    cy.window().its('bg-main-js:react:finished').should('equal', true);
    cy.wait(1000);
    cy.percySnapshot();
  });
});
