import {
  MOBILE,
  DESKTOP,
  viewports,
  A11Y_CONFIG,
  EXCLUDE_PNI_CONSTANTS
} from "./global_variables";

let dimension;

const PNI_A11Y = () => {
  viewports.forEach(viewport => {
    if (viewport === "iphone-5") {
      dimension = MOBILE;
    } else {
      dimension = DESKTOP;
    }

    context(`${dimension} Assessments`, () => {
      beforeEach(() => {
        cy.viewport(viewport);
        cy.visit(`/`);
        cy.window()
          .its(`main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe().configureAxe(A11Y_CONFIG);
      });

      it("PNI homepage Accessibility ", () => {
        cy.visit("en/privacynotincluded/");
        cy.window()
          .its(`bg-main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({ exclude: EXCLUDE_PNI_CONSTANTS });
      });

      it("PNI Category Page", () => {
        cy.visit("/en/privacynotincluded/categories/toys-games/");
        cy.window()
          .its(`bg-main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({ exclude: EXCLUDE_PNI_CONSTANTS });
      });

      it("PNI Product Page ", () => {
        cy.visit("/en/privacynotincluded/products/percy-cypress/");
        cy.window()
          .its(`bg-main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({ exclude: EXCLUDE_PNI_CONSTANTS });
      });

      it("PNI About Page ", () => {
        cy.visit("/en/privacynotincluded/about/");
        cy.window()
          .its(`bg-main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({ exclude: EXCLUDE_PNI_CONSTANTS });
      });
    });
  });
};

export default PNI_A11Y;
