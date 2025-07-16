import { KineticTypeBrandLine } from "../components/home_page/kinetic_type_brand_line.js";

document
  .querySelectorAll(".kinetic-type-brand-line")
  .forEach((el) => new KineticTypeBrandLine(el).init());
