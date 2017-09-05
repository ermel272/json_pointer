MIN_COVER = 98

install:
	@pip install -e .

install-dev:
	@pip install -e .[dev]

install-test:
	@pip install -e .[test]

install-full:
	@pip install -e .[dev,test]

run-tests: install-test
	@nosetests --with-coverage --cover-inclusive --cover-erase \
	--cover-tests --cover-min-percentage=$(MIN_COVER)
