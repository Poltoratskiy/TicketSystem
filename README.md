### TaskHandlerService

Tech stack: Flask, Postgres, SQLAlchemy

First, clone the repository to your local machine:

```bash
git clone https://github.com/Poltoratskiy/TicketSystem.git
```

Change database connection configs in ***app.configs.py***

Install modules:
```bash
make install
```

Run project
```bash
make run
```
The project will be available at **127.0.0.1:5000/**

## Routes
* POST http://localhost:5000/tickets - create new ticket

Example, request body:
```json
{
    "text": "text of the ticket",
    "theme": "theme of the ticket",
    "email": "email@mail.org"
}
```


* GET http://localhost:5000/tickets/<int:id> - get info about ticket by id

* PATCH http://localhost:5000/tickets - update status of ticket
Example, request body:
```json
{
    "id": 3,
    "registered_on": "2019-08-01 22:06:22.634782",
    "changed_on": "2019-08-01 22:06:22.634791",
    "text": "text of the ticket",
    "theme": "theme of the ticket",
    "email": "email@mail.org",
    "status": {
        "id": 3,
        "name": "закрыт"
    }
}
```

* POST http://localhost:5000/comments - add comment to the ticket
Example, request body:
```json
{
    "id": 1,
    "text": "text of comment",
    "email": "email@mail.org",
    "ticket_id":3
}
```
