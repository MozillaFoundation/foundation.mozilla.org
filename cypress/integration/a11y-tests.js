const customViolationLogger = violation => cy.task("log", violation)
const customViolationHandler = violation => cy.task("log", violation)

const A11Y_CONFIG = {
  branding: {
    brand: "Mozilla",
    application: "FoMo"
  },
  reporter: "v2"
}

const EXCLUDE_CONSTANTS = {
  exclude: [
    ['.join-us'], // Signups
    ['.wide-screen-menu', '.nav-links'], // Desktop Nav
    ['.narrow-screen-menu-container', '.nav-links'], //Mobile Nav
    ['.donate-banner'] // Donate Banner
    ['.site-footer', '#language-switcher'], // Language Switcher
    ['.site-footer a.logo'] // Footer Logo
  ]
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

  /******** Primary Page Assessments *********/

  it.skip(`Homepage Accessibility Report`, () => {
    cy.checkA11y(EXCLUDE_CONSTANTS)
  })

  it.skip("About Page Accessibility Report", () => {
    cy.get(".wide-screen-menu > .nav-links > a:nth-child(1)")
      .click()
      .injectAxe()
      .configureAxe(A11Y_CONFIG)
      .checkA11y(EXCLUDE_CONSTANTS)
  })

  it.skip("Participate Page Accessibility Report", () => {
    cy.get(".wide-screen-menu > .nav-links > a:nth-child(4)")
      .click()
      .injectAxe()
      .configureAxe(A11Y_CONFIG)
      .checkA11y(EXCLUDE_CONSTANTS)
  })

  it.skip("Blog Index Page Accessibility Report", () => {
    cy.visit("en/blog/")
      .injectAxe()
      .configureAxe(A11Y_CONFIG)
      .checkA11y(EXCLUDE_CONSTANTS)
  })

  it.skip("Fixed Blog Page Accessibility Report", () => {
    cy.visit("/en/blog/initial-test-blog-post-with-fixed-title")
      .injectAxe()
      .configureAxe(A11Y_CONFIG)
      .checkA11y(EXCLUDE_CONSTANTS)
  })

  /******** Partial Assessments *********/

  // General newsletter tests

  it("Newsletter Sign Ups Accessibility Report", () => {
    cy.get(".site-footer .join-us input[type='email']")
      .click()
    cy.checkA11y({
      include: [
        [".join-us input[type='email'"],
        [".join-us .form-l10n .country-picker"],
        [".join-us .form-l10n #userLanguage-footer"],
        [".join-us input[type='checkbox'"],
        [".join-us button.btn-primary"]
      ]
    })
  })

  /* TODO

      - Mobile Nav/Hamburger
      - Footer Social Links
      - Footer Language Switcher
      - Donate Buttons
  */
});
