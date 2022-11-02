
# Setup Environment
## Requirement
* Python, pip installed
* Virtualenv installed via pip
* Postgresql
## Create Django environment
clone project
Create virtualenv and activate virtualenv by run following cmds line by line
```bash 
virtualenv env
.\env\scripts\activate (activate virtualenv)
```
You should see (env) at the head of cmd. 
All the following step require virtualenv is activated.
```bash
cd dlib-19.24.0
python setup.py install
```
Wait for dlib installed successfully.
Install opencv and face_recognition
```bash
pip install opencv-python
pip install face_recognition
```
now install all the requirement packages listed in requirements.txt.
Run following cmd in the root directory (same directory to requirements.txt).
```bash
pip install -r requirements.txt
```
If errors occur liên hệ Nam Anh.
now try to run django server. 
Migration alert will occur because we havent connect and migrate model to DB. 
```bash
python manage.py runserver
```
## Postgresql
* open pgAdmin4
* Create new database name security
* connect the db to django.
* You can google it and follow the instruction.

After connect the database to django server. Run django server again to check db server connected successfully.
Now migrate Django models to DB.
```bash
python manage.py makemigrations
python manage.py migrate
```
Open Querytool and run these cmds
```bash
create extension if not exists CUBE
```
```bash
ALTER TABLE accounts_myuser
  add vec_low CUBE
```
```bash
ALTER TABLE accounts_myuser
  add vec_high CUBE
```
```bash
create index accounts_myuser_vec_idx on accounts_myuser (vec_low, vec_high)
```
## Now our environment is ready.
### AUTHENTICATION

##### POST - get token (Must Provide account credentials - username, password)
```bash
http://127.0.0.1:8000/accounts/auth/token/
```
##### POST - refresh token
```bash
http://127.0.0.1:8000/accounts/auth/token/refresh/
```
-------------
### USERS MANAGEMENT
#### Ordinary user viewset
```bash
http://127.0.0.1:8000/accounts/ordinary/
```
##### Method
  - GET - list: Admin only.
  - POST - register user: no Permission.
=======
```bash
http://127.0.0.1:8000/accounts/ordinary/{id}/
```
##### Method
 - PUT - update: only Account owner or Admin.
 - GET - retrieve: only Account owner or Admin.
 - DELETE - detele: Only Account owner or Admin.
----------------
#### Admin user viewset
```bash
http://127.0.0.1:8000/accounts/admin/
```
#### Method
- GET - list: only admin.

```bash
http://127.0.0.1:8000/accounts/admin/{pk}
```
#### Method
- GET - retrieve admin detail: only Admin.

------------------
### SEARCH AND FILTER
* example
##### FILTER
search fields include  username, first_name, email, phone, address
Decendant ordered  by birth, username
```bash
http://127.0.0.1:8000/accounts/ordinary/?ordering=-birth,-username
```
* ordering_fields = ['username', 'first_name', 'email', 'phone', 
                       'address', 'visits__time', 'visits']
List accounts ordered by nearest visit
```bash
http://127.0.0.1:8000/accounts/ordinary/?ordering=-visits__time
or
http://127.0.0.1:8000/accounts/ordinary/?ordering=-visits__time

```
##### SEARCH
* Search through all accounts' attributes
* Search fields = ['username', 'first_name', 'email', 'phone', 'address']
* We can use both filter and search
```bash
http://127.0.0.1:8000/accounts/ordinary/?search=092393123
```
```bash
http://127.0.0.1:8000/accounts/ordinary/?ordering=-birth,-username&search=BuiNgocNam
```
```bash
http://127.0.0.1:8000/accounts/ordinary/?ordering=-birth&search=namanhble14012002@gmail.com
```




 
