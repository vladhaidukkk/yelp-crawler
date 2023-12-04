install:
	@pip install -r requirements.txt

compile:
	@rm -f requirements*.txt
	@pip-compile requirements.in

sync:
	@pip-sync requirements*.txt
