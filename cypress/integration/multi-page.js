const FIXED_DATE = new Date(2019, 1, 1).getTime()

describe('multipage visual regression tests', () => {
  beforeEach(function () {
    cy.clock(FIXED_DATE);
  });

  it('Loads the multipage campaign correctly', function() {
    cy.visit(`/en/campaigns/multi-page/`);
    cy.window().its('main-js:react:finished').should('equal', true);
    cy.wait(1000);
    cy.percySnapshot();
  });
});
