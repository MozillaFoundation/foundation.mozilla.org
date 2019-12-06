const A11Y_SETTINGS = {
  reporter: `v2`
};

describe(`A11y Tests`, () => {
  beforeEach(() => {
    cy.injectAxe();
    cy.configureAxe(A11Y_SETTINGS);
  });

  before(() => {
    cy.visit(`/`);
    cy.window()
      .its(`main-js:react:finished`)
      .should(`equal`, true);
    cy.wait(500);
  });

  it(`Homepage`, () => cy.checkA11y(A11Y_SETTINGS));
});
