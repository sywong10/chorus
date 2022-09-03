
**Capstone - Chorus project**


The Capstone - Chorus project is a final project of Full Stack Web Developer Nanodegree of Udacity.

* Chorus project is an application to help singers in nearby counties to come together, let choral directors know their interest and availability.
Singers can register themselves to a local registry with information of their voice part, their availability for rehersal days and phone number for communication.

* Choral directories can use this information to assemble their choral groups per available voice parts and availability.

<br><br>

**Motivation**
I like to use this course to practice python.


**Models**

singer table contains column name, phone, voice_part, not_available<br>
choir table contains columns name and practice_time<br>
enrollment table contains enrollment_id, choir_id and singer_id

<br><br>

**hosted application on Heroku**

https://sally-chorus.herokuapp.com/
<br><br><br>


**repo in github**

https://github.com/sywong10/chorus



**import a base collection to Postman if interested**
<br>
1. install postman
2. click on Collections
3. click on "Import"
4. click on "Upload Files", select choir.postman_collection.json
5. this will provide a group of basic REST activities for each role
6. {{host}} should be set to the application server if intend to run REST to the application.  If REST activities are intended to run on local flask, then default setting will suffice the neede and no additional change is needed. 
7. Bear token for director and singer can be found below.  Value of tokens should be set in postman.
   1. click on "director" folder in Collections, type should set to "Bearer Token", set the appropriate token value.
   2. click on "singer" folder in Collections, type should set to "Bearer Token", set the appropriate token value.


<br><br>
**Endpoints**

**GET** <br />
  &nbsp;&nbsp;&nbsp;/singers  <br />
  &nbsp;&nbsp;&nbsp;/singers/<int:singer_id> <br /> 
  &nbsp;&nbsp;&nbsp;/singers/<voice_part> <br /> 
  &nbsp;&nbsp;&nbsp;/choirs <br /> 
  &nbsp;&nbsp;&nbsp;/choir/<int:cid> <br /> 
  &nbsp;&nbsp;&nbsp;/choir/<int:cid>/<s_voice_part> <br />


**PATCH** <br />
  &nbsp;&nbsp;&nbsp;/singers/<int:id> <br /> 
  &nbsp;&nbsp;&nbsp;/choirs/<int:id> <br />

**POST** <br />
  &nbsp;&nbsp;&nbsp;/singers <br /> 
  &nbsp;&nbsp;&nbsp;/choirs <br /> 
  &nbsp;&nbsp;&nbsp;/enroll/<choir_name>/<int:sid> <br />

**DELETE** <br />
  &nbsp;&nbsp;&nbsp;/singers/<int:id> <br /> 
  &nbsp;&nbsp;&nbsp;/choirs/<int:id> <br />

<br><br>
**Roles** <br />

* **singer**: can register singer, unregister singer, update singer information, view list of people who have registered, list of people who are enrolled in each choir.<br>
* **director**: can do everything singer can.  Director can add new choir groups; director also can enroll and unenroll singers to a chorus according to choir needs in different voice parts and among singer availability.<br><br>


| role | permissions |
| --- | ---- |
| singer | delete:singer, get:choirs, get:enrollments, get:singers, patch:singers, post:singers |
| director | delete:choirs, delete:singers, get:choirs, get:enrollments, get:part, get:part_in_choir, get:singers, patch:choirs, patch:singers, post:choirs, post:enroll_singer, post:singers |



<br><br>

**Project dependencies**<br?
alembic==1.7.5<br>
click==7.1.2<br>
colorama==0.4.4<br>
ecdsa==0.17.0<br>
Flask==1.1.2<br>
Flask-Cors==3.0.10<br>
Flask-Migrate==1.8.0<br>
Flask-Script==2.0.6<br>
Flask-SQLAlchemy==2.5.1<br>
greenlet==1.1.2<br>
gunicorn==20.1.0<br>
importlib-metadata==4.8.2<br>
importlib-resources==5.4.0<br>
itsdangerous==1.1.0<br>
Jinja2==2.11.3<br>
Mako==1.1.6<br>
MarkupSafe==2.0.1<br>
psycopg2-binary==2.9.2<br>
pyasn1==0.4.8<br>
pycodestyle==2.8.0<br>
python-jose==3.3.0<br>
rsa==4.8<br>
six==1.16.0<br>
SQLAlchemy==1.3.24<br>
typing-extensions==4.0.1<br>
Werkzeug==1.0.1<br>
zipp==3.6.0<br>
python-dotenv<br><br><br>



