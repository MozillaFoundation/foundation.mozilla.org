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

import primaryNav from "./primary-nav.js";

const SHOW_MEMBER_NOTICE = false;

// To be populated via XHR...
let env, networkSiteURL;

// Track all ReactDOM.render calls so we can use a Promise.all()
// all the way at the end to make sure we don't report "we are done"
// until all the React stuff is _actually_ done.
const apps = [];

let main = {
  init() {
    this.fetchEnv(envData => {
      env = envData;
      networkSiteURL = env.NETWORK_SITE_URL;

      // HEROKU_APP_DOMAIN is used by review apps
      if (!networkSiteURL && env.HEROKU_APP_NAME) {
        networkSiteURL = `https://${env.HEROKU_APP_NAME}.herokuapp.com`;
      }

      Analytics.initialize();

      this.injectReactComponents();
      this.bindGlobalHandlers();
      this.decorateExternalLinks();
      this.bindGAEventTrackers();

      // Record that we're done, when we're really done.
      Promise.all(apps).then(() => {
        window[`main-js:react:finished`] = true;
      });
    });
  },

  decorateExternalLinks() {
    Array.from(document.querySelectorAll(`a`)).forEach(link => {
      let href = link.getAttribute(`href`);

      // Define an external link as any URL with `//` in it
      if (
        href &&
        href.match(/\/\//) &&
        env.TARGET_DOMAINS.some(domain => !href.match(`//${domain}`))
      ) {
        link.setAttribute(`target`, `_blank`);

        // https://www.jitbit.com/alexblog/256-targetblank---the-most-underestimated-vulnerability-ever/
        link.setAttribute(`rel`, `noopener noreferrer`);
      }
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

    // Call once to get scroll position on initial page load.
    onScroll();

    primaryNav.init();

    // Extra tracking

    document
      .getElementById(`donate-header-btn`)
      .addEventListener(`click`, () => {
        ReactGA.event({
          category: `donate`,
          action: `donate button tap`,
          label: `${document.title} header`
        });
      });

    document
      .getElementById(`donate-footer-btn`)
      .addEventListener(`click`, () => {
        ReactGA.event({
          category: `donate`,
          action: `donate button tap`,
          label: `${document.title} footer`
        });
      });
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
    if (document.querySelectorAll(`.join-us`)) {
      var elements = Array.from(document.querySelectorAll(`.join-us`));

      if (elements.length) {
        elements.forEach(element => {
          var props = element.dataset;

          apps.push(
            new Promise(resolve => {
              ReactDOM.render(
                <JoinUs
                  {...props}
                  isHidden={false}
                  whenLoaded={() => resolve()}
                />,
                element
              );
            })
          );
        });
      }
    }

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

      props.apiUrl = `${networkSiteURL}/api/campaign/petitions/${
        props.petitionId
      }/`;

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

    // Fellowships single filter fellow list
    let singleFilterFellowList = Array.from(
      document.querySelectorAll(`.single-filter-fellow-list`)
    );

    singleFilterFellowList.forEach(target => {
      apps.push(
        new Promise(resolve => {
          ReactDOM.render(
            <SingleFilterFellowList
              env={env}
              filterType={target.dataset.filterType}
              filterOptions={target.dataset.filterOptions.split(`,`)}
              selectedOption={target.dataset.selectedOption}
              whenLoaded={() => resolve()}
            />,
            target
          );
        })
      );
    });

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

    //Profile Directory Filter-Bar GA

    const filters = document.querySelectorAll(
      `.profile-directory .fellowships-directory-filter .filter-option button`
    );

    filters.forEach(filter => {
      let year = filter.textContent.trim();
      filter.addEventListener("click", () => {
        ReactGA.event({
          category: `profiles`,
          action: `directory filter"`,
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

    /*
      The following code has been disabled for
      https://github.com/mozilla/foundation.mozilla.org/issues/2630,
      but we want to keep this code around for when we need to
      re-enable this functionality

      ---
      import injectDonateModal from './donate-modal/donate-modal.jsx';
      ...
      let donationModal = document.querySelector(`.donate-modal-wrapper`);

      if (donationModal) {
        let modalOptions = {
          title: `We all love the web. Join Mozilla in defending it!`,
          subheading: `Let's protect the world's largest resource for future generations. A few times a year, the Mozilla Foundation asks for donations.`,
          cta: {
            title: `Chip in to help us keep the web healthy, wonderful, and welcoming to all.`,
            text: `Support Mozilla`
          },
          utm: {
            medium: `foundation`,
            campaign: `mainsite`,
            content: `popupbutton`
          },
          ga: {
            category: `site`,
            action: `donate tap`,
            label: `donate popup on foundation site`
          }
        };

        injectDonateModal(donationModal, modalOptions);
      }
    */
  }
};

main.init();
