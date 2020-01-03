import { viewports, A11Y_CONFIG } from './global_variables'

let dimension;

const GLOBAL_COMPONENT_A11Y = () => {
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
      
              if (viewport === 'iphone-5') {

                before(() => {
                  cy.viewport(viewport)
                  cy.visit(`/`)
                  cy.window()
                    .its(`main-js:react:finished`)
                    .should(`equal`, true)
                  cy.wait(500);
                  cy.injectAxe()
                    .configureAxe(A11Y_CONFIG)
                })
      
                it.skip('General Assessment', () => {

                  // testing user interaction to get to mobile newsletter
                  cy.get(".wide-screen-menu-container .burger")
                    .click()
                  cy.get(".narrow-screen-menu-container .btn-newsletter")
                    .click()
                  cy.wait(300)
                  
                  // Check focus states
                  cy.get(".join-us[data-form-position='header'] input[type='email']")
                    .click()
                    .wait(300)
                    .should('have.focus')
                  cy.get(".join-us[data-form-position='header'] select.country-picker")
                    .select("Canada")
                    .wait(200)
                    .should('have.focus')
                  cy.get(".join-us[data-form-position='header'] select#userLanguage-header")
                    .select("Français")
                    .wait(200)
                    .should('have.focus')
                  cy.checkA11y(".join-us[data-form-position='header']");
                });
      
                it.skip('Should display error messages after submission failure.', () => {
                  // testing user interaction to get to mobile newsletter
                  cy.get(".wide-screen-menu-container .burger")
                    .click()
                  cy.get(".narrow-screen-menu-container .btn-newsletter")
                    .click()
                  cy.wait(200)
                  cy.get(".join-us[data-form-position='header'] button")
                    .click()
                  
                  // wait for the server to respond, then test for the error
                  cy.wait(300)
                  cy.get('.has-danger')
                    .children('p.form-control-feedback')
                    .should('be.visible')

                  // test a11y again, but only .has-danger containers
                  cy.checkA11y(".join-us[data-form-position='header'] form .has-danger");
                });
              } else if (viewport === 'macbook-13') {

                before(() => {
                  cy.viewport(viewport)
                  cy.visit(`/`)
                  cy.window()
                    .its(`main-js:react:finished`)
                    .should(`equal`, true)
                  cy.wait(500);
                  cy.injectAxe()
                    .configureAxe(A11Y_CONFIG)
                })

                it.skip('General Assessment', () => {

                  // testing user interaction to get to desktop newsletter
                  cy.get(".wide-screen-menu-container .btn-newsletter")
                    .trigger('click', {force: true})
                  cy.get("#nav-newsletter-form-wrapper")
                    .should('be.visible')
                    .then(() => {
                      
                    // Check focus states
                    cy.get(".join-us[data-form-position='header'] input[type='email']")
                      .should('be.visible')
                      .click({force:true})
                    cy.get(".join-us[data-form-position='header'] select.country-picker")
                      .select("Canada", {force: true})
                      .wait(200)
                      .should('have.focus')
                    cy.get(".join-us[data-form-position='header'] select#userLanguage-header")
                      .select("Français", {force: true})
                      .wait(200)
                      .should('have.focus')
                    cy.checkA11y(".join-us[data-form-position='header']");
                    })
                });
      
                it.skip('Should display error messages after submission failure.', () => {

                  // testing user interaction to get to mobile newsletter
                  cy.get(".wide-screen-menu-container .btn-newsletter")
                    .click()
                  cy.wait(200)
                  cy.get(".join-us[data-form-position='header'] button")
                    .click()
                  
                  // wait for the server to respond, then test for the error
                  cy.wait(300)
                  cy.get('.has-danger')
                    .children('p.form-control-feedback')
                    .should('be.visible')

                  // test a11y again, but only .has-danger containers
                  cy.checkA11y(".join-us[data-form-position='header'] form .has-danger");
                });
      
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
                  .configureAxe(A11Y_CONFIG)
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
}

export default GLOBAL_COMPONENT_A11Y;
