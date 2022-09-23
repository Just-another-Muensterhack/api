#!/bin/sh

# check if all required environment variables are configured
failed=0
if [ -z "${POSTGRES_HOST}" ]; then
  echo "Missing environment variable: POSTGRES_HOST"
  failed=1
fi
if [ -z "${POSTGRES_PORT}" ]; then
  echo "Missing environment variable: POSTGRES_PORT"
  failed=1
fi
if [ -z "${POSTGRES_USER}" ]; then
  echo "Missing environment variable: POSTGRES_USER"
  failed=1
fi
if [ -z "${POSTGRES_NAME}" ]; then
  echo "Missing environment variable: POSTGRES_NAME"
  failed=1
fi
if [ ${failed} -ne 0 ]; then
  exit 1
fi

echo "Waiting for postgres..."

# shellcheck disable=SC2153
while ! nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
  sleep 0.1
done

echo "postgres started"

# shellcheck disable=SC2198
if [ -z "${@}" ]; then
  uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug
else
  exec "${@}"
fi
