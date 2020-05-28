# Hackstack API Documentation

This api is created for event Hackstack1.0 organized by hackerearth.<br>
Team-VIVA_WARRIORS
<br><br>
The purpose of the API is to create and handle events.There will be a super admin that will have the right to add other admins to host their events on the website.Admin login functionality is provide so that the admin can add or delete the events he created.Detailed registrations will be available for the event the admin has hosted.
<br>
The API is currently integrated with the following website:
`https://event-handler.netlify.app/`
<br>
# Installation and How to Run
Tech Stack:
- Python3

Installation:
- Python3: https://www.python.org/downloads/

How to run:
- Install requirements.txt
    - `pip install -r requirements.txt`
- Run the following command through terminal (from Project root): 
    - `python3 app.py`
- If everything is setup correctly, the app will run on http://127.0.0.1:5000/
   

# Authentication



## `/admin/login`
This endpoint can be used to login an admin with their username and password.

Request Type: `POST` <br> 
Request Body: `application/json` <br>
Parameters:<br>
`username`: username of the admin <br>
`password`: password of the account

Sample request:
```
POST: http://127.0.0.1:5000/admin/login
{
    'username':'username',
    'password':'passowrd'
}
```
Sample response:
```
{
    'username':'your_username',
    'access_token':'some_access_token',
    'refresh_token':'some_refresh_token',
    'expires_in':'some_time',
    'registered_user':True/False
}
```
<br>
## `/admin/logout`
This endpoint can be used to logout.
Request Header: `key:Authentication`, `value:Bearer {{access_token}}` <br> 
Request Type: `GET` <br> 
Parameters:<br>
`None`

Sample request:
```
GET: http://127.0.0.1:5000/admin/logout
```
Sample response:
```
{
    "message": "Logout Successful",
    "code": "S6",
    "time": "some_time",
    "status": "Success"
}
```
<br>
## `/admin/changepwd`
This endpoint can be used to change an admin's password.

Request Type: `POST` <br> 
Request Header: `key:Authentication`, `value:Bearer {{access_token}}` <br> 
Request Body: `application/json` <br>
Parameters:<br>
`username`: username of the admin <br>
`old_password`: password of the account<br>
`new_password`: new password for the account

Sample request:
```
POST: http://127.0.0.1:5000/admin/login
{
    'username':'username',
    'old_password':'password',
    'new_password':'new password'
}
```
Sample response:
```
{
    'message':'Password Successfuly changed',
    'code':'S2',
    'time':'some_time'
    'status':'Success'
}
```
<br>
## `/admin/register`
This endpoint can be used to register a new admin.
`CAN ONLY BE USED BY THE SUPERADMIN`

Request Type: `POST` <br> 
Request Header: `key:Authentication`, `value:Bearer {{access_token}}` <br> 
Request Body: `application/json` <br>
Parameters:<br>
`username`: username of the admin <br>
`password`: password for the account<br>

Sample request:
```
POST: http://127.0.0.1:5000/admin/login
{
    'username':'username',
    'password':'password'
}
```
Sample response:
```
{
    'message':'New admin successfully created',
    'code':'S1',
    'time':'some_time'
    'status':'Success'
}
```
<br>
## `/admin/id`
This endpoint can be used to get uuid and name of an admin.

Request Type: `GET` <br> 
Request Header: `key:Authentication`, `value:Bearer {{access_token}}` <br> 
Parameters:<br>
`None`

Sample request:
```
GET: http://127.0.0.1:5000/admin/id
```
Sample response:
```
{
    "id": {
        "uuid": "a3c5793b-bedfc5a2c90",
        "username": "some_name"
    }
}
```
<br>
## `/admin/all`
This endpoint can be used to get a list of all admins.
`CAN ONLY BE USED BY THE SUPERADMIN`

Request Type: `POST` <br> 
Request Header: `key:Authentication`, `value:Bearer {{access_token}}` <br> 
Parameters:<br>
`None`

Sample request:
```
GET: http://127.0.0.1:5000/admin/all
```
Sample response:
```
[
    {
        "username": "ADMIN!",
        "uuid": "833672c6-bc14d81c941a"
    },
    {
        "username": "ADMIN2",
        "uuid": "dc8e5c99-ac8c"
    }
]
```
<br>
<br>
# Events

## `/event`
This endpoint can be used to create a new event

Request Type: `POST` <br> 
Request Header: `key:Authentication`, `value:Bearer {{access_token}}` <br> 
Request Body: `application/json` <br>
Parameters:<br>
`event_name`: name of the event <br>

Sample request:
```
POST: http://127.0.0.1:5000/admin/login
{
    'event_name':'some_event'\
}
```
Sample response:
```
{
    'message':'New event added successfully',
    'code':'S4',
    'time':'some_time'
    'status':'Success'
}
```
<br>
## `/event`
This endpoint can be used to get a list of all events for the logged-in admin.

Request Type: `GET` <br> 
Request Header: `key:Authentication`, `value:Bearer {{access_token}}` <br> 
Request Body: `application/json` <br>
Parameters:<br>
`None`
Sample request:
```
GET: http://127.0.0.1:5000/event
```
Sample response:
```
[
    {
        "event_name": "Sample",
        "username": "name_of_the_admin_who_hosted_the_event"
    },
    {
        "event_name": "Sample2",
        "username": "name_of_the_admin_who_hosted_the_event"
    },
    
]
```
<br>
## `/event`
This endpoint can be used to delete an event.

