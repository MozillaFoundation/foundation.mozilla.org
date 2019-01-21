describe('Integration test with visual testing', () => {
  it('Loads the homepage', function() {

    // Load the page or perform any other interactions with the app.
    cy.visit(`/`);

    // Take a snapshot for visual diffing
    cy.percySnapshot();
  });
});
