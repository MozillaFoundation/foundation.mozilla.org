const CREEPINESS_FACE = document.querySelector(".creep-o-meter-information");

export class CreepUtils {
  static moveCreepyFace() {
    // When searching, check to see how many products are still visible
    // If there are no visible products, there are "no search results"
    // And when there are no search results, do not show the creepo-meter-face
    if (document.querySelectorAll(".product-box:not(.d-none)").length) {
      // If there are search results, show the creepo-meter-face
      CREEPINESS_FACE.classList.remove("d-none");
    } else {
      // If there are no search results, hide the creepo-meter-face
      CREEPINESS_FACE.classList.add("d-none");
    }
  }

  static sortOnCreepiness() {
    const container = document.querySelector(`.product-box-list`);
    const list = [...container.querySelectorAll(`.product-box`)];
    const creepVal = (e) => parseFloat(e.dataset.creepiness);
    list
      .sort((a, b) => creepVal(a) - creepVal(b))
      .forEach((p) => container.append(p));
  }
}