Request Type: `DELETE` <br> 
Request Header: `key:Authentication`, `value:Bearer {{access_token}}` <br> 
Request Body: `application/json` <br>
Parameters:<br>
`event_name`: name of the event <br>

Sample request:
```
POST: http://127.0.0.1:5000/event
{
    'event_name':'some_event'
}
```
Sample response:
```
{
    'message':'Event deleted successfully',
    'code':'S5',
    'time':'some_time'
    'status':'Success'
}
```
<br>
<br>
# Contact Us

## `/contact`
This endpoint can be used to save a message to database from a user.

Request Type: `POST` <br> 
Request Body: `application/json` <br>
Parameters:<br>
`name`: name of the user <br>
`email`: email of the user<br>
`message`:the message to be sent<br>

Sample request:
```
POST: http://127.0.0.1:5000/contact
{
    'name': 'person_name',
    'email': 'name@example.com',
    'message':'wanted to now about something'
}
```
Sample response:
```
{
    'message':'Your message is sent, we'll get in touch soon',
    'code':'S7',
    'time':'some_time'
    'status':'Success'
}
```
<br>
<br>
# Event Registrations

## `/registration`
This endpoint can be used to make a person register for an event.

Request Type: `POST` <br> 
Request Body: `form_data` <br>
Parameters:<br>
`name`: name/ <br>
`email`: email <br>
`type`: self/corporate/group/others <br>
`mobile_number`: mobile number <br>
`no_of_tickets`: number of tickets wanted for the event <br>
`image`: upload image of an id. <br>
`event_name`: name of event to register in <br>

Sample request:
```
POST: http://127.0.0.1:5000/registration
all parameters
```
Sample response:
```
{
    'registration_number':'some_number'
}
```
<br>
## `registration`
This endpoint can be used to fetch a list of all registrations hosted by the logged in admin.

Request Type: `GET` <br> 
Request Header: `key:Authentication`, `value:Bearer {{access_token}}` <br> 
Request Body: `application/json` <br>
Parameters:<br>
`None`

Sample request:
```
GET: http://127.0.0.1:5000/registration
```
Sample response:
```
[
    {
        "name": "aa",
        "registration_id": "1",
        "image": "link_to_image",
        "mobile": "12345",
        "email": "aa@gmail.com",
        "no_of_tickets": 6,
        "registration_type": "others",
        "event": "event 3"
    },
    {
        "name": "bb",
        "registration_id": "2",
        "image": "link_to_image",
        "mobile": "12345",
        "email": "bb@gmail.com",
        "no_of_tickets": 8,
        "registration_type": "others",
        "event": "event 5"
    }
]
```
<br>
## `registration/<string:registration_number>`
This endpoint can be used to get the details of registration using the registration number.

Request Type: `GET` <br> 
Request Header: `key:Authentication`, `value:Bearer {{access_token}}` <br> 
Parameters:<br>
`None`

Sample request:
```
GET: http://127.0.0.1:5000/registration/2
```
Sample response:
```
{
        "name": "bb",
        "registration_number": "2",
        "image": "link_to_image",
        "mobile": "12345",
        "email": "bb@gmail.com",
        "no_of_tickets": 8,
        "registration_type": "others",
        "event": "event 5"
}
```

<br><br>
# Errors and Exceptions
Below are the error code and their corresponding messages that will be returned in case of invalid API request.


| Name | Code | Message  |
| ---- | ---- | ---- |
| INSUFFICIENT_PRIVELEGES_ERROR | E1| You dont have the adequate priveleges for this operation|
| REGISTER_ADMIN_ERROR | E2| Administrator not registered|
| INVALID_CREDENTIALS_ERROR | E3| The entered credentials are invalid.|
| ADMIN_EXISTS_ERROR | E4| The Admin name entered already exists.|
| NO_ADMIN_ERROR | E5| No Admins exists.|
| REGISTRATION_ERROR | E6| An error occured while registering.|
| UNKNOWN_ERROR | E7| Unknown error occured.|
| CHANGE_PASSWORD_ERROR | E8|Unable to change password.|
| INCORRECT_OLD_PASSWORD_ERROR | E9| The old password you entered is incorrect.|
| NO_REGISTRATIONS_ERROR | E10| No registrations found.|
| REGISTRATION_EXISTS_ERROR | E11| Registration with same email already exists.|
| NO_EVENT_ERROR | E12| No events found|
| EVENT_ADD_ERROR | E13| Unable to add event|
| EVENT_DELETE_ERROR | E14| Unable to delete event|
| ONGOING_EVENT_ERROR | E15| Ongoing Event|
| EXPIRED_TOKEN_ERROR | E16| The token has expired.|
| INVALID_TOKEN_ERROR | E17| The token is invalid.|
| MISSING_TOKEN_ERROR | E18| The token missing in the header|
| REVOKED_TOKEN_ERROR | E19| The token is revoked|
| MESSAGE_SEND_ERROR | E20| Unable to send message,try again later.|