**Setup local development environment**

**create empty databases**
1. su - postgres 
2. $ createdb capstone <br>
3. $ createdb capstone_test <br>


**setup Python environment**

1. su switch back to normal user
2. $ python3 -m venv cap
3. $ pip install -r requirements.txt <br>
4. $ source cap/bin/activate <br>
5. $ export FLASK_APP=app.py <br>
6. $ export FLASK_ENV=development <br>
7. $ flask run --reload (this will create empty tables in database)<br><br>

**if intend to populate database with sample data**<br> 
8. $ cd dbscripts <br>
     $ psql -U postgres capstone < choir.sql <br>
     $ psql -U postgres capstone_test < choir.sql <br>
        Password for user postgres: <br>
        INSERT 0 1 <br>
        INSERT 0 1 <br>
        INSERT 0 1 <br>

    $  psql -U postgres capstone < singer.sql <br>
    $  psql -U postgres capstone < enrollment.sql <br>

9. $ cd ..<br>
     $ flask db init <br>
     $ flask db migrate -m "initial migration" <br>

    

**if intend to recreate database**<br>
if databases need to be re-created...

1. comment out both foreign keys in class ChoirEnrollment, restart flask <br>

capstone=# delete from enrollment; <br>
DELETE 17 <br>
capstone=# select * from enrollment; <br>
 id | choir_id | singer_id <br>
----+----------+----------- <br>
(0 rows) <br>

capstone=# <br>

2. capstone=# delete from choir; <br><br>

3. capstone=# delete from singer; <br><br>

4. stop flask <br><br>

5. su switch user to postgres <br>
    $ dropdb capstone <br><br>

6. createdb capstone <br>
    createdb capstone_test <br><br>

7. uncomment both forieng keys in class ChoirEnrollment <br><br>

8. flask run --reload   (this should create empty tables) <br><br>

9. $ cd dbscripts <br>
   $ psql -U postgres capstone < choir.sql <br>
          Password for user postgres: <br>
          INSERT 0 1 <br>
          INSERT 0 1 <br>
          INSERT 0 1 <br>

      $  psql -U postgres capstone < singer.sql <br>
      $  psql -U postgres capstone < enrollment.sql <br><br>

10.  $ mv migrations migrations-orig
     $ flask db init <br>
     $ flask db migrate -m "initial migration" <br><br>

     

**curl examples for some endpoints, assuming flask is running on local machine**<br>
**API endpoints** <br><br>
http://localhost:5000 <br><br>


