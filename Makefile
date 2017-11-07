clean:
	rm -rf dist forrest.egg-info

all: clean
	 python setup.py sdist

upload:
	twine upload --repository pypi dist/*
