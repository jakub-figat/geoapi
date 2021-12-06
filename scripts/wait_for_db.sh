#!/usr/bin/env sh

set -o errexit
set -o nounset


postgres_ready () {
  nc -z -i 2 "$POSTGRES_HOST" "$POSTGRES_PORT"
}

until postgres_ready; do
  echo "Postgres is unavailable, waiting..."
done

exec "$@"