const customViolationLogger = violation => cy.task("log", violation)
const customViolationHandler = violation => cy.task("log", violation)

const A11Y_CONFIG = {
  branding: {
    brand: "Mozilla",
    application: "FoMo"
  },
  reporter: "v2"
}

describe(`A11y Tests`, () => {  
  beforeEach(() => {
    cy.injectAxe();
    cy.configureAxe(A11Y_CONFIG);
  });

  before(() => {
    cy.visit(`/`);
    cy.window()
      .its(`main-js:react:finished`)
      .should(`equal`, true);
    cy.wait(500);
  });

  // Need to test prod for Initiatives + Internet Health pages

  it(`Homepage Accessibility Report`, () => {
    cy.checkA11y()
  })

  it("About Page Accessibility Report", () => {
    cy.get(".wide-screen-menu > .nav-links > a:nth-child(1)")
      .click()
      .injectAxe()
      .configureAxe(A11Y_CONFIG)
      .checkA11y()
  })

  it("Participate Page Accessibility Report", () => {
    cy.get(".wide-screen-menu > .nav-links > a:nth-child(4)")
      .click()
      .injectAxe()
      .configureAxe(A11Y_CONFIG)
      .checkA11y()
  })

  /* TODO
      - Blog
      - Blog Page
      - Header Newsletter
  */
});
