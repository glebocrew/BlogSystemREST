# Rest API Blog System
#### Developer: @glebocrew
#### Gritsenko Gleb Mikhailovich, 11-i-3
----

## How to run a project
Firstly, clone the project from a repository
```bash
git clone https://github.com/glebocrew/BlogSystemREST
```

After that, create your venv and install requirements
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```
```bash
pip install requirements.txt
```

Then, insert your database into confs/conf.json
```json
"conn": {
    "host": "host",
    "port": 1111,
    "user": "user",
    "password": "password",
    "database": "test"
}
```

After that, run `init.py`
```bash
python3 init.py
```
And see logs in logs/init_logs.txt

To start an app type
```bash
uvicorn main:app --reload
```
Enjoy!

## API
This project provides a comfy API
All of it is in the /api route
There are:
1. /api/users
    - GET /api/users -- gets all users
    - GET /api/users/{id} -- gets sertain user
    - PUT /api/users/?email={email}&login={login}&password={password} -- creates new user
    - PATCH /api/users/{id}?email={email}&login={login}&password={password} -- changes some fields of one user
    - DELETE /api/users/{id} -- deletes one user
2. /api/posts
    - GET /api/posts -- gets all posts
    - GET /api/posts/{id} -- gets the post
    - PUT /api/posts/?authorId={authorId}&title={title}&content={content} -- creates new post
    - PATCH /api/posts/{id}?title={title}&content={content} -- changes some fields of a post
    - DELETE /api/posts/{id} -- deletes one post
Also, visit, /docs

## HTMLs
To watch how site looks with my awful design visit / (root route)

## Cases&Runs of API
### GET /api/users
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/users' \
  -H 'accept: application/json'
```

```json
[
  [
    {
      "id": "bc6554dd-017d-4d7e-8301-aa204b601161",
      "email": "glebocrew@yandex.ru",
      "login": "glebocrew",
      "password": "3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2",
      "createdAt": "2025-10-01T23:03:38",
      "updatedAt": "2025-10-01T23:03:38"
    },
  ],
  200
]
```

### GET users/user/{id}
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/users/bc6554dd-017d-4d7e-8301-aa204b601161' \
  -H 'accept: application/json'
```

```json
[
  {
    "id": "bc6554dd-017d-4d7e-8301-aa204b601161",
    "email": "glebocrew@yandex.ru",
    "login": "glebocrew",
    "password": "3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2",
    "createdAt": "2025-10-01T23:03:38",
    "updatedAt": "2025-10-01T23:03:38"
  }
]
```
---
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/users/incorrect' \
  -H 'accept: application/json'
```

```json
{
  "detail": "User not found"
}
```
\+ 404 status


### PUT /api/users/?email={email}&login={login}&password={password}

```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/api/users/?email=glebocrew%40gmail.com&login=glebocrew&password=123123' \
  -H 'accept: application/json'
```

```json
[
  "OK",
  201
]
```

Check this!
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/users' \
  -H 'accept: application/json'
```

```json
[
  [
    {
      "id": "75598b6b-3d53-418d-86bc-7de7c5869685",
      "email": "glebocrew@gmail.com",
      "login": "glebocrew",
      "password": "263fec58861449aacc1c328a4aff64aff4c62df4a2d50b3f207fa89b6e242c9aa778e7a8baeffef85b6ca6d2e7dc16ff0a760d59c13c238f6bcdc32f8ce9cc62",
      "createdAt": "2025-10-02T01:49:14",
      "updatedAt": "2025-10-02T01:49:14"
    }
  ],
  200
]
```

---

If we try to insert same data
```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/api/users/?email=glebocrew%40gmail.com&login=glebocrew&password=123123' \
  -H 'accept: application/json'
```
```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/api/users/?email=glebocrew%40gmail.com&login=glebocrew&password=123123' \
  -H 'accept: application/json'
```

So, we could repeat this command numerous times, but the result will be
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/users' \
  -H 'accept: application/json'
```

```json
[
  [
    {
      "id": "75598b6b-3d53-418d-86bc-7de7c5869685",
      "email": "glebocrew@gmail.com",
      "login": "glebocrew",
      "password": "263fec58861449aacc1c328a4aff64aff4c62df4a2d50b3f207fa89b6e242c9aa778e7a8baeffef85b6ca6d2e7dc16ff0a760d59c13c238f6bcdc32f8ce9cc62",
      "createdAt": "2025-10-02T01:49:14",
      "updatedAt": "2025-10-02T01:49:14"
    }
  ],
  200
]
```
That's because emails can't repeat

---

### PATCH /api/users/{id}?email={email}&login={login}&password={password}

```bash
curl -X 'PATCH' \
  'http://127.0.0.1:8000/api/users/fdg?email=dsfg&login=sdfg&password=sdf' \
  -H 'accept: application/json'
```

