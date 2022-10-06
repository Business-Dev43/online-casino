# Online Casino Game

The online casino game.

# Setup Project Locally
  
  Need to follow these steps:
  
  - Clone the project.

```bash
git clone https://github.com/Business-Dev43/online-casino.git
```

- Change the directory.

```bash
cd online-casino
```

- Install `pipenv` library.

```bash
pip install pipenv
```

- Create virtual environment.

```bash
pipenv shell
```

- Install the dependencies.

```bash
pipenv install
```

# Run Project Locally

  Need to follow these steps:

- Go inside project.

```bash
cd casino
```

- Setup database.

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

- Run server.

```bash
python manage.py runserver
```

- Hit this URL on browser.

```bash
http://127.0.0.1:8000
```