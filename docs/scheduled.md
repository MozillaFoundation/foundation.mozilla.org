## Scheduled tasks

### Delete non-staff management command

Every sunday, a script runs on prod dyno to remove non-staff accounts created on the Foundation site. An account is considered staff if one of those conditions is true:
- it's an `@mozillafoundation.org` email,
- `is_staff` is at True,
- the account is in a group.

### Generating vote statistics for Data Studio

The `generate_pni_report` management task can run periodically to summarize vote totals for each product in the buyer's guide.
Data is inserted or updated into the database specified By `PNI_STATS_DB_URL`.
You must also have the `USE_COMMENTO` variable set.

The database should have the following schema:

```postgresql
create table product_stats
(
  id               integer not null constraint product_stats_pkey primary key,
  product_name     varchar(100),
  creepiness       integer,
  creepiness_votes integer,
  would_buy        integer,
  would_not_buy    integer
);

create table comment_counts
(
  url            varchar(2048) not null constraint comment_counts_pkey primary key,
  title          varchar(255),
  total_comments integer
);

```
