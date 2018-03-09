.PHONY: build

install:
	pip install -U -r build-requirements.txt
	python setup.py develop

test:
	py.test --cov=awsdeploy tests/unit

check-code:
	pycodestyle .
	pyflakes .

integration-test:
	py.test -s tests/integration

build-dev:
	docker-compose build awsdeploy

dev: build-dev
	docker-compose run awsdeploy bash

clean:
	rm -fr dist

build: build-dev
	docker-compose run awsdeploy python setup.py sdist bdist_wheel
	docker-compose run awsdeploy pandoc --from=markdown --to=rst --output=build/README.rst README.md

release-pypi: build-dev build
	docker-compose run awsdeploy twine upload dist/*

release-docker:
	docker build --no-cache -t flomotlik/awsdeploy -f Dockerfile.release .
	docker push flomotlik/awsdeploy

release: release-pypi release-docker

whalebrew:
	docker build -t flomotlik/awsdeploy:whalebrew -f Dockerfile.whalebrew .
	whalebrew install -f flomotlik/awsdeploy:whalebrew