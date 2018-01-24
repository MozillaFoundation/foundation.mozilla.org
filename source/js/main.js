/* eslint no-unused-vars: ["error", { "varsIgnorePattern": "React" }] */

import React from 'react';
import ReactGA from 'react-ga';
import ReactDOM from 'react-dom';
import Cookies from 'js-cookie';

import JoinUs from './components/join/join.jsx';
import PrimaryNav from './components/nav/nav.jsx';
import People from './components/people/people.jsx';
import Takeover from './components/takeover/takeover.jsx';
import MemberNotice from './components/member-notice/member-notice.jsx';
import MultipageNav from './components/multipage-nav/multipage-nav.jsx';
import Highlights from './components/highlights/highlights.jsx';
import Leaders from './components/leaders/leaders.jsx';
import HomeNews from './components/home-news/home-news.jsx';
import News from './components/news/news.jsx';
import Upcoming from './components/upcoming/upcoming.jsx';
import Person from './components/people/person.jsx';

const SHOW_MEMBER_NOTICE = false;

// To be populated via XHR...
let env, networkSiteURL;

let main = {
  init () {
    this.fetchEnv((envData) => {
      env = envData;
      networkSiteURL = env.NETWORK_SITE_URL;

      // HEROKU_APP_DOMAIN is used by review apps
      if (!networkSiteURL && env.HEROKU_APP_NAME) {
        networkSiteURL = `https://${env.HEROKU_APP_NAME}.herokuapp.com`;
      }

      this.fetchHomeDataIfNeeded((data) => {
        this.injectReactComponents(data);
        this.bindGlobalHandlers();
      });
    });
  },

  fetchEnv (callback) {
    let envReq = new XMLHttpRequest();

    envReq.addEventListener(`load`, () => {
      callback.call(this, JSON.parse(envReq.response));
    });

    envReq.open(`GET`, `/environment.json`);
    envReq.send();
  },

  fetchHomeDataIfNeeded (callback) {
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

  bindGlobalHandlers () {
    // Close primary nav when escape is pressed
    document.addEventListener(`keyup`, (e) => {
      if (e.keyCode === 27 && !this.reactPrimaryNav.state.isHidden) {
        this.reactPrimaryNav.hide();
      }
    });

    // Track window scroll position and add/remove class to change sticky header appearance

    let lastKnownScrollPosition = 0;
    let ticking = false;
    let elBurgerWrapper = document.querySelector(`.wrapper-burger`);

    let adjustNavbar = (scrollPosition) => {
      // 100px down is the point that the navbar starts to transition to black
      if (scrollPosition > 100) {
        elBurgerWrapper.classList.add(`scrolled`);
      } else {
        elBurgerWrapper.classList.remove(`scrolled`);
      }
    };

    window.addEventListener(`scroll`, () => {
      lastKnownScrollPosition = window.scrollY;

      if (!ticking) {
        window.requestAnimationFrame(() => {
          adjustNavbar(lastKnownScrollPosition);
          ticking = false;
        });
      }

      ticking = true;
    });

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
  },

  // Trigger blurring of page contents when primary nav is toggled
  onPrimaryNavStateChange (event) {
    let elWrapper = document.querySelector(`body > .wrapper`);

    if (event.isHidden) {
      elWrapper.classList.remove(`blurred`);
    } else {
      elWrapper.classList.add(`blurred`);
    }
  },

  // Embed various React components based on the existence of containers within the current page
  injectReactComponents (data) {
    if (document.getElementById(`primary-nav`)) {
      ReactDOM.render(
        <PrimaryNav
          ref={(primaryNav) => { this.reactPrimaryNav = primaryNav; }}
          onStateChange={this.onPrimaryNavStateChange}/>,
        document.getElementById(`primary-nav`)
      );

      if (document.getElementById(`burger`)) {
        document.getElementById(`burger`).addEventListener(`click`, () => {
          this.reactPrimaryNav.toggle();
        });
      }
    }

    if (SHOW_MEMBER_NOTICE && document.getElementById(`member-notice`)) {
      ReactDOM.render(<MemberNotice/>, document.getElementById(`member-notice`));
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

      ReactDOM.render(<Takeover onHide={onTakeoverHide}/>, document.querySelector(`#view-home .takeover`));
      Cookies.set(`seen-takeover`, `true`, { expires: 365 });
      ReactGA.pageview(`/welcome-splash`);
    }

    // Embed additional instances of the Join Us box that don't need an API exposed (eg: Homepage)
    if (document.querySelectorAll(`.join-us:not(#join-us)`)) {
      var elements = Array.from(document.querySelectorAll(`.join-us:not(#join-us)`));

      if(elements.length) {
        elements.forEach(element => {
          var props = element.dataset;

          ReactDOM.render(<JoinUs {...props} isHidden={false} />, element);
        });
      }
    }

    if (document.getElementById(`people`)) {
      ReactDOM.render(<People env={env}/>, document.getElementById(`people`));
    }

    // Multipage nav used in landing pages
    if (document.querySelector(`#multipage-nav`)) {
      let links = [];

      links = [].map.call(document.querySelectorAll(`#multipage-nav div a`), (child) => {
        return {
          label: child.textContent.trim(),
          href: child.getAttribute(`href`),
          isActive: !!child.getAttribute(`class`).match(/active/)
        };
      });

      ReactDOM.render(<MultipageNav links={links} />, document.querySelector(`#multipage-nav-mobile .container .row .col-12`));
    }

    // Homepage

    if (data) {
      // Leaders
      if (document.querySelector(`#featured-people-box`)) {
        ReactDOM.render(<Leaders data={data.leaders}/>, document.querySelector(`#featured-people-box`));
      }

      // Home News
      if (document.querySelector(`#home-news`)) {
        ReactDOM.render(<HomeNews data={data.news}/>, document.querySelector(`#home-news`));
      }

      // Highlights
      if (document.querySelector(`#home-highlights`)) {
        ReactDOM.render(<Highlights data={data.highlights}/>, document.querySelector(`#home-highlights`));
      }
    }

    // Upcoming
    if (document.querySelector(`#upcoming`)) {
      ReactDOM.render(<Upcoming env={env}/>, document.querySelector(`#upcoming`));
    }

    // News
    if (document.querySelector(`#news`)) {
      ReactDOM.render(<News env={env}/>, document.querySelector(`#news`));
    }

    // Science Fellowship
    if (document.getElementById(`featured-science-fellow`)) {
      let metadata = {
        featured: true,
        'internet_health_issues': [ `Decentralization`, `Open Innovation` ],
        links: [],
        name: `Firstname Surname`,
        role: `[Area Fellowship] Fellow, [Year]`,
        location: `City, Country`,
        image: `https://images.pexels.com/photos/264206/pexels-photo-264206.jpeg?w=500`,
        quote: `Quote quote quote quote quote quote quote quote quote quote quote quote.`,
        affiliations: [ `Stanford University Professor; YouthLAB founder`]
      };

      ReactDOM.render(<Person metadata={metadata} />, document.getElementById(`featured-science-fellow`));
    }
  }
};

main.init();

// Append Google Analytics code
import './analytics.js';
