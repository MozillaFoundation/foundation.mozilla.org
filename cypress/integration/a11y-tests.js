const customViolationLogger = violation => cy.task("log", violation)
const customViolationHandler = violation => cy.task("log", violation)

const A11Y_CONFIG = {
  reporter: "v2"
}

let EXCLUDE_PNI_GLOBAL;

const EXCLUDE_CONSTANTS = {
  exclude: [
    ['.join-us'], // Signups
    ['.wide-screen-menu', '.nav-links'], // Desktop Nav
    ['.narrow-screen-menu-container', '.nav-links'], //Mobile Nav
    ['.donate-banner *'] // Donate Banner
    ['.site-footer', '#language-switcher'], // Language Switcher
    ['.site-footer a.logo'] // Footer Logo
  ]
}

const EXCLUDE_PNI_CONSTANTS = {
  exclude: [
    ['.join-us'], // Signups
    ['.wide-screen-menu', '.nav-links'], // Desktop Nav
    ['.narrow-screen-menu-container', '.nav-links'], //Mobile Nav
    ['.donate-banner *'] // Donate Banner
    ['.site-footer', '#language-switcher'], // Language Switcher
    ['.site-footer a.logo'], // Footer Logo
    ['#coral-talk-stream', 'iframe'] // Coral
  ]
}

describe(`A11Y Tests`, () => {  
  // before(() => {
  //   cy.window()
  //     .its(`main-js:react:finished`)
  //     .should(`equal`, true);
  //   cy.wait(500);
  // });

  // Need to test prod for Initiatives + Internet Health pages

  describe(`FoMo Page Assessments`, () => {

    // FOMO

    it.skip(`Homepage Accessibility Report`, () => {
      cy.visit()
        .injectAxe()
        .configureAxe(A11Y_CONFIG)
        .checkA11y(EXCLUDE_CONSTANTS)
    })

    it.skip("About Page Accessibility Report", () => {
      cy.visit(`en/about`)
        .injectAxe()
        .configureAxe(A11Y_CONFIG)
        .checkA11y(EXCLUDE_CONSTANTS)
    })

    it.skip("Participate Page Accessibility Report", () => {
      cy.visit(`en/participate`)
        .injectAxe()
        .configureAxe(A11Y_CONFIG)
        .checkA11y(EXCLUDE_CONSTANTS)
    })

    // FOMO Blog

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
  })

  describe(`PNI Page Assessments`, () => {

    it.skip("PNI homepage Accessibility Report", () => {
      cy.visit("en/privacynotincluded/")
      cy.injectAxe()
        .configureAxe(A11Y_CONFIG)
        .checkA11y(EXCLUDE_CONSTANTS)
    })

    it.skip("PNI Category Page Accessibility Report", () => {
      cy.visit("/en/privacynotincluded/categories/toys-games/")
        .injectAxe()
        .configureAxe(A11Y_CONFIG)
        .checkA11y(EXCLUDE_CONSTANTS)
    })

    it.skip("PNI Product Page Accessibility Report", () => {
      cy.visit("/en/privacynotincluded/products/percy-cypress/")
        .injectAxe()
        .configureAxe(A11Y_CONFIG)
        .checkA11y(EXCLUDE_CONSTANTS)
    })

    it("PNI About Page Accessibility Report", () => {
      cy.visit("/en/privacynotincluded/about/")
        .injectAxe()
        .configureAxe(A11Y_CONFIG)
        .checkA11y(EXCLUDE_PNI_CONSTANTS)
    })
  })

  describe(`Global Component Assessments`, () => {
    
    // General newsletter tests

    it.skip("Newsletter Sign Ups Accessibility Report", () => {
      cy.visit(`/`)
        .get(".site-footer .join-us input[type='email']")
        .click()
        .checkA11y({
          include: [
            [".join-us input[type='email'"],
            [".join-us .form-l10n .country-picker"],
            [".join-us .form-l10n #userLanguage-footer"],
            [".join-us input[type='checkbox'"],
            [".join-us button.btn-primary"]
          ]
        })
    })

  })

});
