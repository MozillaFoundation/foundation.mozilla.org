describe('Accessibility testing for foundation.mozilla.org', function () {
 
    before( function () {
        cy.visit('http://localhost:8000/');
 
        // Inject the axe-core library
        cy.injectAxe();
    });
 
    it('Should load the correct URL', async function () {
        cy.url().should('eq', 'http://localhost:9999/#/login');
    });
    
    it('Has a valid login form.', async function () {
        cy.get('form').within(() => {
            cy.get('input#email').should('be.visible');
 
            cy.get('input#password').should('be.visible');
 
            cy.get('button').should('be.visible');
        });
 
        // first a11y test
        cy.checkA11y();
    });
 
    it('Should display an error message after login failure.', async function () {
        cy.get('input#email').type('fail@test.com');
 
        cy.get('input#password').type('swordfish');
 
        cy.get('button').click();
 
        // wait for the server to respond, then test for the error
        cy.wait(1000)
            .get('div.alert')
            .should('be.visible');
 
        // test a11y again, but only the alert container.
        cy.checkA11y('div.alert');
    });
 
    it('Should redirect to the dashboard after login success.', async function () {
        cy.get('input#email')
            .clear()
            .type('test@test.com')
            .should('have.value', 'test@test.com');
 
        cy.get('input#password')
            .clear()
            .type('123@123')
            .should('have.value', '123@123');
 
        cy.get('button').click();
 
        cy.wait(1000)
            .url().should('eq', 'http://localhost:9999/#/');
    });
 
});
