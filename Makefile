pkg = dtoolkit

help:
	@echo "'clean' - remove all cached files"
	@echo "'clean-build' - remove build artifacts"
	@echo "'clean-pyc' - remove Python file artifacts"
	@echo "'clean-cov' - remove coverage files"
	@echo "'clean-model' - remove model or pipeline files"
	@echo "'clean-doc' - remove documentation"
	@echo "'lint' - lint source codes"
	@echo "'dist' - build package"
	@echo "'test' - run tests and check coverage"
	@echo "'info' - show conda environment and $(pkg) information"
	@echo "'html' - build html documentation"

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-model:
	find . -name '*.model' -exec rm -f {} +
	find . -name '*.joblib' -exec rm -f {} +
	find . -name '*.pipeline' -exec rm -f {} +

clean-cov:
	rm -rf coverage.xml
	rm -rf .coverage

clean-doc:
	cd doc && make clean
	rm -rf doc/source/reference/api

clean: clean-build clean-pyc clean-cov clean-model clean-doc

lint:
	pre-commit run -a -v

test:
	pytest -v -r a -n auto --color=yes --cov=$(pkg) --cov-append --cov-report term-missing --cov-report xml $(pkg)

doctest:
	pytest -v -r a -n auto --color=yes --cov=$(pkg) --cov-append --cov-report xml --doctest-only $(pkg)

dist:
	python setup.py sdist bdist_wheel
	ls -l dist

info:
	python -V
	python -c "import $(pkg); print($(pkg).__version__)"
	conda info
	conda list

html:
	cd doc && make html
