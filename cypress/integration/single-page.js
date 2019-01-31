const FIXED_DATE = new Date(2019, 1, 1).getTime()

describe('Integration test with visual testing', () => {
  beforeEach(function () {
    cy.clock(FIXED_DATE);
  });

  it('Loads the homepage', function() {
    cy.visit(`/`);
    cy.window().its('bundle finished loading').should('equal', true);
    cy.percySnapshot();
  });
});
