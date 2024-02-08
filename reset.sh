#!/bin/bash
set -e

for migration in $(git ls-files --others --exclude-standard | grep library/migrations)
do
  rm  $migration
done

rm -f db.sqlite3

python manage.py makemigrations

python manage.py migrate
