#!/bin/bash
set -e

echo "Starting entrypoint..."

echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL is ready!"


echo "Waiting for Redis at $REDIS_HOST:$REDIS_PORT..."
until redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping | grep -q PONG; do
  echo "Redis is unavailable - sleeping"
  sleep 1
done
echo "Redis is ready!"


echo "Applying Django migrations..."
python manage.py migrate --noinput --fake-initial

echo "Starting gunicorn in background..."
"$@" &  # command from docker-compose
GUNICORN_PID=$!

echo "Checking backend readiness..."
python - <<END
import urllib.request, sys, time

url = "http://127.0.0.1:8000/health/" 
timeout = 60  # حداکثر زمان انتظار به ثانیه
for _ in range(timeout):
    try:
        urllib.request.urlopen(url)
        print("Backend is responding!")
        break
    except:
        time.sleep(1)
else:
    print("Backend did not respond within 60 seconds", file=sys.stderr)
    sys.exit(1)
END

wait $GUNICORN_PID