const Utility = {
  /**
   * Find and bind all necessary DOM nodes, returning "false" if not all DOM nodes were found.
   * @param  {Object} elements        Object that contains all keys and unprocessed values
   * @param  {Boolean} findAllMatched Object that contains all keys and unprocessed values
   * @returns {Boolean} Returns elements if all DOM nodes specified have been found.
   *                    Returns false otherwise.
   */
  checkAndBindDomNodes(elements, findAllMatched) {
    let allFound = Object.keys(elements).every(key => {
      // if this element already resolved to a DOM node, move on to the next
      let selector = elements[key];
      if (typeof selector !== "string") return true;

      // find DOM nodes, and report on the result (binding it if found for later use)
      if (findAllMatched) {
        let nodes = document.querySelectorAll(selector);

        if (nodes) elements[key] = nodes;
        return nodes.length > 0;
      }

      let node = document.querySelector(selector);

      if (node) elements[key] = node;
      return !!node;
    });

    return allFound ? elements : false;
  },

  /**
   * Hide newsletter button on nav if the page's main content section has a sign up form already.
   */
  hideNavNewsletterButtonConditionally() {
    let mainSignup = document.querySelector(`.main-content .join-us`);
    let navButtons = document.querySelectorAll(`nav .btn-newsletter`);

    if (!!mainSignup && navButtons.length > 0) {
      navButtons.forEach(button => button.classList.add(`d-none`));
    }
  }
};

export default Utility;