set token variables (tokens below are valid for 24 hours)<br><br>
$ singer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ5NVJqMVUwdUd0NFJvcjI1VGtpRiJ9.eyJpc3MiOiJodHRwczovL3N5d29uZzEwY2hvcnVzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MmRjNmQ3ZTM1Yzk5ZGM4YjhjNjczMDIiLCJhdWQiOiJjaG9ydXMiLCJpYXQiOjE2NjIyMTQwOTIsImV4cCI6MTY2MjMwMDQ5MiwiYXpwIjoidGFVZXFWNXk3RWdoN2c2S2Y5UDU3ajJ6VERwTHVjbVUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpzaW5nZXJzIiwiZ2V0OmNob2lycyIsImdldDplbnJvbGxtZW50cyIsImdldDpzaW5nZXJzIiwicGF0Y2g6c2luZ2VycyIsInBvc3Q6c2luZ2VycyJdfQ.N5TRjX7hhYIp18sLpynlRVVKnoxadMkN0Z2ebkSPaeDSy2P1iBtmC7sBgV8Mopwtj7UKlRt78HVfqEYas3-CrHi-C5bCRiEGfKhC6RlIhjlhLlX-eZ4CtcdVnnhtuGfUs73fKf2aIn_6RHJqbv1_8flc0krs7e_6HcjjIbNt8-DWj6FxSyoeWJSZNxMEml81NdKzKz5AGfmCgFj4JR6zk__h1TcHwmCm8ruAM92mU3AHhuKGfejcztMTNofC2Tw-SrSnIzt0-sJ5yxsxKLWjxRMlO4g-hpCQd--OzGcuar-we8wInq4fDMPNHxI-r2GnNqToOt25P4FssPfsvzS80g'<br><br>
$ director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ5NVJqMVUwdUd0NFJvcjI1VGtpRiJ9.eyJpc3MiOiJodHRwczovL3N5d29uZzEwY2hvcnVzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MmRjNmNiN2U1MThlYmI2Nzc1ZWIyMWYiLCJhdWQiOiJjaG9ydXMiLCJpYXQiOjE2NjIyMTM4MTEsImV4cCI6MTY2MjMwMDIxMSwiYXpwIjoidGFVZXFWNXk3RWdoN2c2S2Y5UDU3ajJ6VERwTHVjbVUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjaG9pcnMiLCJkZWxldGU6c2luZ2VycyIsImdldDpjaG9pcnMiLCJnZXQ6ZW5yb2xsbWVudHMiLCJnZXQ6cGFydCIsImdldDpwYXJ0X2luX2Nob2lyIiwiZ2V0OnNpbmdlcnMiLCJwYXRjaDpjaG9pcnMiLCJwYXRjaDpzaW5nZXJzIiwicG9zdDpjaG9pcnMiLCJwb3N0OmVucm9sbF9zaW5nZXIiLCJwb3N0OnNpbmdlcnMiXX0.TqWbfrnazsaXQEvLn8-n9kYZhMXWHqvLSxo4BMKY0UkhkVDXD5xIvYPKvvGgUvLihzhYpQb8Gpc0GzX3nOzurqibrTQy92eq5tQAzkV3rwrqkMEZiqR9gXj19GieixmflyyDYNwBK6vDTaB0Bmr_gqHYCg4OjvhVQzufFv4WhxRRs0WgajTwWKUDFK9UL6Bxoow-6WAoMBzIOyf4X2AiRAb21mw-WRamImP4SRyGvU_IJ--S95iao6euwHaoMAuCSZjcAkdtmgju30gYDJ7BCzW2WX6qKbIIu-p2ULeYCLiwGfDXsY4cERAtuJyM2efaZ2d7UNAj9xKjj8HcpjZgQg'<br><br>

list singer information for signers in first page <br><br>
$ curl http://localhost:5000/singers -H "Accept: application/json" -H "Authorization: Bearer $singer_token" <br>

list singer information for singers in paginated page 2 <br><br>
$ curl -X GET http://localhost:5000/singers\?page\=2 -H "Accept: application/json" -H "Authorization: Bearer $singer_token <br>

list singer information by singer_id = 2 <br><br>
$ curl -X GET http://localhost:5000/singers/2 -H "Accept: application/json" -H "Authorization: Bearer $singer_token" <br>

list singer name in specified voice part (alto) <br><br>
$ curl -X GET http://localhost:5000/singers/alto -H "Accept: application/json" -H "Authorization: Bearer $singer_token" <br><br>


**Error Code**

401 - authorization header, token issue <br>
403 - not authorized <br>
404 - resource not found <br>
409 - schedule conflict <br>
422 - unprocessable_entity <br>

==================


**GET /singers**
* fetch registered singer list 
* need 'get:singers' permission
* returns: json containing all info in singer table.

GET /singers
```json

{
    "singers": [
        {
            "id": 1,
            "name": "Jane Doe",
            "not_avilable": "Thursday",
            "phone": "111-111-1111",
            "voice_part": "alto"
        },
        {
            "id": 2,
            "name": "Leslie Knope",
            "not_avilable": "Tuesday",
            "phone": "131-111-1111",
            "voice_part": "soprano"
        }
      ]
}
```


**GET /singers/<voice_type>**
* fetch names of specified voice type among registered singers.
* needs 'get:singers'
* the endpoint returns 10 singers a page.
* query an incorrect voice type will return error 422

GET /singers/soprano

```json
{
    "soprano": [
        "Leslie Knope",
        "Ann Perkins",
        "Angela Martin"
    ],
    "success": true,
    "total": 3
}
```
when querying incorrect voice type:

GET /singers/baritone


