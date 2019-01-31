const FIXED_DATE = new Date(2019, 1, 1).getTime()

describe('multipage visual regression tests', () => {
  beforeEach(function () {
    cy.clock(FIXED_DATE);
  });

  it('Loads the multipage campaign correctly', function() {
    // Load the multipage campaign
    cy.visit(`/en/campaigns/multi-page/`);

    // Give the browser a few seconds for JSX
    // conversion to kick in.
    cy.wait(10000);

    // And take a snapshot for visual diffing
    cy.percySnapshot();
  });
});
