VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

build:
	$(RM) dist/*
	$(PYTHON) -m pip install --upgrade build
	$(PYTHON) -m build

upload:
	$(PYTHON) -m pip install --upgrade twine
	$(PYTHON) -m twine upload dist/* --verbose

$(VENV)/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

run: venv/bin/activate
	$(PYTHON) app.py

setup: requirements.txt
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf $(VENV)