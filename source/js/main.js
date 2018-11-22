/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from 'react';
import ReactGA from 'react-ga';
import ReactDOM from 'react-dom';
import Cookies from 'js-cookie';
import Analytics from './analytics.js';

import JoinUs from './components/join/join.jsx';
import Petition from './components/petition/petition.jsx';
import People from './components/people/people.jsx';
import Takeover from './components/takeover/takeover.jsx';
import MemberNotice from './components/member-notice/member-notice.jsx';
import MultipageNav from './components/multipage-nav/multipage-nav.jsx';
import News from './components/news/news.jsx';
import SingleFilterFellowList from './components/fellow-list/single-filter-fellow-list.jsx';
import PulseProjectList from './components/pulse-project-list/pulse-project-list.jsx';
import injectDonateModal from './donate-modal/donate-modal.jsx';

import primaryNav from './primary-nav.js';

const SHOW_MEMBER_NOTICE = false;

// To be populated via XHR...
let env, networkSiteURL;

let main = {
  init() {
    this.fetchEnv((envData) => {
      env = envData;
      networkSiteURL = env.NETWORK_SITE_URL;

      // HEROKU_APP_DOMAIN is used by review apps
      if (!networkSiteURL && env.HEROKU_APP_NAME) {
        networkSiteURL = `https://${env.HEROKU_APP_NAME}.herokuapp.com`;
      }

      this.injectReactComponents();
      this.bindGlobalHandlers();
      this.decorateExternalLinks();

      Analytics.initialize();
      this.bindGAEventTrackers();
    });
  },

  decorateExternalLinks() {
    Array.from( document.querySelectorAll(`a`) ).forEach((link) => {
      let href = link.getAttribute(`href`);

      // Define an external link as any URL with `//` in it
      if (href && href.match(/\/\//) && !href.match(`//${env.TARGET_DOMAIN}`)) {
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

    let adjustNavbar = (scrollPosition) => {
      if (scrollPosition > 0) {
        elBurgerWrapper.classList.add(`scrolled`);
      } else {
        elBurgerWrapper.classList.remove(`scrolled`);
      }
    };


    let elCtaAnchor = document.querySelector(`#cta-anchor`);
    let elStickyButton = document.querySelector(`.narrow-sticky-button-container`);
    let noopCtaButton = () => {};
    let adjustCtaButton = noopCtaButton;

    if (elCtaAnchor && elStickyButton) {
      let getAnchorPosition = () => {
        return elCtaAnchor.getBoundingClientRect().top + window.scrollY - window.innerHeight;
      };

      let ctaAnchorPosition = getAnchorPosition();

      window.addEventListener(`resize`, () => {
        ctaAnchorPosition = getAnchorPosition();
      });

      let scrollCtaButton = (scrollPosition) => {
        if (scrollPosition > ctaAnchorPosition) {
          elStickyButton.classList.add(`hidden`);
          adjustCtaButton = noopCtaButton;
        }
      };

      let initCtaButton = (scrollPosition) => {
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

    // Adjust #hero offset on load and window resize to accomodate the sticky header

    let elHero = document.querySelector(`#hero`);
    let elStickyTop = document.querySelector(`.sticky-top`);

    let adjustHero = () => {
      elHero.style.paddingTop = `${elStickyTop.clientHeight}px`;
      elHero.style.marginTop = `-${elStickyTop.clientHeight}px`;
    };

    adjustHero();

    window.addEventListener(`resize`, () => {
      adjustHero();
    });

    // Extra tracking

    document.getElementById(`donate-header-btn`).addEventListener(`click`, () => {
      ReactGA.event({
        category: `donate`,
        action: `donate button tap`,
        label: `${document.title} header`
      });
    });

    document.getElementById(`donate-footer-btn`).addEventListener(`click`, () => {
      ReactGA.event({
        category: `donate`,
        action: `donate button tap`,
        label: `${document.title} footer`
      });
    });
  },

  bindGAEventTrackers() {
    if (document.querySelector(`#see-more-modular-page`)) {
      document.querySelector(`#see-more-modular-page`).addEventListener(`click`, () => {
        let label = ``;
        let pageHeader = document.querySelector(`.cms h1`);

        if (pageHeader) {
          label = `${pageHeader.innerText} - footer cta`;
        }

        Analytics.sendGAEvent(`navigation`, `page footer cta`, label);
      });
    }
  },

  // Embed various React components based on the existence of containers within the current page
  injectReactComponents() {
    if (SHOW_MEMBER_NOTICE && document.getElementById(`member-notice`)) {
      ReactDOM.render(<MemberNotice />, document.getElementById(`member-notice`));
    }

    // Show Takeover for new visitors
    if (env.SHOW_TAKEOVER && !Cookies.get(`seen-takeover`) && document.querySelector(`#view-home .takeover`)) {
      let elWrapper = document.querySelector(`#view-home > .wrapper`);

      // Don't allow the content block to scroll
      elWrapper.style.overflow = `hidden`;
      elWrapper.style.height = `100vh`;

      let onTakeoverHide = () => {
        // Allow scrolling again when the takeover is dismissed
        elWrapper.style.overflow = null;
        elWrapper.style.height = null;
      };

      ReactDOM.render(<Takeover onHide={onTakeoverHide} />, document.querySelector(`#view-home .takeover`));
      Cookies.set(`seen-takeover`, `true`, { expires: 365 });
      ReactGA.pageview(`/welcome-splash`);
    }

    // Embed additional instances of the Join Us box that don't need an API exposed (eg: Homepage)
    if (document.querySelectorAll(`.join-us:not(#join-us)`)) {
      var elements = Array.from(document.querySelectorAll(`.join-us:not(#join-us)`));

      if (elements.length) {
        elements.forEach(element => {
          var props = element.dataset;

          ReactDOM.render(<JoinUs {...props} isHidden={false} />, element);
        });
      }
    }

    // petition elements
    var petitionElements = Array.from(document.querySelectorAll(`.sign-petition`));
    var subscribed = false;

    if (window.location.search.indexOf(`subscribed=1`) !== -1) {
      subscribed = true;
    }

    petitionElements.forEach(element => {
      var props = element.dataset;

      props.apiUrl = `${networkSiteURL}/api/campaign/petitions/${props.petitionId}/`;

      ReactDOM.render(<Petition {...props} isHidden={false} subscribed={subscribed}/>, element);
    });

    if (document.getElementById(`people`)) {
      ReactDOM.render(<People env={env} />, document.getElementById(`people`));
    }

    // Multipage nav used in landing pages
    if (document.querySelector(`#multipage-nav`)) {
      let links = [];

      links = [].map.call(document.querySelectorAll(`#multipage-nav a`), (child) => {
        return {
          label: child.textContent.trim(),
          href: child.getAttribute(`href`),
          isActive: !!child.getAttribute(`class`).match(/multipage-link-active/),
          isHighlighted: !child.getAttribute(`class`).match(/multipage-link-active-no-highlight/)
        };
      });

      ReactDOM.render(<MultipageNav links={links} />, document.querySelector(`#multipage-nav-mobile .container .row .col-12`));
    }

    // News
    if (document.querySelector(`#news`)) {
      ReactDOM.render(<News env={env} />, document.querySelector(`#news`));
    }

    // Fellowships single filter fellow list
    let singleFilterFellowList = Array.from(
      document.querySelectorAll(`.single-filter-fellow-list`)
    );

    singleFilterFellowList.forEach(target => {
      return ReactDOM.render(
        <SingleFilterFellowList
          env={env}
          filterType={target.dataset.filterType}
          filterOptions={target.dataset.filterOptions.split(`,`)}
          selectedOption={target.dataset.selectedOption}
        />, target
      );
    });

    // Pulse project lists
    let pulseProjectList = Array.from(
      document.querySelectorAll(`.pulse-project-list`)
    );

    pulseProjectList.forEach(target => {
      ReactDOM.render(
        <PulseProjectList
          env={ env }
          featured={ target.dataset.featured === `True` }
          help={ target.dataset.help }
          issues={ target.dataset.issues }
          max={ parseInt(target.dataset.max, 10) }
          query={ target.dataset.query || `` }
          reverseChronological={ target.dataset.reversed === `True` } />,
        target
      );
    });

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
  }
};

main.init();
