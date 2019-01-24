describe('multipage visual regression tests', () => {
  it('Loads the multipage campaign correctly', function() {

    // Load the multipage campaign
    cy.visit(`/en/campaigns/multi-page/`);

    // And take a snapshot for visual diffing
    cy.percySnapshot();
  });
});
