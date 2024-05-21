run:
	@uvicorn store.main:app --reload

pre-commit-install:
	@poetry run pre-commit install
