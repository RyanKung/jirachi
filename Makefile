run:
	python -m jirachi
test:
	python -m tests --log-level INFO --test-timeout 120
upload:
	python setup.py sdist --formats=gztar register upload
