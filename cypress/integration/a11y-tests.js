const viewports = ['iphone-5', 'macbook-13']

const A11Y_CONFIG = {
  reporter: "v2"
}

const EXCLUDE_CONSTANTS = [
  ['.join-us'], // Signups
  ['.wide-screen-menu', '.nav-links'], // Desktop Nav
  ['.narrow-screen-menu-container', '.nav-links'], //Mobile Nav
  ['.donate-banner *'] // Donate Banner
  ['.site-footer', '#language-switcher'], // Language Switcher
  ['.site-footer a.logo'] // Footer Logo
]

const EXCLUDE_PNI_CONSTANTS = EXCLUDE_CONSTANTS.concat([
  ['#coral-talk-stream', 'iframe'] // Coral
])

let dimension;

describe(`Accessibility Tests`, () => {  
  
  describe(`FoMo Page Assessments`, () => {
    viewports.forEach((viewport) => {
      // FOMO

      if (viewport === 'iphone-5') {
          dimension = 'Mobile'
      } else {
          dimension = 'Desktop'
      }
      
      context(`${dimension} Assessments`, () => {

        it.skip(`Homepage`, () => {
          cy.viewport(viewport)
            .visit(`/`)
          cy.window()
            .its(`main-js:react:finished`)
            .should(`equal`, true)
          cy.wait(500);
          cy.injectAxe()
            .configureAxe(A11Y_CONFIG)
            .checkA11y({exclude: EXCLUDE_CONSTANTS})
        })

        it.skip("About Page ", () => {
          cy.viewport(viewport)
          cy.visit(`en/about`)
          cy.window()
            .its(`main-js:react:finished`)
            .should(`equal`, true)
          cy.wait(500);
          cy.injectAxe()
            .configureAxe(A11Y_CONFIG)
            .checkA11y({exclude: EXCLUDE_CONSTANTS})
        })

        it.skip("Participate Page", () => {
          cy.viewport(viewport)
          cy.visit(`en/participate`)
          cy.window()
            .its(`main-js:react:finished`)
            .should(`equal`, true)
          cy.wait(500);
          cy.injectAxe()
            .configureAxe(A11Y_CONFIG)
            .checkA11y({exclude: EXCLUDE_CONSTANTS})
        })

        // FOMO Blog

        it.skip("Blog Index Page", () => {
          cy.viewport(viewport)
          cy.visit("en/blog/")
          cy.window()
            .its(`main-js:react:finished`)
            .should(`equal`, true)
          cy.wait(500);
          cy.injectAxe()
            .configureAxe(A11Y_CONFIG)
            .checkA11y({exclude: EXCLUDE_CONSTANTS})
        })

        it.skip("Fixed Blog Page", () => {
          cy.viewport(viewport)
          cy.visit("/en/blog/initial-test-blog-post-with-fixed-title")
          cy.window()
            .its(`main-js:react:finished`)
            .should(`equal`, true)
          cy.wait(500);
          cy.injectAxe()
            .configureAxe(A11Y_CONFIG)
            .checkA11y({exclude: EXCLUDE_CONSTANTS})
        })
      })
    })
  })

  describe(`PNI Page Assessments`, () => {
    viewports.forEach((viewport) => {
      // FOMO

      if (viewport === 'iphone-5') {
        dimension = 'Mobile'
    } else {
        dimension = 'Desktop'
    }
      
    context(`${dimension} Assessments`, () => {

      it.skip("PNI homepage Accessibility ", () => {
        cy.viewport(viewport)
        cy.visit("en/privacynotincluded/")
        cy.window()
          .its(`bg-main-js:react:finished`)
          .should(`equal`, true)
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({exclude: EXCLUDE_PNI_CONSTANTS})
      })

      it.skip("PNI Category Page", () => {
        cy.viewport(viewport)
        cy.visit("/en/privacynotincluded/categories/toys-games/")
        cy.window()
          .its(`bg-main-js:react:finished`)
          .should(`equal`, true)
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({exclude: EXCLUDE_PNI_CONSTANTS})
      })

      it.skip("PNI Product Page ", () => {
        cy.viewport(viewport)
        cy.visit("/en/privacynotincluded/products/percy-cypress/")
        cy.window()
          .its(`bg-main-js:react:finished`)
          .should(`equal`, true)
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({exclude: EXCLUDE_PNI_CONSTANTS})
      })

      it.skip("PNI About Page ", () => {
        cy.viewport(viewport)
        cy.visit("/en/privacynotincluded/about/")
        cy.window()
          .its(`bg-main-js:react:finished`)
          .should(`equal`, true)
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({exclude: EXCLUDE_PNI_CONSTANTS})
      })
    })
  })
})

  describe(`Global Component Assessments`, () => {
    viewports.forEach((viewport) => {
      // FOMO

      if (viewport === 'iphone-5') {
        dimension = 'Mobile'
    } else {
        dimension = 'Desktop'
    }
      
    context(`${dimension} Assessments`, () => {
  
      // Header newsletter tests

      context("Header Newsletter Sign Up ", () => {

        before(() => {
          cy.viewport(viewport)
          cy.visit(`/`)
          cy.window()
            .its(`main-js:react:finished`)
            .should(`equal`, true)
          cy.wait(500);
          cy.injectAxe()
        })

        if (viewport === 'iphone-5') {

          // testing user interaction to get to newsletter
          it.skip('General Assessment', () => {
            cy.get(".wide-screen-menu-container .burger")
              .click()
            cy.get(".narrow-screen-menu-container .btn-newsletter")
              .click()
            cy.get(".join-us[data-form-position='header'] input[type='email']")
              .click()
              .checkA11y()
          });

          it.skip('Has a valid focus states.', () => {
            cy.get(".join-us[data-form-position='header'] input[type='email']")
              .click()
              .should('have.focus')
            cy.get(".join-us[data-form-position='header'] select.country-picker")
              .select("United States")
              .should('have.focus')
            cy.get(".join-us[data-form-position='header'] select#userLanguage-header")
              .select("English")
              .should('have.focus')
            cy.checkA11y(".join-us[data-form-position='header']")
          });

          it.skip('Should display error messages after submission failure.', () => {
            cy.get(".join-us[data-form-position='header'] button")
              .click()
            
            // wait for the server to respond, then test for the error
            cy.wait(300)
            cy.get('.has-danger.form-check')
                .should('be.visible');

            // test a11y again, but only .has-danger containers
            cy.checkA11y(".join-us[data-form-position='header'] form .has-danger");
          });
        } else {
          cy.log('It\'s Desktop')
        }
      })

      context.skip('Petition', () => {

        before(() => {
          cy.viewport(viewport)
          cy.visit(`/campaigns/single-page/`)
          cy.window()
            .its(`main-js:react:finished`)
            .should(`equal`, true)
          cy.wait(500);
          cy.injectAxe()
          cy.get(".sign-petition")
        });

        // testing petition text

        it.skip('Petition content should be accessible.', () => {
          cy.checkA11y('.sign-petition .petition-content')
        });
        
        // TODO - test again with react-axe [select props function not recognized]
        it.skip ('Has a valid focus states.', () => {
          cy.get('.sign-petition form').within(() => {
              cy.get('input#givenNames').click().should('have.focus');
              cy.get('input#surname').click().should('have.focus');
              cy.get('input#emailInput').click().should('have.focus');
              cy.get('select.country-picker').select('United States').should('have.focus');
          });

          cy.checkA11y('.sign-petition form');
        });

        // testing error messages
      
        it.skip('Should display error messages after submission failure.', () => {
            cy.get('.sign-petition form button').click();
      
            // wait for the server to respond, then test for the error
            cy.wait(300)
            cy.get('.has-danger.form-check')
                .should('be.visible');
      
            // test a11y again, but only .has-danger containers
            cy.checkA11y('.sign-petition form .has-danger');
        });
      });
      })
    })
  })
});
