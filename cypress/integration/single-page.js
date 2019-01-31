const FIXED_DATE = new Date(2019, 1, 1).getTime()

describe('Integration test with visual testing', () => {
  beforeEach(function () {
    cy.clock(FIXED_DATE);
  });

  it('Loads the homepage', function() {
    // Load the homepage
    cy.visit(`/`);

    // Attach a listener to the document that lets us know
    // when main.js is done with all the JSX (re)placement.
    cy.document().then((document) => {
      document.addEventListener(`main-js:done`, evt => {
        // wait one second just in case
        cy.wait(1000);

        // And take a snapshot for visual diffing
        cy.percySnapshot();
      });
    });
  });
});
