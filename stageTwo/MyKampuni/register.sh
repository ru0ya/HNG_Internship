#!/usr/bin/bash

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{
           "first_name": "Samuel",
           "last_name": "Doe",
           "email": "testdevru0ya@gmail.com",
           "password": "password123.",
           "phone": "1234567890"
         }' \
     http://127.0.0.1:8000/auth/register
