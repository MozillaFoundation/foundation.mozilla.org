import { viewports, A11Y_CONFIG, EXCLUDE_CONSTANTS } from "./global_variables";

let dimension;

const FOMO_A11Y = () => {
  viewports.forEach(viewport => {
    if (viewport === "iphone-5") {
      dimension = "Mobile";
    } else {
      dimension = "Desktop";
    }

    context(`${dimension} Assessments`, () => {
      it.skip(`Homepage`, () => {
        cy.viewport(viewport).visit(`/`);
        cy.window()
          .its(`main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({ exclude: EXCLUDE_CONSTANTS });
      });

      it.skip("About Page ", () => {
        cy.viewport(viewport);
        cy.visit(`en/about`);
        cy.window()
          .its(`main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({ exclude: EXCLUDE_CONSTANTS });
      });

      it.skip("Participate Page", () => {
        cy.viewport(viewport);
        cy.visit(`en/participate`);
        cy.window()
          .its(`main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({ exclude: EXCLUDE_CONSTANTS });
      });

      it.skip("Blog Index Page", () => {
        cy.viewport(viewport);
        cy.visit("en/blog/");
        cy.window()
          .its(`main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({ exclude: EXCLUDE_CONSTANTS });
      });

      it.skip("Fixed Blog Page", () => {
        cy.viewport(viewport);
        cy.visit("/en/blog/initial-test-blog-post-with-fixed-title");
        cy.window()
          .its(`main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({ exclude: EXCLUDE_CONSTANTS });
      });
    });
  });
};

export default FOMO_A11Y;
