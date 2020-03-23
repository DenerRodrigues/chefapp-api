# chefapp-api
API Application that allows you to Create and List Food Recipes.

* [Python](https://www.python.org)
* [Django REST Framework](https://www.django-rest-framework.org)

Postman Documentation: https://documenter.getpostman.com/view/2649090/SzS8sQiE?version=latest

Quickstart
----------

#### Clone repository
```shell
git clone https://github.com/DenerRodrigues/chefapp-api
```

#### Install requirements.txt

```shell
pip install -r requirements.txt
```

#### Set environment variables in the `.env` file at project root

Variable     | Description     | Example
-------------|---------------- |--------------------------------------------------------
DEBUG        | Django Debug    | True
DATABASE_URL | Database URL    | sqlite:////home/dener/Workspace/chefapp/api/db.sqlite3


#### Run Migrations
```shell
python manage.py migrate
```

#### Create Admin Account
http://localhost:8000/admin/

```shell
python manage.py createadminaccount
```

#### Run Application
```shell
python manage.py runserver
```
