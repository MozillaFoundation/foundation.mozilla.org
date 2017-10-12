# Mozilla Network

[![Build Status](https://travis-ci.org/mozilla/network.svg?branch=master)](https://travis-ci.org/mozilla/network)
[![Dependency Status](https://david-dm.org/mozilla/network.svg)](https://david-dm.org/mozilla/network)
[![Dev Dependency Status](https://david-dm.org/mozilla/network/dev-status.svg)](https://david-dm.org/mozilla/network/?type=dev)
[![Uses Mofo Standards](https://MozillaFoundation.github.io/mofo-standards/badge.svg)](https://github.com/MozillaFoundation/mofo-standards)

* [Development][#development]
* [Setup][#setup]
* [Stack][#stack]
* [HTML][#html]
* [CSS][#css]
* [React][#react]
* [File Structure][#file-structure]
* [Deployment][#deployment]
* [Staging][#staging]
* [Production][#production]
* [Healthcheck][#healthcheck]
* [Environment Variables][#environment-variables]
* [Security][#security]
* [Resolving an Issue][#resolving-an-issue]
* [Unpatched Vulnerabilities][#unpatched-vulnerabilities]

## Development

### Setup

**Requirements**: Node, npm, git.

Run the following terminal commands to get started:

- `git clone https://github.com/mozilla/network.git`
- `cd network`
- `npm start`

This will install all dependencies, build the code, start a server at [http://127.0.0.1:2017](http://127.0.0.1:2017), and launch it in your default browser.

---

### Stack

#### HTML

HTML is generated from [Pug](https://pugjs.org) templates (formerly known as Jade).

Localized strings are pulled from [Java .properties](https://en.wikipedia.org/wiki/.properties) files located in `/locales`.

#### CSS

CSS is generated from [Sass](http://sass-lang.com/). The [Mofo Bootstrap](https://github.com/mozilla/mofo-bootstrap) theme is pulled in by default.

#### React

React is used *à la carte* for isolated component instances (eg: a tab switcher) since this is not a single page application, but rather a static generated website. This precludes the need for Flux architecture, or such libraries as React Router.

To add a React component, you can target a container element from `/source/js/main.js` and inject it.

---

### File Structure

```
/
├── env <- Environment variables
├── dest <- Compiled code generated from source. Don't edit!
├── locales <- Localized strings (Java .properties syntax)
├── scripts <- Scripts run by npm tasks
└── source <- Source code
    ├── images <- Image assets
    ├── js <- JS code
    │   └── components <- React components
    ├── json <- JSON for static data sets
    │   └── temp <- JSON pulled from web services. Don't commit!
    ├── pug <- Pug templates
    └── sass <- Sass code
```

---

### Deployment

#### Staging

Builds to staging are triggered by commits to `master`.

Staging URL is [network.mofostaging.net](https://network.mofostaging.net)

#### Production

Production deployments are triggered by commits to `production`. Pull Requests to production must recieve approval from one of the core development team, and must pass all tests.

Production URL is [network.mozilla.org](https://network.mozilla.org)

##### Healthcheck

A healthcheck route that indicates the most recent commit and other useful information is accessible on `/healthcheck.html`.

---

### Environment Variables

Default environment variables are declared in `env.default`. If you wish to override any of the values, you can create a local `.env` file in the root of the project. This file should not be committed.

The domains used to fetch static content from Network Pulse and the Network API can be customized by specifying `PULSE_API_DOMAIN` and `NETWORK_API_DOMAIN`, respectively. By default it uses `network-pulse-api-production.herokuapp.com` and `network.mofoprod.net`.

When the build runs, a file `env.json` is created in the root, which is the result of merging `.env` and `env.default` and converting the result to JSON. Values declared in `.env` take precedence.

If you wish to use environment variables in either Node or client-side code, you can simply require `env.json`.

---
### Security

[https://snyk.io](https://snyk.io) is used to test our npm and PyPi dependencies for vulnerabilities. These tests are run on Travis and Appveyor, and will cause a build to fail when a new vulnerability is detected.

#### Resolving an issue

If an issue is reported by Snyk, you have several options to remedy the problem. Firstly, the build log should contain a link to the vulnerability report on snyk.io. On that page you will find links to the issue or CVE, and information about how to resolve the problem. You should start a new feature branch and pull request to resolve this issue before merging any other features.

#### Unpatched vulnerabilities

In some cases, vulnerabilities have not been patched - you will need to look at the nature of the issue and then add an exception to the `.snyk` file for it. You can install the snyk cli using `npm install -g snyk` and add the exception like so: `snyk ignore --id="SNYK-PYTHON-BOTO3-40617" --expiry="2017-12-31" --reason="No fix available"` (Replace the `id` and `reason` with relevant information). The `expiry` flag is an [RFC2822](https://tools.ietf.org/html/rfc2822#page-14) formatted date string that will cause the ignore rule to expire - useful so that we can check periodically for fixes to unpatched vulnerabilities in our dependencies.
