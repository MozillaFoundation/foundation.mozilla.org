# Mozilla Network

[![Build Status](https://travis-ci.org/mozilla/network.svg?branch=master)](https://travis-ci.org/mozilla/network)
[![Uses Mofo Standards](https://MozillaFoundation.github.io/mofo-standards/badge.svg)](https://github.com/MozillaFoundation/mofo-standards)

## Development

### Setup

**Requirements**: Node, npm, git.

Run the following terminal commands to get started:

- `git clone https://github.com/mozilla/network.git`
- `cd network`
- `npm start`

This will install all dependencies, build the code, start a server at [http://127.0.0.1:2017](http://127.0.0.1:2017), and launch it in your default browser.

### Stack

#### HTML

HTML is generated from [Pug](https://pugjs.org) templates (formerly known as Jade).

Localized strings are pulled from [Java .properties](https://en.wikipedia.org/wiki/.properties) files located in `/locales`.

#### CSS

CSS is generated from [Sass](http://sass-lang.com/). The [Mofo Bootstrap](https://github.com/mozilla/mofo-bootstrap) theme is pulled in by default.

#### React

React is used *à la carte* for isolated component instances (eg: a tab switcher) since this is not a single page application, but rather a static generated website. This precludes the need for Flux architecture, or such libraries as React Router.

To add a React component, you can target a container element from `/source/js/main.js` and inject it.

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

### Deployment

#### Staging

Builds to staging are triggered by commits to `master`. A [Jenkins job](https://jenkins.mofoprod.net/view/STAGING/job/Network%20(staging)/) deploys to the "network-staging" S3 bucket in us-east-1, which is served using a CloudFront CDN.

Staging URL is [network.mofostaging.net](https://network.mofostaging.net)

##### gh-pages "personal" staged builds

A build can be deployed to GitHub Pages on any fork by running:

`npm run stage REMOTE` (Change `REMOTE` to match your desired target)

This is typically useful for creating staged builds of unmerged features for design review.

#### Production

Production deployments are triggered manually via a [Jenkins job](https://jenkins.mofoprod.net/view/STAGING/job/Network%20(production)/). Deployments are made to "network-production" in us-east-1, served using a CloudFront CDN.

Temporary production URL is [network.mofoprod.net](https://network.mofoprod.net)

#### Environment Variables

The domains used to fetch static content from Network Pulse and the Network API can be customized by specifying `PULSE_API_DOMAIN` and `NETWORK_API_DOMAIN`, respectively. By default it uses `network-pulse-api-production.herokuapp.com` and `network.mofoprod.net`.
