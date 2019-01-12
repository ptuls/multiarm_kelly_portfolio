all: deps clean style test

clean:
	rm -rf dist/*
	find . -name '*pyc' -delete
	find . -name '.coverage' -delete

deps:
	pip3 install -U pip
	pip3 install wheel
	pip3 install -r requirements.txt
	pip3 install -e .

style:
	flake8 app

package: clean style test
	python3.6 setup.py bdist_wheel
	cp dist/kelly-multiarm-`cat VERSION`-py3-none-any.whl dist/kelly-multiarm-latest-py3-none-any.whl
