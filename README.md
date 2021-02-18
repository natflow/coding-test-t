# Coding Test for T

## Local Development

### System Requirements

* Docker


### Running Locally

1. Build the image: `docker build --target dev --tag app:dev .`
1. Start the server: `docker run --volume ${PWD}/app:/app/app --rm --interactive --publish 8000:8000 app:dev`
1. In another terminal, check the docs: `curl 0.0.0.0:8000/docs`

By default, the server will automatically reload when you change the source code.


### Running Tests

1. Build the image: `docker build --target test --tag app:test .`
1. Run the tests: `docker run --volume ${PWD}/app:/app/app --volume ${PWD}/tests:/app/tests --rm --tty app:test`

By default, the tests will use a fresh in-memory database.

For interactive debugging, you can get a shell inside the Docker container: `docker run --volume ${PWD}/app:/app/app --volume ${PWD}/tests:/app/tests --rm --tty --interactive --entrypoint /bin/bash app:test`


## Endpoints

Find the documentation self-hosted at `/docs`
