## Scheduled tasks

We use heroku scheduler to run periodic tasks. See the "Heroku Scheduler" addon for each app for schedule commands.

### Delete non-staff management command

Every day a script runs on prod remove non-staff accounts created on the Foundation site. An account is considered staff if one of those conditions is true:
- it's an `@mozillafoundation.org` email,
- `is_staff` is set to `True`,
- the account is in a group (and thus had someone explicitly set permissionss for them).

### Synchronize the Wagtail locale trees

We synchronize our content tree to all locales on an hourly basis

### Publish scheduled pages

This runs hourly

### Update the Block Inventory

This runs daily
