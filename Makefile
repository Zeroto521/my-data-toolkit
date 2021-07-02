pkg = dtoolkit

help:
	@echo "'clean' - remove all cached files"
	@echo "'clean-build' - remove build artifacts"
	@echo "'clean-pyc' - remove Python file artifacts"
	@echo "'dist' - build package"
	@echo "'test' - run tests and check coverage"
	@echo "'info' - show conda environment and $(pkg) information"

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean: clean-build clean-pyc
	rm -rf coverage.xml
	rm -rf .coverage

test:
	pytest -v -r s -n auto --color=yes --cov=$(pkg) --cov-append --cov-report term-missing --cov-report xml $(pkg)

dist: clean
	python setup.py sdist bdist_wheel
	ls -l dist

info:
	python -V
	python -c "import $(pkg); print($(pkg).__version__)"
	conda info
	conda list
