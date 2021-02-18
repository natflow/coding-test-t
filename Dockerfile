FROM amazon/aws-lambda-python:3.8 AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt pip

COPY app /app/app



FROM base AS test

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY pytest.ini .

# run with in-memory database
ENTRYPOINT SQLALCHEMY_DATABASE_URL=sqlite:// pytest



FROM test AS dev

COPY movies.db .

ENTRYPOINT ["uvicorn", "--host=0.0.0.0", "--port=8000", "--reload", "app.main:app"]

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://0.0.0.0:8000/docs



FROM base AS prod

CMD ["app.main.handler"]
