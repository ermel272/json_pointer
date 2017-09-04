MIN_COVER = 80

install:
	@pip install -e .

install-dev:
	@pip install -e .[dev]

install-test:
	@pip install -e .[test]

run-tests: install-test
	@nosetests --with-coverage --cover-inclusive --cover-erase \
	--cover-tests --cover-min-percentage=$(MIN_COVER)
