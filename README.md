<div align="center">
  <h2>Simple B2B-Ecommerce with REST framework</h2>
</div>

* python 3.10
* PostgreSQL
---
* JWT
* Axes
* Throttling
* Swagger
* Django debug toolbar


---

<div align="center">
  <h3>Setup guide</h3>
</div>
#### Clone the repo
```
git clone git@github.com:rakibulislam8226/B2B-Ecommerce.git
```
**Go to the directory file**
```
cd B2B-Ecommerce/
```
---
**Create virtual environment based on your operating system**
 * **For ubuntu**
 ```shell
python3.10 -m venv venv
  ```

  ###### Activate the virtual environment
 ```shell
source venv/bin/activate
  ```
 * **For windows**
 ```shell
python -m venv venv
  ```

---
**Copy .example.env file to .env:**

  * For linux
    ```shell
    cp .example.env .env
    ```
  * For windows
    ```shell
    copy .example.env .env
    ```
##### Fill the .env with proper data
---
### Install the requirements file.
```
pip install -r requirements.txt
```
#### Go the the src directory
```
cd src/
```

  ###### Migrate the project
 ```shell
python manage.py migrate
  ```
  ###### If needed create superuser with proper data
  ```
  python manage.py createsuperuser
  ```
  ###### Run the server
 ```shell
python manage.py runserver
  ```
---
<div align="center">
  <h2>Project Structure</h2>
</div>
```
B2B-Ecommerce
.
.
├── account
│   ├── activation.py
│   ├── admin.py
│   ├── api.py
│   ├── apps.py
│   ├── choices.py
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── templates
│   │   ├── activation_email.html
│   │   ├── activation_error.html
│   │   └── activation_success.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── config
│   ├── asgi.py
│   ├── __init__.py
│   ├── models
│   │   └── TimeStampMixin.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── organizations
│   ├── admin.py
│   ├── apis.py
│   ├── apps.py
│   ├── choices.py
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── store
    ├── admin.py
    ├── apis.py
    ├── apps.py
    ├── custom_permissions.py
    ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── urls.py
    └── views.py

```
<div align="center">
  <h2>Thank you</h2>
</div>
