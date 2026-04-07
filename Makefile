# Variables
PYTHON=python

# Default target
all: run

# Install dependencies
install:
	$(PYTHON) -m pip install -r requirements.txt

# Run ETL pipeline
etl:
	$(PYTHON) -m etl.pipeline

# Run Flask app
run:
	$(PYTHON) -m api.app

# Run everything (ETL + app)
start:
	$(PYTHON) -m etl.pipeline
	$(PYTHON) -m api.app

# Clean cache files
clean:
	find . -name "__pycache__" -exec rm -rf {} +