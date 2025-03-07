/**
 * Set up the search/filter functionality PNI category page
 * (See catalog.html and category_page.html)
 *
 * This is to be compiled as its own JS file (bg-search.compiled.js)
 * and not included in `bg-main.compiled.js`
 */

import { SearchFilter } from "./search/search-filter.js";
import { PNIToggle } from "./search/pni-toggle.js";
import { PNISortDropdown } from "./search/pni-sort-dropdown.js";

const searchFilter = new SearchFilter();
new PNIToggle(searchFilter);
new PNISortDropdown(searchFilter);
