.PHONY: test clean

test:
	pytest

clean: clean-dist
	rm -rf __pycache__ .pytest_cache .mypy_cache ./**/__pycache__
	rm -f .coverage coverage.xml ./**/*.pyc
	rm -rf .tox

clean-dist:
	rm -rf dist readwise_reader_cli.egg-info

check-dist:
	twine check dist/*

build-dist: clean-dist
	python -m build

upload-dist:
	twine upload dist/*

upload-test-dist:
	twine upload -r testpypi dist/*

test-publish: test clean-dist build-dist check-dist upload-test-dist clean-dist

publish: test clean-dist build-dist upload-dist check-dist
