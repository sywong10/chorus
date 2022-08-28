
**Capstone - Chorus project**


The Capstone - Chorus project is a final project of Full Stack Web Developer Nanodegree of Udacity.

* Chorus project is an application to help singers in nearby counties to let choral directors know their availability.
Singers can register themselves to a local registry with information of their voice part, their availability for rehersal days and phone number for communication.

* Choral directories can use this information to assemble their choral groups per singers' voice parts and rehearsal availability.


**Models**

singer table with colums name, phone, voice_part, not_available
choir table with columns name and practice_time

enrollment table with enrollment_id, choir_id and singer_id


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


**Roles** <br />

* singer: can register singer, unregister singer, update singer information, view list of people who have registered, list of people enrolled in each choir.
* director: can do everything singer can.  Director also can enroll and unenroll a singer to a chorus according to their voice part and availability.


**setup Python environment**

$ cd capstone <br>
$ pip install -r requirements.txt <br>
$ source cap/bin/activate <br>
$ cd starter <br>
$ export FLASK_APP=app.py <br>
$ export FLASK_ENV=development <br>
$ flask run --reload <br>


**Prep for database**


1.  createdb capstone <br>
    createdb capstone_test <br>

2.  flask run --reload   (this should create empty tables) <br>

3.   $ cd starter/dbscripts <br>
     $ psql -U postgres capstone < choir.sql <br>
     $ psql -U postgres capstone_test < choir.sql <br>
        Password for user postgres: <br>
        INSERT 0 1 <br>
        INSERT 0 1 <br>
        INSERT 0 1 <br>

    $  psql -U postgres capstone < singer.sql <br>
    $  psql -U postgres capstone < enrollment.sql <br>

4.  $ cd starter <br>
     $ mv migrations migration-orig <br>
     $ flask db init <br>
     $ flask db migrate -m "initial migration" <br>

    

**recreate database**

1.
capstone=# delete from enrollment; <br>
DELETE 17 <br>
capstone=# select * from enrollment; <br>
 id | choir_id | singer_id <br>
----+----------+----------- <br>
(0 rows) <br>

capstone=# <br>

2.  capstone=# delete from choir; <br>

3.  capstone=# delete from singer; <br>

4.  stop flask <br>

5.  switch user to postgres <br>
    $ dropdb capstone <br>

6.  createdb capstone <br>
    createdb capstone_test <br>

7.  uncomment both forieng keys in class ChoirEnrollment <br>

8.  flask run --reload   (this should create empty tables) <br>

9.   $ cd starter/dbscripts <br>
     $ psql -U postgres capstone < choir.sql <br>
        Password for user postgres: <br>
        INSERT 0 1 <br>
        INSERT 0 1 <br>
        INSERT 0 1 <br>

    $  psql -U postgres capstone < singer.sql <br>
    $  psql -U postgres capstone < enrollment.sql <br>

10.  $ cd starter <br>
     $ mv migrations migration-orig <br>
     $ flask db init <br>
     $ flask db migrate -m "initial migration" <br>

     

**curl example to some endpoints**


list singer information for signers in first page <br>
$ curl http://localhost:5000/singers -H "Accept: application/json" -H "Authorization: Bearer $singer_token" <br>

list singer information for singers in paginated page 2 <br>
$ curl -X GET http://localhost:5000/singers\?page\=2 -H "Accept: application/json" -H "Authorization: Bearer $singer_token <br>

list singer information by singer_id = 2 <br>
$ curl -X GET http://localhost:5000/singers/2 -H "Accept: application/json" -H "Authorization: Bearer $singer_token" <br>

list singer name in specified voice part (alto) <br>
$ curl -X GET http://localhost:5000/singers/alto -H "Accept: application/json" -H "Authorization: Bearer $singer_token" <br>


**Error Code**

401 - authorization header, token issue <br>
403 - not authorized <br>
404 - resource not found <br>
409 - schedule conflict <br>
422 - unprocessable_entity <br>

==================

**API endpoints** <br>
http://localhost:5000 <br>




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




Domain:         sywong10chorus.us.auth0.com
API Audience:   chorus
Client ID:      taUeqV5y7Egh7g6Kf9P57j2zTDpLucmU
Allowed Callback URLs:  https://localhost:8080/login-result


directory
sywong109@gmail.com


