# media-sharing-site

This is a personal project for me to learn and practice Python and web development with Django.

## VSCode Setup

### Virtualenv

- Install virtualenv and virtualenvwrapper.
- Create a virtualenv (`mkvirtualenv <env name>`).
- Activate the virtualenv if it's not already active (`workon <env_name>`).
- `pip install -r requirements.txt`

Add the virtualenv path to the workspace settings:

`"python.pythonPath": "/home/nate/.virtualenvs/env_web/bin/python"`

### Linting

This project uses Flake8 for python linting. To enable it correctly, add the following to the workspace settings:

```json
    ...
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.enabled": true,
    ...
```

## Generate and view test coverage

```shell
coverage run --source='.' manage.py test apps
coverage report
```
