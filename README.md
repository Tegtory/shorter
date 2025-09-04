# Link Shorter

link shorter - a little project that can help in a various situations and attempt to make something like clck.ru and etc

## ENV

| ENV NAME   | REQUIRED | DESC                                                          |
|-------------|----------|--------------------------------------------------------------|
| HOST        | +        | Host of site to gen links                                    |
| PORT        | +        | PORT of fastapi (def: 9123)  (required for compose)          |
| BOT_TOKEN   | -        | BOT_TOKEN FOR AIOGRAM IF NOT PROVIDED BOT DONT START         |
| BLACK_LIST  | -        | WIP                                                          |
| DB_HOST     | -        | host of database (def: db_shorter_app)                       |
| DB_PORT     | -        | port of database (def: 5432)                                 |
| DB_NAME     | -        | name of database (def: shorter)                              |
| DB_USER     | -        | name of user with access to database (def: user_shorter)     |
| DB_PASSWORD | -        | password of user with access to database (def: blank string) |

## Run

```bash
$ pip install uv
$ uv sync
$ python -m shorter
```

## TODO

- [ ] add tests
- [X] integrate ci/cd
- [x] add real database
- [ ] add migrations
- [ ] add inline_query to bot
- [ ] blacklist
- [X] DEBUG server

## Architeture

```text
link_shorter
│
├───common
│
├───domain
│   │   link.py
│   │
│   ├───interfaces
│   │
│   └───use_cases
│
├───infrastructure
│   │   di.py
│   │
│   └───repositories
│
├───presentors
│   ├───aiogram
│   └───fastapi
└───tests

```