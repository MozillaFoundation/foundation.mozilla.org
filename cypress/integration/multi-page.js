const FIXED_DATE = new Date(2019, 1, 1).getTime()

describe('multipage visual regression tests', () => {
  beforeEach(function () {
    cy.clock(FIXED_DATE);
  });

  it('Loads the multipage campaign correctly', function() {
    cy.visit(`/en/campaigns/multi-page/`);
    cy.window().its('bundle finished loading').should('equal', true);
    cy.percySnapshot();
  });
});