https://sywong10chorus.us.auth0.com/authorize?audience=chorus&response_type=token&client_id=taUeqV5y7Egh7g6Kf9P57j2zTDpLucmU&redirect_uri=https://localhost:8080/login-result
https://localhost:8080/login-result#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ5NVJqMVUwdUd0NFJvcjI1VGtpRiJ9.eyJpc3MiOiJodHRwczovL3N5d29uZzEwY2hvcnVzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MmRjNmNiN2U1MThlYmI2Nzc1ZWIyMWYiLCJhdWQiOiJjaG9ydXMiLCJpYXQiOjE2NjE3MTQxNzEsImV4cCI6MTY2MTgwMDU3MSwiYXpwIjoidGFVZXFWNXk3RWdoN2c2S2Y5UDU3ajJ6VERwTHVjbVUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjaG9pcnMiLCJkZWxldGU6c2luZ2VycyIsImdldDpjaG9pcnMiLCJnZXQ6ZW5yb2xsbWVudHMiLCJnZXQ6cGFydCIsImdldDpwYXJ0X2luX2Nob2lyIiwiZ2V0OnNpbmdlcnMiLCJwYXRjaDpjaG9pcnMiLCJwYXRjaDpzaW5nZXJzIiwicG9zdDpjaG9pcnMiLCJwb3N0OmVucm9sbF9zaW5nZXIiLCJwb3N0OnNpbmdlcnMiXX0.meqUIIFV3GQidppqjcIHrTauVS89AUsPrbG661nQTBWWXVveBOnWA_WyGqetlotOylAGhHWEsIj9PMGVJZqDzD_cbcyMNAOBizRJB_5_wJYpunlXI2JlMTi1rr1yT3BVXT_dIEsMd3Po_utcK6eJLgZR2sKpEjU5IpxZD8D8noYbYJ17oMA5o5CrDCTsvUFGzka9Yuj7E167oq3C52vWy01a1K9o9TKiy1G0Q56lsvD4QnCkWs6g1FKQoWVucMVeqiF_EMzj00TMqPT2iXo4hu5nJeHNwKhE8fScQg3A64mSdRu5X7WgdB8DEBn_oFKHrmB5q83h1Pw5fcd96_M7Wg&expires_in=86400&token_type=Bearer


singer
sywong10@yahoo.comeyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ5NVJqMVUwdUd0NFJvcjI1VGtpRiJ9.eyJpc3MiOiJodHRwczovL3N5d29uZzEwY2hvcnVzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MmRjNmNiN2U1MThlYmI2Nzc1ZWIyMWYiLCJhdWQiOiJjaG9ydXMiLCJpYXQiOjE2NjE3MTQxNzEsImV4cCI6MTY2MTgwMDU3MSwiYXpwIjoidGFVZXFWNXk3RWdoN2c2S2Y5UDU3ajJ6VERwTHVjbVUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjaG9pcnMiLCJkZWxldGU6c2luZ2VycyIsImdldDpjaG9pcnMiLCJnZXQ6ZW5yb2xsbWVudHMiLCJnZXQ6cGFydCIsImdldDpwYXJ0X2luX2Nob2lyIiwiZ2V0OnNpbmdlcnMiLCJwYXRjaDpjaG9pcnMiLCJwYXRjaDpzaW5nZXJzIiwicG9zdDpjaG9pcnMiLCJwb3N0OmVucm9sbF9zaW5nZXIiLCJwb3N0OnNpbmdlcnMiXX0.meqUIIFV3GQidppqjcIHrTauVS89AUsPrbG661nQTBWWXVveBOnWA_WyGqetlotOylAGhHWEsIj9PMGVJZqDzD_cbcyMNAOBizRJB_5_wJYpunlXI2JlMTi1rr1yT3BVXT_dIEsMd3Po_utcK6eJLgZR2sKpEjU5IpxZD8D8noYbYJ17oMA5o5CrDCTsvUFGzka9Yuj7E167oq3C52vWy01a1K9o9TKiy1G0Q56lsvD4QnCkWs6g1FKQoWVucMVeqiF_EMzj00TMqPT2iXo4hu5nJeHNwKhE8fScQg3A64mSdRu5X7WgdB8DEBn_oFKHrmB5q83h1Pw5fcd96_M7Wg

https://localhost:8080/login-result#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjQ5NVJqMVUwdUd0NFJvcjI1VGtpRiJ9.eyJpc3MiOiJodHRwczovL3N5d29uZzEwY2hvcnVzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MmRjNmQ3ZTM1Yzk5ZGM4YjhjNjczMDIiLCJhdWQiOiJjaG9ydXMiLCJpYXQiOjE2NjExODg1MTAsImV4cCI6MTY2MTI3NDkxMCwiYXpwIjoidGFVZXFWNXk3RWdoN2c2S2Y5UDU3ajJ6VERwTHVjbVUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpzaW5nZXJzIiwiZ2V0OmNob2lycyIsImdldDplbnJvbGxtZW50cyIsImdldDpzaW5nZXJzIiwicGF0Y2g6c2luZ2VycyIsInBvc3Q6c2luZ2VycyJdfQ.Z4t_RA0u_R9nMzhf6SqG__MgPceIZrY9tnN6asVshdpQLc9cOTAJFT9dirO_t9dschDlRP6Y51gIUqsD1ux7gma1tuBZzLHwVCL96t8k1rImUmbuIo3VbayHKCW0oD9Cr1Ek82Ess88Up3FGQLtEq6Hd3EA-dtfErslI_tTN2yKN_QFqYyQOykBkzz1BXl_kVMobuxuuGUWlvpxA65LO8ug9DSRX86ojE_Peg1qRWLhpUKK20hNgvn9L9XqJ5v8vILhqzjQxSZBpejIM-w4tGEnx3GqpCDBGWfC7-bM_ROnllzUMOYV0ookapTC6bYA9-yTmvdgPgQeYYIS2pdN0mw&expires_in=86400&token_type=Bearer