```json
{
    "error": 422,
    "message": "unprocessable_entity",
    "success": false
}

```

***GET /singers/<int:singer_id>***
* query specific singer information
* need 'get:singers'
* endpoint returns singer information


```json
{
    "singer": {
        "id": 2,
        "name": "Leslie Knope",
        "not_avilable": "Tuesday",
        "phone": "131-111-1111",
        "voice_part": "soprano"
    },
    "success": true
}
```


***PATCH /singer/<int:singer_id>***

* update information of an existing singer
* the endpoint returns json object of the updated singer

example input json body

```json

{
    "voice_part": "bass"
}

```
return json

```json

{
    "singer": {
        "id": 10,
        "name": "Chris Traeger",
        "not_avilable": "Thursday",
        "phone": "132-253-7831",
        "voice_part": "bass"
    },
    "success": true
}

```

***POST /singer***
* this endpoint allows singers to register to signer table
* needs 'post:singers'

example body json
```json
{
    "name": "Michael Scott",
    "phone": "123-123-1234",
    "voice_part": "tenor",
    "not_available": "Thursday"
}
```

json return
```json
{
    "singer added": "Michael Scott added",
    "success": true
}
```

***DELETE /singers/<int:singer_id>***
* this endpoint delete specified singer from singer table
* requires 'delete:singers'
* this endpoint first checks if specified singer is enrolled in a choir.  If no, the endpoint will delete the singer.  If the singer is already enrolled to a choir, yes, the endpoint will unenroll, then delete.
* the endpoint returns return code and deleted singer name.

DELETE /singers/17

```json

{
    "deleted singer": {
        "id": 17,
        "name": "Michael Scott",
        "voice_part": "tenor"
    },
    "success": true
}
```

***GET /choirs***
* this endpoint queries available choirs in the area
* needs 'get:choirs' permission
* the return contains information of each choir in the area

```json

{
    "choirs": [
        {
            "id": 1,
            "name": "Hudson Choir",
            "practice time": "Tuesday 7 pm"
        },
        {
            "id": 2,
            "name": "Bergen Choir",
            "practice time": "Tuesday 7 pm"
        },
        {
            "id": 3,
            "name": "Mercer Choir",
            "practice time": "Thursday 7 pm"
        }
    ],
    "success": true
}
```

***POST /choirs***
* this endpoint add a new choir
* needs 'post:choirs' permission
* the endpoint returns json of added choir

POST /choirs

Body
```json
{
    "name": "Somerset Choir2",
    "practice_time": "Wednesday 7 pm"
}
```

json retun

```json
{
    "choir added": "Somerset Choir2",
    "success": true
}
```

***PATCH /choirs/<int:choir_id>***
* this endpoint update specified choir
* needs 'patch:choirs'
* the endpoint returns updated choir and information

PATCH /choirs/4

```json

{
    "success": true,
    "updated choir": {
        "id": 4,
        "name": "Somerset Choir2",
        "practice time": "Friday 7 pm"
    }
}

```

***DELETE /choirs/<int:choir_id>
* this endpoint deletes specified choir
* needs 'delete:choirs'
* it returns information of deleted choir

```json

{
    "removed choir": {
        "id": 4,
        "name": "Somerset Choir2",
        "practice time": "Friday 7 pm"
    },
    "success": true
}

```

***POST /enroll/<choir name>/<int:singer_id>***
* enroll specified singer to choir
* need 'post:enroll_singer'
* the endpoint checks which day the sinter is not available and enrolls the singer to specified choir when there is no schedule conflict. 
* the endpoint return json of singer name and the choir he or she is enrolled to.


POST /enroll/hudson/18

```json
{
    "singer added": "Michael Scott",
    "success": true,
    "updated choir": "Hudson Choir"
}
```

***GET /choir/<choir_id>/<voice_type>***
* this endpoint queries specified voice type in the choir
* need 'get:choirs'
* this endpoint returns json of list of name of the voice type in this choir.


GET /choir/1/tenor

```json
{
    "Choir name": "Hudson Choir",
    "success": true,
    "tenor": [
        "Mark Brendanawicz",
        "Ben Wyatt",
        "Craig Middleborooks",
        "Jim Halpert",
        "Michael Scott"
    ]
}
```




