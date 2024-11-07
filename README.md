# The creatify iterview mini project.

#### run step：
##### 1.run docker: docker-compose up --build
##### 2.user signup:
```
req:
curl --location 'http://127.0.0.1:8000/signup/' \
--data-raw '{
    "email": "test@test.com",
    "password": "123"
}'
rsp:
{"userid":1,"email":"test@test.com"}
```
##### 3.user signin:
```
req:
curl --location 'http://127.0.0.1:8000/signin/' \
--data-raw '{
    "email": "test@test.com",
    "password": "123"
}'
rsp:
{"access_token": "xxxx", "refresh_token": "xxxx"}
```
##### 3.get me info:
```
req:
curl --location 'http://127.0.0.1:8000/me/' \
--header 'Authorization: Bearer <access_token_from_signin>'
rsp:
{"id": 1, "email": "test@test.com"}
```
