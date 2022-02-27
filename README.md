# User Feedback RESTful API

How to:
1. Install python 3 and Pip.
2. Run “pip install django” on CMD to install Django.
3. Run “pip install djangorestframework” on CMD to install Django Rest Framework.
4. Run “pip install drf_yasg” on CMD to install Yet another Swagger generator.
5. In project folder run “python manage.py runserver” in CMD to start the server.
6. Enter the provided url in your browser of choice. http://127.0.0.1:8000/. The web interface can be used here.
7. I’ve included a premade admin account “admin” with password “admin”.
8. http://127.0.0.1:8000/api/ has all the endpoints listed as drf_yasg generated Swagger documentation. The POST endpoints require the parameters in json format.

- /delete_user/ -
Requires “id” of the user you want to delete. Requires you to be logged in as an admin.
- /feedbacks/ -
Returns all feedbacks.
- /feedbacks/{id} -
Returns a feedback.
- /login/ -
Log in as user. Requires “username” and “password”.
- /logout/ -
Log out from user.
- /new_feedback/ -
Requires “body” and “owner” (owner as id). Requires you to be logged in.
- /signup/ -
Requires “username”, “password1” and “password2”. Creates new user.
- /users/ -
Returns all users and their ids.
- /users/{id}/ -
Returns a user.
- /users/{id}/feedbacks/ -
Returns all feedbacks of a user.

Example:

http://127.0.0.1:8000/signup/
POST {“username”: “TestUser”, “password1”: “password”, “password2”: “password"}
Creates user “TestUser” with password “password” and automatically logs in.

http://127.0.0.1:8000/users/
GET
Returns a json list of all users and their IDs.

http://127.0.0.1:8000/new_feedback/
POST {“body”: “Test feedback”, “owner”: 3}
Creates new feedback “Test feedback” for user with ID 3. Requires you to be logged in. Feedback author is automatically set as the logged in user.