```json
{
  "detail": "User not found"
}
```
\+ 404 status

---

```bash
curl -X 'PATCH' \
  'http://127.0.0.1:8000/api/users/75598b6b-3d53-418d-86bc-7de7c5869685?email=new_mail%40glebocrew.ru' \
  -H 'accept: application/json'
```

```json
[
  {
    "message": "User updated successfully"
  },
  200
]
```

Lets check this
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/users' \
  -H 'accept: application/json'
```

```json
[
  [
    {
      "id": "75598b6b-3d53-418d-86bc-7de7c5869685",
      "email": "new_mail@glebocrew.ru",
      "login": "glebocrew",
      "password": "094aa5f5f83e2df635beed363b0103afd10647c354953f382daef4b456de29ca288f9abee263257c27db42b034bd68854c85ec08e5f50f0e59a17b592cfdcb9f",
      "createdAt": "2025-10-02T01:49:14",
      "updatedAt": "2025-10-02T01:56:49"
    }
  ],
  200
]
```

### DELETE /api/users/{id}
Let's delete an unexisting user

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/users/incorrect_id' \
  -H 'accept: application/json'
```

```json
{
  "detail": "User not found"
}
```
\+ 404 status

### GET /api/posts
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/posts' \
  -H 'accept: application/json'
```

```json
[
  {
    "id": "06335982-05b2-4d84-9957-bd529c338a4c",
    "authorId": "75598b6b-3d53-418d-86bc-7de7c5869685",
    "title": "Interesting Header",
    "content": "Some content",
    "createdAt": "2025-10-02T02:03:44",
    "updatedAt": "2025-10-02T02:03:44"
  }
]
```
\+ 200 status

### GET /api/posts/{id}
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/posts/06335982-05b2-4d84-9957-bd529c338a4c' \
  -H 'accept: application/json'
```

```json
[
  {
    "id": "06335982-05b2-4d84-9957-bd529c338a4c",
    "authorId": "75598b6b-3d53-418d-86bc-7de7c5869685",
    "title": "Interesting Header",
    "content": "Some content",
    "createdAt": "2025-10-02T02:03:44",
    "updatedAt": "2025-10-02T02:03:44"
  }
]
```
---
Or sth incorrect

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/posts/not_id_at_all' \
  -H 'accept: application/json'
```

```json
{
  "detail": "Post not found"
}
```

### PUT /api/posts/?authorId={authorId}&title={title}&content={content}

```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/api/posts?authorId=75598b6b-3d53-418d-86bc-7de7c5869685&title=Interesting%20Header%202&content=Some%20content%202' \
  -H 'accept: application/json'
```

```json
[
  "OK",
  201
]
```

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/posts' \
  -H 'accept: application/json'
```

```json
[
  {
    "id": "06335982-05b2-4d84-9957-bd529c338a4c",
    "authorId": "75598b6b-3d53-418d-86bc-7de7c5869685",
    "title": "Interesting Header",
    "content": "Some content",
    "createdAt": "2025-10-02T02:03:44",
    "updatedAt": "2025-10-02T02:03:44"
  },
  {
    "id": "9c6095d9-2d8f-428d-bd34-df342997015d",
    "authorId": "75598b6b-3d53-418d-86bc-7de7c5869685",
    "title": "Interesting Header 2",
    "content": "Some content 2",
    "createdAt": "2025-10-02T02:08:25",
    "updatedAt": "2025-10-02T02:08:25"
  }
]
```

### PATCH /api/posts/{id}?title={title}&content={content}
```bash
curl -X 'PATCH' \
  'http://127.0.0.1:8000/api/posts/06335982-05b2-4d84-9957-bd529c338a4c?title=New%20Title&content=New%20Content' \
  -H 'accept: application/json'
```

```json
[
  {
    "message": "Post updated successfully"
  },
  200
]
```

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/posts/06335982-05b2-4d84-9957-bd529c338a4c' \
  -H 'accept: application/json'
```

```json
[
  {
    "id": "06335982-05b2-4d84-9957-bd529c338a4c",
    "authorId": "75598b6b-3d53-418d-86bc-7de7c5869685",
    "title": "New Title",
    "content": "New Content",
    "createdAt": "2025-10-02T02:03:44",
    "updatedAt": "2025-10-02T02:10:26"
  }
]
```

### DELETE /api/posts/{id} -- deletes one post


```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/posts/06335982-05b2-4d84-9957-bd529c338a4c' \
  -H 'accept: application/json'
```

```json
[
  "OK",
  200
]
```

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/posts/06335982-05b2-4d84-9957-bd529c338a4c' \
  -H 'accept: application/json'
```

```json
{
  "detail": "Post not found"
}
```
---

P.S. if you delete user you delete all of his posts because their's author's ID is not a hook at that moment.

----

All in all. I've spent a lot of time for this project. So I'll be very glad if you'll run it on your PC...