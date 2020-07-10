<div align="center">
  <br>
  <img alt="Crazy Bones" src="https://vignette.wikia.nocookie.net/crazybonespedia/images/1/1c/LogoIdea2.png/revision/latest/scale-to-width-down/310?cb=20190222195524" width="500px">
  <h1><a href="https://crazybone.herokuapp.com/">Crazy Bones</a></h1>
  <strong>xxxxx</strong>
</div>

## What is Crazy Bones

[Crazy Bones](https://en.wikipedia.org/wiki/Gogo%27s_Crazy_Bones) are small colorful characters that come in hundreds of colors and designs, each one with a unique name, design, personality and special ability. Gogo's were inspired by games from ancient Greece where children played by bouncing and throwing the carved knuckle bones of sheep, called astralgus - the game was called Astragals . The game has survived for over 3.000 years, and is known today as "jacks"; marbles are another variation. Each Gogo has a unique number for collecting and designed so you can hold and throw with one finger. Their 'Gogo's' name is a reference to 'Gogo Jacks' which is the English name for the ancient game of Tabas. And their name Bones is a reference to how the original game was played with real bones.

## Table of Contents

- [What is Crazy Bones](#what-is-crazy-bones)
- [Getting Started](#getting-started)
- [Tech Stack We Used](#tech-stack-we-used)
- [Development Documentation](#development-documentation)
- [Core Team](#core-team)

## Getting Started

Following these instructions will allow you to run and build the project on your local machine for development and testing purposes.

Create local PostgreSQL database:

```bash
CREATE DATABASE crazybones
```

Copy Django Secret Key from other Django or search Generate Django Secret Key on Google to `settings.py`

Move to project folder and run following command to make to your models into your database schema:

```bash
python manage.py migrate
```

Install Stripe:

```bash
pip install stripe
```

Go to main_app/urls/urls.py and uncomment seed path

```base
#path('seed/', views.seed, name='seed'),
```

In your browser navigate to [http://127.0.0.1:8000/seed](http:127.0.0.1:800/seed) to seed all the crazybones into database

Now you are good to go! Navigate to [http://127.0.0.1:8000/](http:127.0.0.1:800/), sign up and start playing

<h3>Congrats!</h3>

## Tech Stack We Used

- Local
  - [Python](https://www.python.org/downloads/) 3.8
  - [Django](https://www.djangoproject.com/download/) 3.0.8
  - [PostgreSQL](https://www.postgresql.org/download/) 12
- Live
  - [Heroku](https://www.heroku.com)
  - [Heroku Postgres](https://www.heroku.com/postgres)

## Development Documentation

- [Trello board](https://trello.com/b/UHIbge4o/crazbone-trader)
- ERD![ERD image](/main_app/static/img/ERD.png)
- Wireframe![Wirefram image](/main_app/static/img/wireframe.png)

## Core Team

- [@Albatrooss](https://github.com/Albatrooss)
- [@ibrahimalhanich](https://github.com/ibrahimalhanich)
- [@jpeng11](https://github.com/jpeng11)
- [@banhpete](https://github.com/banhpete)

<p align="center">
  <img alt="CrazyBone" width="200px" src="https://vignette.wikia.nocookie.net/crazybonespedia/images/f/ff/Mascot101.png/revision/latest/scale-to-width-down/310?cb=20190222171713">
  <br>
  <strong>Happy Coding</strong> ❤️
</p>
