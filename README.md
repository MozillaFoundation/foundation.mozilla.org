# New Mozilla Foundation Website Prototype
Clone and checkout this branch to a directory separate from your working foundation.mozilla.org environment.

## To Build / Re-build
1) Run `./clean_install.sh`
2) This should remove your old env, create a new one, and start the server

## Misc. Commands
### To enter environment to run commands
1) Run `source env/bin/activate`

### To start dev server without re-building
1) Run `python manage.py runserver`

### To login to admin dashboard
1) Go to `http://localhost:8000/admin/`
2) Enter for user/pass: `admin/admin`
