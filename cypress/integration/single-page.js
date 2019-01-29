const FIXED_DATE = new Date(2019, 1, 1).getTime()

describe('Integration test with visual testing', () => {
  beforeEach(function () {
    cy.clock(FIXED_DATE);
  });

  it('Loads the homepage', function() {
    // Load the homepage
    cy.visit(`/`);

    // Give the browser a few seconds for JSX
    // conversion to kick in.
    cy.wait(10000);

    // Take a snapshot for visual diffing
    cy.percySnapshot();
  });
});
