const FIXED_DATE = new Date(2019, 1, 1).getTime()

describe('multipage visual regression tests', () => {
  beforeEach(function () {
    cy.clock(FIXED_DATE);
  });

  it('Loads the multipage campaign correctly', function() {
    // Load the multipage campaign
    cy.visit(`/en/campaigns/multi-page/`);

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
