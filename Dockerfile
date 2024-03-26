FROM docker:26-cli

RUN apk add --update --no-cache python3 py-pip

RUN pip install --no-cache-dir --break-system-packages \
    dagster \
    dagster-postgres \
    dagster-docker

WORKDIR /opt/dagster/app

COPY repo.py /opt/dagster/app

EXPOSE 4000

# hardcoding these here is kind of hacky - need to figure out a way to pass these to
# containers spun up for job steps (via docker_executor?)
ENV DAGSTER_PG_USERNAME="postgres_user" \
        DAGSTER_PG_PASSWORD="postgres_password" \
        DAGSTER_PG_DB="postgres_db" \
        DAGSTER_PG_HOST="db"


CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "repo.py"]
