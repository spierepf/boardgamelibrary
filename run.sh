#!/bin/bash
set -m
./reset.sh
python manage.py runserver &
sleep 2
curl -X POST http://localhost:8000/testOnly/createUser/ -H 'Content-Type: application/json' -d '{"username":"test@example.com", "password":"password", "groups":["ADMIN"]}'
fg python
