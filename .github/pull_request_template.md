:warning: :warning: :warning:

**HACKTOBER USERS:** PRs WILL BE CLOSED AS SPAM unless you follow proper PR procedures.

- If there is no issue filed, your PR does not fix a documented problem, and will immediately get closed. If there is no issue, and your PR _actually_ fixes something (code or documentation, either is fine), file an issue first.
- If you do not fill out the template, your PR will immediately get closed
- If your PR only fixes a single letter or word instead of fixing all spelling mistakes in that file, your PR will immediately get closed.
- If you do not respond to requests for changes, your PR will get closed.

Filing PRs without following organizational instructions about how to file PRs is not helping open source, it's being a jerk to the people who work hard on keeping open source alive and well.

:warning: :warning: :warning:


Closes #
Related PRs/issues #

## Checklist

_Remove unnecessary checks_

**Tests**
- [ ] Is the code I'm adding covered by tests?

**Changes in Models:**
- [ ] Did I update or add new fake data?
- [ ] Did I squash my migration?
- [ ] [Are my changes backward-compatible](https://github.com/mozilla/foundation.mozilla.org/blob/master/docs/workflow.md#django-migrations-what-to-do-when-working-on-backward-incompatible-migrations). If not, did I schedule a deploy with the rest of the team?

**Documentation:**
- [ ] Is my code documented?
- [ ] Did I update the READMEs or wagtail documentation?
