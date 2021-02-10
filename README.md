# Coding Test for T

## Local Development

### System Requirements

* Python 3.7


### Setup

1. Setup virtual environment: `python3 -m venv venv`
1. Activate virtual environment: `source venv/bin/activate`
1. Install requirements: `pip install -r requirements.txt -r requirements-dev.txt`


### Running Locally

1. Follow Setup steps above
1. Start the server: `uvicorn --host=0.0.0.0 --port=8000 --reload app.main:app`
1. In another terminal, check setup and docs: `curl 0.0.0.0:8000/docs`


### Running Tests

1. Follow Setup steps above
1. Run the tests, using an in-memory database: `SQLALCHEMY_DATABASE_URL=sqlite:// pytest`


## Endpoints

Find the documentation self-hosted at `/docs`
