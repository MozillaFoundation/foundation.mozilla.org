/**
 * Set up the search/filter functionality for PNI pages
 */

import { SearchFilter } from "./search/search-filter.js";
import { PNIToggle } from "./search/pni-toggle.js";

const searchFilter = new SearchFilter();
new PNIToggle(searchFilter);
