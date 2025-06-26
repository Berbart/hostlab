.PHONY: test ci

test:
pytest -v

ci:
pip install -r requirements.txt
playwright install
pytest -v
