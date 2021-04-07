## Scheduled tasks

### Delete non-staff management command

Every sunday, a script runs on prod dyno to remove non-staff accounts created on the Foundation site. An account is considered staff if one of those conditions is true:
- it's an `@mozillafoundation.org` email,
- `is_staff` is at True,
- the account is in a group.
