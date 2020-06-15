# graph_QL Django API using PostgreSQL (POC)


### The Environment

We are using (dev and code):
- pipenv to manage environments
- pre-commit to format code and execute quality code hooks
- isort to sort imports inside code
- black as code formatter
- flake8 to check code quality
- pylint and extensions as linter
- mixer and pytest (and extensions) for testing

We are using (packages):
- Django 3.0.7 as base
- Graphene django to manage GraqhQL API
- Django Filters extension from Django
- django-graphql-auth and django-graphql-jwt to manage authentication and tokens
- django-channels-graphql-ws and graphene-subscriptions to manage API subscriptions
- psycopg2-binary to connect to PostgreSQL


### How to RUN develop environment

We have created a docker-compose that run three dockers:

**THE API**: graphql_django_api_api_ideas_1

**THE POSTGRESQL DATABASE**: dev_postgresql_container

**FAKE MAIL SERVER TO MANAGE REGISTERS**: dev_mail_container


You must only do a simple...

```docker-compose up```

...and enjoy!

Info of interest:

all fixture users are:

test2, test3, test4... test5@test.com and password is smart@Z1 or smart@z1

Also there is a superadmin user:

manuelcaucelo@gmail.com / smart@z1

In register process a validation email will be send.
I have no integratiosn with mailgun or similar so i used the python mail server to check the email token in the magiclink.

You can see that mail appear making a docker log follow in mail docker.

You can use: 127.0.0.1:8000/graphql or import insomnia collection to check the endpoints.

You can also check in the .env file the connection info to postgreSQL database.

### Launchers

We have created a make file with shortcuts (to play in local):

- make pipenv `pipenv install --dev`
To launch a Django Fake Mail client where receive local mails and view content

- make mailserver `python -m smtpd -n -c DebuggingServer localhost:1025`
To launch a Django Fake Mail server where receive local mails and view content

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


### Extras

- Added a Insomnia JSON file to check the GraphQL endpoints.
- Added fixtures to hace data to play with (docker compose load this data)
- Added special GraphQL template to check subscription.
    * Due to insomnia or simple GraphQL cannot launch subscriptions (has a problem sending headers with channels). We have included a modified version of graphQL to check the subscription. These are the steps:
    1. Login in admin panel with super user:
        manuelcaucelo@gmail.com / smart@z1
    2. Open 127.0.0.1:8000/graphql in your browser and check with "me" Query if we are logged. If not, use AuthToken function.
    After reload again this browser and you can see the me response.
    3. Launch subscription (the browser will remain awaiting news...)
    4. From insomnia use test4@test.com user to to login and create an idea.
    5. You can see the message appears in browser!

### To DO

- Would be nice a coverage of 100% (current 73%). Its bored and its only a demo.
- Would be great add Celery (or another) and Cache.
- I need more time to do a "boy scout refactor"
