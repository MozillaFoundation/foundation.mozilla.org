## Development

### Pipenv and Invoke commands

Pipenv pattern to run Django management commands is:

- `pipenv run python [path to manage.py] [manage.py command] [options]`

For example, you can run your development server that way:

- `pipenv run python network-api/manage.py runserver`

But it's a bit long. So instead, you can use invoke:

- `inv runserver`

### Invoke tasks available:

- `inv -l`: list available invoke tasks
- `inv makemigrations`: Creates new migration(s) for apps
- `inv migrate`: Updates database schema
- `inv runserver`: Start a web server
- `inv setup`: Prepare your dev environment after a fresh git clone
- `inv test`: Run tests
- `inv catch-up`: Install dependencies and apply migrations

For management commands not covered by an invoke tasks, use `inv manage [command]` (example: `inv manage load_fake_data`). You can pass flag and options to management commands using `inv manage [command] -o [positional argument] -f [optional argument]`. For example:
- `inv manage runserver -o 3000`
- `inv manage load_fake_data -f seed=VALUE`
- `inv manage migrate -o news`
