#!/usr/bin/make -f

path = DjangoGraphql

pipenvpipenv:
	$(RUN_COMMAND) pipenv install --dev

migrations:
	$(RUN_COMMAND) python $(path)/manage.py makemigrations $(ATTRS)

migrate:
	$(RUN_COMMAND) python $(path)/manage.py migrate $(ATTRS)

test:
	$(RUN_COMMAND) $(path)/pytest $(ATTRS)

shell:
	$(RUN_COMMAND) python $(path)/manage.py shell

mailserver:
	$(RUN_COMMAND) python -m smtpd -n -c DebuggingServer localhost:1025

precommit:
	$(RUN_COMMAND) pre-commit run --all-files