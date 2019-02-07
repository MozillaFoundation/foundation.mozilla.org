## Development

This project is based on [Wagtail](https://wagtail.io/), which is itself based on Django, so the documentation for both projects applies.
 If you're new to Django, Django official documentation provide a [tutorial](https://docs.djangoproject.com/en/2.0/intro/) and a handful of [topics](https://docs.djangoproject.com/en/2.0/topics/) and [how-to](https://docs.djangoproject.com/en/2.0/howto/) guides to help you get started. If you're completely new to programming, check
 [Django Girls](https://tutorial.djangogirls.org/en/) tutorial.

### Pipenv workflow

Checking [Pipenv documentation](https://docs.pipenv.org/) is highly recommended if you're new to it.

#### Virtual environment

- `pipenv shell` activates your virtual environment and automatically loads your `.env`. Run `exit` to leave it. You don't need to be in your virtual environment to run python commands: Use `pipenv run python [...]` instead.

#### Installing dependencies

- `pipenv install [package name]`

After installing a package, pipenv automatically runs a `pipenv lock` that updates the `pipfile.lock`. You need to add both `pipfile` and `pipfile.lock` to your commit.

#### Updating dependencies

- `pipenv update --outdated` to list dependencies that need to be updated,
- `pipenv update` to update dependencies

If a dependency is updated, pipenv automatically runs a `pipenv lock` that updates the `pipfile.lock`. You need to add both `pipfile` and `pipfile.lock` to your commit.

#### Listing installed dependencies

- `pipenv graph`

### Overriding templates and static content

Sometimes it is necessary to override templates or static js/css/etc assets. In order to track *what* we changed in these files please surround your changes with:

```
# override: start #123
... override code here...
# override: end #123
```

Where `#...` is an issue number pointing to the issue that these changes are being made for.
