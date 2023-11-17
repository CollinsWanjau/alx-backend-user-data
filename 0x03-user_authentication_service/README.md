# 0x03. User authentication service

## Learning Objectives

- How to declare API routes in a Flask app
- How to get and set cookies
- How to retrieve request form data
- How to return various HTTP status codes

## Requirements

- All your functions should be type annotated
- The flask app should only interact with Auth and never with DB directly.
- Only public methods of Auth and DB should be used outside these classes

## Tasks

### [0. User model](./user.py)

- In this task you will create a SQLAlchemy model named User for a database table named users (by using the mapping declaration of SQLAlchemy).

- The model will have the following attrs:

    - id, represents a column of type integer that can't be null and is a primary key
    - email, represents a column of type string that can't be null and is unique
    - hashed_password, represents a column of type string that can't be null
    - session_id, represents a column of type string that can be null
    - reset_token, represents a column of type string that can be null
