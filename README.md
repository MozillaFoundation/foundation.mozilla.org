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

Managed content comes from: `network.mofoprod.net`, and `network-pulse-api-production.herokuapp.com`.

#### Production

Production deployments are triggered manually via a [Jenkins job](https://jenkins.mofoprod.net/view/STAGING/job/Network%20(production)/). Deployments are made to "network-production" in us-east-1, served using a CloudFront CDN.

Temporary production URL is [network.mofoprod.net](https://network.mofoprod.net)

Managed content comes from: `network.mofoprod.net`, and `network-pulse-api-production.herokuapp.com`.

#### Dev

Dev deployments for smoke testing API code changes are triggered manually via a [Jenkins job](https://jenkins.mofoprod.net/view/STAGING/job/Network%20(dev)/). Deployments are made to "network-smoketest" in us-east-1, served using a CloudFront CDN.

Dev URL is [network-dev.mofostaging.net](https://network-dev.mofostaging.net)

Managed content comes from: `network-api.mofostaging.net`, and `network-pulse-api-production.herokuapp.com`.

##### Healthcheck

A healthcheck route that indicates the most recent commit and other useful information is accessible on `/healthcheck.html`.

### Environment Variables

Default environment variables are declared in `defaults.env`. If you wish to override any of the values, you can create a local `.env` file in the root of the project. This file should not be committed.

The domains used to fetch static content from Network Pulse and the Network API can be customized by specifying `PULSE_API_DOMAIN` and `NETWORK_API_DOMAIN`, respectively. By default it uses `network-pulse-api-production.herokuapp.com` and `network.mofoprod.net`.

When the build runs, a file `env.json` is created in the root, which is the result of merging `.env` and `defaults.env` and converting the result to JSON. Values declared in `.env` take precedence.

If you wish to use environment variables in either Node or client-side code, you can simply require `env.json`.
