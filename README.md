## Secure web chat based on WebSocket and powered by aiohttp

Powered by AIOHTTP framework for Python 3.5.3+

## Features

* Public Chat mode with rooms
* Private Chat mode with message encryption and signature verification
* Based on WebSocket

## Installation

### Virtual Env

My version of Python is 3.8.0

Install all requirements to your virtualenv

```    
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

### Database

First you need to create a PostgreSQL database. Example:

```
$ psql -U postgres -h localhost
> CREATE DATABASE chat_bd;
> CREATE USER chat_admin WITH PASSWORD '0000';
> GRANT ALL PRIVILEGES ON DATABASE chat_bd TO chat_adbin;
 ```
 
Enter database information into the config.py file.

To initialize database (create tables) run init_db.py
```
$ python3 init_db.py
 ```

## Run
To run this code just type to console

```
$ python3 main.py
 ```
    
Open browser

    http://0.0.0.0:80

## Built with

* [aiohttp](https://github.com/aio-libs/aiohttp) – Asynchronous HTTP client/server framework for asyncio and Python
* [cryptico](https://github.com/wwwtyro/cryptico) – An easy-to-use encryption system utilizing RSA and AES for javascript
* [aiopg](https://github.com/aio-libs/aiopg) – A library for accessing a PostgreSQL database from the asyncio