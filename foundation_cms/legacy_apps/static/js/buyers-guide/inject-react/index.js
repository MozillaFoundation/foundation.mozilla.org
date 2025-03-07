import injectCreepVote from "./creep-vote.js";
import injectProductQuiz from "./product-quiz.js";

/**
 * Inject React components
 * @param {Array} apps The existing array we are using to to track all React client rendering calls
 * @param {String} siteUrl Foundation site base URL
 */
export const injectReactComponents = (apps, siteUrl) => {
  injectCreepVote(apps, siteUrl);
  injectProductQuiz(apps, siteUrl);
};
