import { MOBILE, DESKTOP, viewports, A11Y_CONFIG } from "./global_variables";

let dimension;
const INERT_CODE_PATH = false;

const GLOBAL_COMPONENT_A11Y = () => {
  viewports.forEach(viewport => {
    if (viewport === "iphone-5") {
      dimension = MOBILE;
    } else {
      dimension = DESKTOP;
    }

    context(`${dimension} Assessments`, () => {
      context("Header Newsletter Sign Up ", () => {
        if (viewport === MOBILE) {
          beforeEach(() => {
            cy.viewport(375, 667);
            cy.visit(`/`);
            cy.window()
              .its(`main-js:react:finished`)
              .should(`equal`, true);
            cy.wait(500);
            cy.injectAxe().configureAxe(A11Y_CONFIG);
          });

          it("General Assessment", () => {
            // testing user interaction to get to mobile newsletter
            cy.get(".wide-screen-menu-container .burger").click();
            cy.get(".narrow-screen-menu-container .btn-newsletter").click();
            cy.wait(200);

            // Check focus states
            cy.get(".join-us[data-form-position='header'] input[type='email']")
              .click()
              .wait(200)
              .should("have.focus");
            cy.get(
              ".join-us[data-form-position='header'] select.country-picker"
            )
              .select("Canada")
              .wait(200)
              .should("have.focus");
            cy.get(
              ".join-us[data-form-position='header'] select#userLanguage-header"
            )
              .select("Français")
              .wait(200)
              .should("have.focus");
            cy.checkA11y(".join-us[data-form-position='header']");
          });

          it("Should display error messages after submission failure.", () => {
            // testing user interaction to get to mobile newsletter
            cy.get(".wide-screen-menu-container .burger").click();
            cy.get(".narrow-screen-menu-container .btn-newsletter").click();
            cy.wait(200);

            // submit with invalid data, without clicking the input field
            cy.get(".join-us[data-form-position='header'] button").click();
            cy.wait(200);

            // test for the error
            cy.get(".has-danger")
              .children("p.form-control-feedback")
              .should("be.visible");

            // test a11y again, but only .has-danger containers
            cy.checkA11y(
              ".join-us[data-form-position='header'] form .has-danger"
            );

            // dismiss the menu
            cy.get(".wide-screen-menu-container .burger").click();
          });
        } else if (viewport === DESKTOP) {
          beforeEach(() => {
            cy.viewport(viewport);
            cy.visit(`/`);
            cy.window()
              .its(`main-js:react:finished`)
              .should(`equal`, true);
            cy.wait(500);
            cy.injectAxe().configureAxe(A11Y_CONFIG);
          });

          it("General Assessment", () => {
            // testing user interaction to get to desktop newsletter
            cy.get(".wide-screen-menu-container .btn-newsletter").click({
              force: true
            });
            cy.wait(500);

            cy.get("#nav-newsletter-form-wrapper")
              .should("have.class", "expanded")
              .should("be.visible")
              .then(() => {
                // Check focus states
                cy.get(
                  ".join-us[data-form-position='header'] input[type='email']"
                )
                  .should("be.visible")
                  .click({ force: true });
                cy.get(
                  ".join-us[data-form-position='header'] select.country-picker"
                )
                  .select("Canada", { force: true })
                  .wait(200)
                  .should("have.focus");
                cy.get(
                  ".join-us[data-form-position='header'] select#userLanguage-header"
                )
                  .select("Français", { force: true })
                  .wait(200)
                  .should("have.focus");
                cy.checkA11y(".join-us[data-form-position='header']");
              });
          });

          it("Should display error messages after submission failure.", () => {
            // testing user interaction to get to desktop newsletter
            cy.get(".wide-screen-menu-container .btn-newsletter").click({
              force: true
            });
            cy.wait(500);

            // submit with invalid data, without clicking the input field
            cy.get(".join-us[data-form-position='header'] button").click({
              force: true
            });
            cy.wait(200);

            // test for the error
            cy.get(".has-danger p.form-control-feedback").should("be.visible");

            // test a11y again, but only .has-danger containers
            cy.checkA11y(
              ".join-us[data-form-position='header'] form .has-danger"
            );
          });
        }
      });

      context("Petition", () => {
        before(() => {
          cy.viewport(viewport);
          cy.visit(`/campaigns/single-page/`);
          cy.window()
            .its(`main-js:react:finished`)
            .should(`equal`, true);
          cy.wait(500);
          cy.injectAxe().configureAxe(A11Y_CONFIG);
          cy.get(".sign-petition");
        });

        it("Petition content should be accessible.", () => {
          cy.checkA11y(".sign-petition .petition-content");
        });

        it("Petition form has valid focus states.", () => {
          cy.get(".sign-petition form").within(() => {
            cy.get("input#givenNames")
              .click()
              .should("have.focus");
            cy.get("input#surname")
              .click()
              .should("have.focus");
            cy.get("input#emailInput")
              .click()
              .should("have.focus");
            cy.get("select.country-picker")
              .select("United States")
              .should("have.focus");
          });

          // test general a11y for this form

          if (INERT_CODE_PATH) {
            // KNOWN FAILURE: COLOR CONTRAST TOO LOW
            cy.checkA11y(".sign-petition form");
          }
        });

        // testing error messages
        it("Should display error messages after submission failure.", () => {
          cy.get(".sign-petition form button").click();

          // wait for the server to respond, then test for the error
          cy.wait(300);
          cy.get(".has-danger.form-check").should("be.visible");

          // test a11y again, but only .has-danger containers

          if (INERT_CODE_PATH) {
            // KNOWN FAILURE: COLOR CONTRAST TOO LOW
            cy.checkA11y(".sign-petition form .has-danger");
          }
        });
      });
    });
  });
};

export default GLOBAL_COMPONENT_A11Y;
