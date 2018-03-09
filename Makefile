.PHONY: build

install:
	pip install -U -r build-requirements.txt
	python setup.py develop

test:
	py.test --cov=deployto tests/unit

check-code:
	pycodestyle .
	pyflakes .

integration-test:
	py.test -s tests/integration

build-dev:
	docker-compose build deployto

dev: build-dev
	docker-compose run deployto bash

clean:
	rm -fr dist

build: build-dev
	docker-compose run deployto python setup.py sdist bdist_wheel
	docker-compose run deployto pandoc --from=markdown --to=rst --output=build/README.rst README.md

release-pypi: build-dev build
	docker-compose run deployto twine upload dist/*

release-docker:
	docker build --no-cache -t theserverlessway/deployto -f Dockerfile.release .
	docker push theserverlessway/deployto

release: release-pypi release-docker

whalebrew:
	docker build -t theserverlessway/deployto:whalebrew -f Dockerfile.whalebrew .
	whalebrew install -f theserverlessway/deployto:whalebrew