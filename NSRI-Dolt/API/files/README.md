# Dolt Library — Django + Dolt demo

A Django web app backed by [Dolt](https://docs.dolthub.com/), a SQL database with
Git-like version control. Demonstrates a **shared field** (`author_name`) stored in
both the `Author` and `Book` tables, with drift detection/repair.

---

## Prerequisites

- Python 3.10+
- Dolt
- MySQL:
  - macOS: `brew install mysql-client pkg-config`
  - Ubuntu/Debian: `sudo apt install libmysqlclient-dev`

---

## Setup

### 1. Create the Dolt database

In one terminal window:
```bash
mkdir library_db && cd library_db
dolt init
dolt sql -q "CREATE DATABASE library;"
# Start the SQL server (keep this terminal open)
dolt sql-server --host 127.0.0.1 --port 3306 --user root
```

### 2. Install Python dependencies

In another terminal window, do this and all Python steps: 
```bash
cd /path/to/dolt_library
pip install -r requirements.txt
```

### 3. Run Django migrations


```bash
python manage.py make migrations library
```
(The above should theoretically be automatically done, but wasn't for me, so probably best to manually specify)

```bash
python manage.py migrate
```

### 4. Start the dev server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000

---


