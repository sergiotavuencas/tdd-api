run:
	@uvicorn store.main:app --reload

pre-commit-install:
	@poetry run pre-commit install

test:
	@poetry run pytest

test-matching:
	@poetry run pytest -s -rx -k $(K) --pdb store ./tests/
