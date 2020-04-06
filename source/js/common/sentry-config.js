import * as Sentry from "@sentry/browser";

function initializeSentry(dsn, release, environment) {
  Sentry.init({
    dsn,
    release,
    environment,
    ignoreErrors: [
      "tgetT is not defined",
      "Unexpected token 'else'",
      "Object doesn't support property or method 'forEach'",
      /Cannot redefine non-configurable property '[a-zA-Z\d_]+'/,
      /^An invalid or illegal selector was specified.+$/
    ]
  });
}

export default initializeSentry;
