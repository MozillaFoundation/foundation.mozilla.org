/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from "react";
import ReactGA from "react-ga";
import ReactDOM from "react-dom";
import Analytics from "./analytics.js";

import JoinUs from "./components/join/join.jsx";
import Petition from "./components/petition/petition.jsx";
import MemberNotice from "./components/member-notice/member-notice.jsx";
import MultipageNavMobile from "./components/multipage-nav-mobile/multipage-nav-mobile.jsx";
import News from "./components/news/news.jsx";
import PulseProjectList from "./components/pulse-project-list/pulse-project-list.jsx";
import ShareButtonGroup from "./components/share-button-group/share-button-group.jsx";

import primaryNav from "./primary-nav.js";
import navNewsletter from "./nav-newsletter.js";
import bindMozFestGA from "./mozfest-ga.js";
import youTubeRegretsTunnel from "./youtube-regrets.js";

const SHOW_MEMBER_NOTICE = false;

// To be populated via XHR and querySelector
let env, networkSiteURL, csrfToken;

// Track all ReactDOM.render calls so we can use a Promise.all()
// all the way at the end to make sure we don't report "we are done"
// until all the React stuff is _actually_ done.
const apps = [];

let main = {
  init() {
    this.fetchEnv(envData => {
      env = envData;
      networkSiteURL = env.NETWORK_SITE_URL;

      csrfToken = document.querySelector(`meta[name="csrf-token"]`);
      csrfToken = csrfToken ? csrfToken.getAttribute(`content`) : false;

      // HEROKU_APP_DOMAIN is used by review apps
      if (!networkSiteURL && env.HEROKU_APP_NAME) {
        networkSiteURL = `https://${env.HEROKU_APP_NAME}.herokuapp.com`;
      }

      const gaMeta = document.querySelector(`meta[name="ga-identifier"]`);
      if (gaMeta) {
        let gaIdentifier = gaMeta.getAttribute(`content`);
        Analytics.initialize(gaIdentifier);
      }

      this.injectReactComponents();
      this.bindGlobalHandlers();
      this.bindGAEventTrackers();

      // Record that we're done, when we're really done.
      Promise.all(apps).then(() => {
        window[`main-js:react:finished`] = true;
      });
    });
  },

  fetchEnv(callback) {
    let envReq = new XMLHttpRequest();

    envReq.addEventListener(`load`, () => {
      callback.call(this, JSON.parse(envReq.response));
    });

    envReq.open(`GET`, `/environment.json`);
    envReq.send();
  },

  fetchHomeDataIfNeeded(callback) {
    // Only fetch data if you're on the homepage
    if (document.querySelector(`#view-home`)) {
      let homepageReq = new XMLHttpRequest();

      homepageReq.addEventListener(`load`, () => {
        callback.call(this, JSON.parse(homepageReq.response));
      });

      homepageReq.open(`GET`, `${networkSiteURL}/api/homepage/`);
      homepageReq.send();
    } else {
      callback.call(this, {});
    }
  },

  bindGlobalHandlers() {
    // Track window scroll position and add/remove class to change sticky header appearance

    let lastKnownScrollPosition = 0;
    let ticking = false;
    let elBurgerWrapper = document.querySelector(`.wrapper-burger`);

    let adjustNavbar = scrollPosition => {
      if (scrollPosition > 0) {
        elBurgerWrapper.classList.add(`scrolled`);
      } else {
        elBurgerWrapper.classList.remove(`scrolled`);
      }
    };

    let elCtaAnchor = document.querySelector(`#cta-anchor`);
    let elStickyButton = document.querySelector(
      `.narrow-sticky-button-container`
    );
    let noopCtaButton = () => {};
    let adjustCtaButton = noopCtaButton;

    if (elCtaAnchor && elStickyButton) {
      let getAnchorPosition = () => {
        return (
          elCtaAnchor.getBoundingClientRect().top +
          window.scrollY -
          window.innerHeight
        );
      };

      let ctaAnchorPosition = getAnchorPosition();

      window.addEventListener(`resize`, () => {
        ctaAnchorPosition = getAnchorPosition();
      });

      let scrollCtaButton = scrollPosition => {
        if (scrollPosition > ctaAnchorPosition) {
          elStickyButton.classList.add(`hidden`);
          adjustCtaButton = noopCtaButton;
        }
      };

      let initCtaButton = scrollPosition => {
        if (scrollPosition <= ctaAnchorPosition) {
          elStickyButton.classList.remove(`hidden`);
          adjustCtaButton = scrollCtaButton;
        }
      };

      adjustCtaButton = initCtaButton;
    }

    let onScroll = () => {
      lastKnownScrollPosition = window.scrollY;

      if (!ticking) {
        window.requestAnimationFrame(() => {
          adjustNavbar(lastKnownScrollPosition);
          adjustCtaButton(lastKnownScrollPosition);
          ticking = false;
        });
      }

      ticking = true;
    };

    window.addEventListener(`scroll`, onScroll);

    // Toggle sticky share buttons on blog page

    let blogPageStickyButtons = document.querySelector(
      `#view-blog .blog-sticky-side .share-button-group`
    );
    let blogPageFullButtons = document.querySelector(
      `#view-blog .blog-body .share-button-group`
    );

    if (blogPageStickyButtons && blogPageFullButtons) {
      const isInViewport = element => {
        let box = element.getBoundingClientRect();

        return box.top <= window.innerHeight && box.top + box.height >= 0;
      };

      const toggleStickyButtons = () => {
        if (isInViewport(blogPageFullButtons)) {
          blogPageStickyButtons.classList.add(`faded`);
        } else {
          blogPageStickyButtons.classList.remove(`faded`);
        }
      };

      window.addEventListener(`scroll`, toggleStickyButtons);
      toggleStickyButtons();
    }

    // Call once to get scroll position on initial page load.
    onScroll();

    primaryNav.init();
    navNewsletter.init(networkSiteURL, csrfToken);
    youTubeRegretsTunnel.init();

    // Extra tracking

    let donateHeaderBtn = document.getElementById(`donate-header-btn`);
    if (donateHeaderBtn) {
      donateHeaderBtn.addEventListener(`click`, () => {
        ReactGA.event({
          category: `donate`,
          action: `donate button tap`,
          label: `${document.title} header`
        });
      });
    }

    let donateFooterBtn = document.getElementById(`donate-footer-btn`);
    if (donateFooterBtn) {
      donateFooterBtn.addEventListener(`click`, () => {
        ReactGA.event({
          category: `donate`,
          action: `donate button tap`,
          label: `${document.title} footer`
        });
      });
    }
  },

  bindGAEventTrackers() {
    let seeMorePage = document.querySelector(`#see-more-modular-page`);

    if (seeMorePage) {
      seeMorePage.addEventListener(`click`, () => {
        let label = ``;
        let pageHeader = document.querySelector(`.cms h1`);

        if (pageHeader) {
          label = `${pageHeader.innerText} - footer cta`;
        }

        Analytics.sendGAEvent(`navigation`, `page footer cta`, label);
      });
    }

    let participateDonateBtn = document.querySelector(
      `#view-participate .card-cta .btn[href*="donate.mozilla.org"]`
    );

    if (participateDonateBtn) {
      participateDonateBtn.addEventListener(`click`, () => {
        ReactGA.event({
          category: `donate`,
          action: `donate button tap`,
          label: document.title
        });
      });
    }

    bindMozFestGA();
  },

  // Embed various React components based on the existence of containers within the current page
  injectReactComponents() {
    if (SHOW_MEMBER_NOTICE && document.getElementById(`member-notice`)) {
      apps.push(
        new Promise(resolve => {
          ReactDOM.render(
            <MemberNotice whenLoaded={() => resolve()} />,
            document.getElementById(`member-notice`)
          );
        })
      );
    }

    // Embed additional instances of the Join Us box that don't need an API exposed (eg: Homepage)
    document.querySelectorAll(`.join-us:not(.on-nav)`).forEach(element => {
      var props = element.dataset;

      props.apiUrl = `${networkSiteURL}/api/campaign/signups/${props.signupId ||
        0}/`;

      props.csrfToken = props.csrfToken || csrfToken;
      props.isHidden = false;

      apps.push(
        new Promise(resolve => {
          ReactDOM.render(
            <JoinUs {...props} whenLoaded={() => resolve()} />,
            element
          );
        })
      );
    });

    // petition elements
    var petitionElements = Array.from(
      document.querySelectorAll(`.sign-petition`)
    );
    var subscribed = false;

    if (window.location.search.indexOf(`subscribed=1`) !== -1) {
      subscribed = true;
    }

    petitionElements.forEach(element => {
      var props = element.dataset;

      props.apiUrl = `${networkSiteURL}/api/campaign/petitions/${props.petitionId}/`;

      apps.push(
        new Promise(resolve => {
          ReactDOM.render(
            <Petition
              {...props}
              isHidden={false}
              subscribed={subscribed}
              whenLoaded={() => resolve()}
            />,
            element
          );
        })
      );
    });

    // Multipage nav used in landing pages
    if (document.querySelector(`#multipage-nav`)) {
      let links = [];

      links = [].map.call(
        document.querySelectorAll(`#multipage-nav a`),
        child => {
          return {
            label: child.textContent.trim(),
            href: child.getAttribute(`href`),
            isActive: !!child.getAttribute(`class`).match(/active/)
          };
        }
      );

      apps.push(
        new Promise(resolve => {
          ReactDOM.render(
            <MultipageNavMobile links={links} whenLoaded={() => resolve()} />,
            document.querySelector(
              `#multipage-nav-mobile .container .row .col-12`
            )
          );
        })
      );
    }

    // News
    if (document.querySelector(`#news`)) {
      apps.push(
        new Promise(resolve => {
          ReactDOM.render(
            <News env={env} whenLoaded={() => resolve()} />,
            document.querySelector(`#news`)
          );
        })
      );
    }

    // Pulse project lists
    let pulseProjectList = Array.from(
      document.querySelectorAll(`.pulse-project-list`)
    );

    pulseProjectList.forEach(target => {
      apps.push(
        new Promise(resolve => {
          ReactDOM.render(
            <PulseProjectList
              env={env}
              featured={target.dataset.featured === `True`}
              help={target.dataset.help}
              issues={target.dataset.issues}
              max={parseInt(target.dataset.max, 10)}
              query={target.dataset.query || ``}
              reverseChronological={target.dataset.reversed === `True`}
              whenLoaded={() => resolve()}
              directLink={target.dataset.directLink === `True`}
            />,
            target
          );
        })
      );
    });

    // Share button group
    let shareButtonGroups = document.querySelectorAll(
      `.share-button-group-wrapper`
    );
    if (shareButtonGroups) {
      shareButtonGroups.forEach(element => {
        var props = element.dataset;

        apps.push(
          new Promise(resolve => {
            ReactDOM.render(
              <ShareButtonGroup {...props} whenLoaded={() => resolve()} />,
              element
            );
          })
        );
      });
    }

    //Profile Directory Filter-Bar GA

    const filters = document.querySelectorAll(
      `.profile-directory .fellowships-directory-filter .filter-option button`
    );

    filters.forEach(filter => {
      let year = filter.textContent.trim();
      filter.addEventListener(`click`, () => {
        ReactGA.event({
          category: `profiles`,
          action: `directory filter`,
          label: `${document.title} ${year}`
        });
      });
    });

    //Profile Directory Cards Social Media GA

    function profileCardSocialAnalytics(
      socialTwitter,
      socialLinkedIn,
      profileName
    ) {
      if (socialTwitter) {
        socialTwitter.addEventListener(`click`, () => {
          ReactGA.event({
            category: `profiles`,
            action: `profile tap`,
            label: `${document.title} ${profileName} twitter`,
            transport: `beacon`
          });
        });
      }

      if (socialLinkedIn) {
        socialLinkedIn.addEventListener(`click`, () => {
          ReactGA.event({
            category: `profiles`,
            action: `profile tap`,
            label: `${document.title} ${profileName} linkedin`,
            transport: `beacon`
          });
        });
      }
    }

    //Profile Directory Card Headshot/Name GA

    function bindProfileCardAnalytics(profileCards) {
      // event listener & GA
      let bindAnalytics = (element, profileName) => {
        element.addEventListener(`click`, () => {
          ReactGA.event({
            category: `profiles`,
            action: `profile tap`,
            label: `${document.title} ${profileName} pulse profile`,
            transport: `beacon`
          });
        });
      };

      // adding event listener for each headshot & name
      profileCards.forEach(card => {
        let profileHeadshotElement = card.querySelector(`.headshot-container`);
        let profileNameElement = card.querySelector(`.meta-block-name`);
        let profileName = profileNameElement.textContent.trim();

        [(profileNameElement, profileHeadshotElement)].forEach(target =>
          bindAnalytics(target, profileName)
        );

        let socialTwitter = card.querySelector(`.twitter`);
        let socialLinkedIn = card.querySelector(`.linkedIn`);
        profileCardSocialAnalytics(socialTwitter, socialLinkedIn, profileName);
      });
    }

    // store profile cards
    let profileCards = document.querySelectorAll(`.profiles .person-card`);

    // checks for profile cards in the initial page load
    if (profileCards.length > 0) {
      bindProfileCardAnalytics(profileCards);
    }
    // And start listening for profile filter events,
    // in case profile cards get updated.
    document.addEventListener(`profiles:list-updated`, () => {
      // Refetch the profile cards, because they'll have gone stale.
      profileCards = document.querySelectorAll(`.profiles .person-card`);
      bindProfileCardAnalytics(profileCards);
    });

    // Enable the "load more results" button on index pages
    let loadMoreButton = document.querySelector(`.load-more-index-entries`);
    if (loadMoreButton) {
      const entries = document.querySelector(`.index-entries`);

      // Get the page size from the document, which the IndexPage should
      // have templated into its button as a data-page-size attribute.
      const pageSize = parseInt(loadMoreButton.dataset.pageSize) || 12;

      // Start at page 1, as page 0 is the same sat as the initial page set.
      let page = 1;

      const loadMoreResults = () => {
        loadMoreButton.disabled = true;

        // Construct our API call as a relative URL:
        let url = `./entries/?page=${page++}&page_size=${pageSize}`;

        // And then fetch the results and render them into the page.
        fetch(url)
          .then(result => result.json())
          .then(data => {
            if (!data.has_next) {
              loadMoreButton.removeEventListener(`click`, loadMoreResults);
              loadMoreButton.parentNode.removeChild(loadMoreButton);
            }
            return data.entries_html;
          })
          .then(entries_html => {
            const div = document.createElement(`div`);
            div.innerHTML = entries_html;
            Array.from(div.children).forEach(c => entries.appendChild(c));
          })
          .catch(err => {
            // TODO: what do we want to do in this case?
            console.error(err);
          })
          .finally(() => {
            loadMoreButton.disabled = false;
          });
      };

      loadMoreButton.addEventListener(`click`, loadMoreResults);
    }
  }
};

main.init();
