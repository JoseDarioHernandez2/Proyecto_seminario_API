install:
	poetry install

run-api:
	poetry run uvicorn SRC.API.main:app --reload --host 127.0.0.1 --port 8000
	
run-ui:
	poetry run streamlit run APP/app.py
	
test:
	poetry run pytest -v

test-api:
	poetry run pytest tests/test_api_contract.py -v

format:
	poetry run black .

lint:
	poetry run ruff check .

clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache .ruff_cache .mypy_cache .DS_Store

run-all:
	poetry run uvicorn SRC.API.main:app --reload --host 127.0.0.1 --port 8000 &
	poetry run streamlit run APP/app.py
