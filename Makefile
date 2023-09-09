.PHONY: test clean

test:
	pytest

clean: clean-dist
	rm -rf .pytest_cache ./**/__pycache__

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
