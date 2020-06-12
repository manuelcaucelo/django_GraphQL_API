# graph_QL Django API using PostgreSQL (POC)


### The Environment

We are using (dev and code):
- pipenv to manage environments
- pre-commit to format code and execute quality code hooks
- isort to sort imports inside code
- black as code formatter
- flake8 to check code quality
- pylint as linter

We are using (packages):
- Django 3.0.7 as base
- Graphene django to manage GraqhQL API
- Django Filters extension from Django
- django-graphql-auth and django-graphql-jwt to manage authentication and tokens
- django-channels-graphql-ws and graphene-subscriptions to manage API subscriptions


### Preparing developing environment

We are using pipenv but you can prepare the virtual environment using virtualven or whatever:

- (If you dont have pipenv on your system) install pipenv with `pip install pipenv`
- Create local develop environment `pipenv install --dev`
- Synchronize environment `pipenv lock & pipenv sync` (if you need)
- Enter on environment shell: `pipenv shell`


### Launchers

We have created a make file with shortcuts:

- make pipenv `pipenv install --dev`
To launch a Django Fake Mail client where receive local mails and view content

- make mailclient `python -m smtpd -n -c DebuggingServer localhost:1025`
To launch a Django Fake Mail client where receive local mails and view content

- make precommit `pre-commit run --all-files`
On environment always use before commit. If you dont and do commit before run pre-commit, pre-commit is auto-triggered

- make shell `manage.py shell`
Open a Django Python shell

- make test `manage.py shell`
Launch the test suite with coverage

- make migrations `manage.py makemigrations $(ATTRS)`
Make the migrations

- make migrate `manage.py migrate $(ATTRS)`
Execute the migrations
