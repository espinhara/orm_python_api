from flask import Flask, request
from flask_restful import Api, Resource
from models import Person, Activities, Users
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)
#  Hard code authentication
# USERS = {
#   'espinhara':'123',
# }
#
#
# @auth.verify_password
# def verify(login, password):
#     if not (login, password):
#         return False
#     return USERS.get(login) == password


@auth.verify_password
def verify(login, password):
    if not (login, password):
        return False
    return Users.query.filter_by(login=login, password=password).first()


class People(Resource):
    @auth.login_required
    def get(self, name):
        try:
            person = Person.query.filter_by(name=name).first()
            response = {
                'name': person.name,
                'id': person.id,
                'age': person.age,
            }
        except AttributeError:
            response = {
                "status": "error",
                "message": "Cannot find person with name equals: {}".format(name)
            }
        return response

    def put(self, name):
        person = Person.query.filter_by(name=name).first()
        try:
            dates = request.json

            if 'name' in dates:
                person.name = dates['name']
            if 'age' in dates:
                person.age = dates['age']

            person.save()

            response = {
                'id': person.id,
                'name': person.name,
                'age': person.age
            }
        except IndexError:
            response = {
                "status": 'error',
                "message": 'Cannot find user name {} for update'.format(name)
            }
        except Exception:
            response = {
                "status": "error",
                "message": "An error occurred while trying to access the server"
            }
        return response

    def delete(self, name):
        try:
            person = Person.query.filter_by(name=name).first()
            person.delete()
            response = {
                "status": "ok",
                "message": "Deleted {}".format(name)
            }
        except AttributeError:
            response = {
                "status": "error",
                "message": "Cannot find user name {}".format(name)
            }
        # except Exception:
        #     response = {
        #         "status": "error",
        #         "message": "An error occurred while trying to access the server"
        #     }
        return response


class User(Resource):
    def post(self):
        dates = request.json
        user = Users(login=dates['login'], password=dates['password'])
        user.save()


class AllPeople(Resource):
    @auth.login_required
    def get(self):
        people = Person.query.all()
        return [{"id": i.id, "name": i.name, "age": i.age} for i in people]

    @auth.login_required
    def post(self):
        dates = request.json
        person = Person(name=dates['name'], age=dates['age'])
        person.save()

        response = {
            "id": person.id,
            "name": person.name,
            "age": person.age
        }

        return response


class AllActivities(Resource):
    def get(self):
        activities = Activities.query.all()
        return [
            {
                "id": i.id,
                "name": i.name,
                "person_id": i.person_id,
                "description": i.description,
                "person": i.person.name
            } for i in activities
        ]

    def post(self):
        dates = request.json
        person = Person.query.filter_by(name=dates['person']).first()
        activity = Activities(name=dates['name'], description=dates['description'], person=person)
        activity.save()
        response = {
            'person': activity.person.name,
            'name': activity.name,
            'description': activity.description
        }

        return response


api.add_resource(People, '/person/<string:name>')
api.add_resource(AllPeople, '/person/')
api.add_resource(AllActivities, "/activities/")


if __name__ == '__main__':
    app.run(debug=True)

# TODO: return activities for user name
# TODO: add a status field for the activity that are: done, pending
# TODO: alter status activity by activity id
# TODO: add exception handling for each method, return if the record does not exist a message.
