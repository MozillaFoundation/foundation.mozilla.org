- [x] land Playwright testing
- [x] create PNI search test(s)
- [x] move all `init()` calls out as plain functions
- [x] updated the base data to include subcategories for a PNI main category.
- [x] update tests to check for subcategory behaviour.
- [x] continue the refactor
- [x] move all "object functions" in search over as (temporary) "class functions"
- [x] move all "can be moved to utils" functions into their own (possibly more than one) util modules
- [x] move the setupXYZ functions back into the class (where sensible)
- [x] we should be done with the initial refactor now


Outstanding tasks:
- check if we can create a single history update function, as we call build and set state in several different places at the moment.
- try to move as many consts into classes/constructors rather than keeping them bare consts
