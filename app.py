from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from models import Persons, Activities, Users

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


@auth.verify_password
def verification(username, password):
    if not (username, password):
        return False
    return Users.query.filter_by(user=username, password=password)



class Person(Resource):
    @auth.login_required
    def get(self, name):
        person = Persons.query.filter_by(name=name).first()
        try:
            response = {
                'name': person.name,
                'age': person.age,
                'id': person.id
            }
        except AttributeError:
            message = 'Person Not Found'
            response = {'status': 'Error', 'message': message}
        except Exception:
            message = 'Unknown Error'
            response = {'status': 'Error', 'message': message}
        return response

    def put(self, name):
        person = Persons.query.filter_by(name=name).first()
        data = request.json
        if 'name' in data:
            person.name = data['name']
        if 'age' in data:
            person.age = data['age']
        person.save()
        response = {
            'name': person.name,
            'age': person.age,
            'id': person.id
        }
        return response

    def delete(self, name):
        person = Persons.query.filter_by(name=name).first()
        message = f'Person {person.name} Has Been Deleted'
        person.delete()
        return {'status': 'Success', 'message': message}


class List_Persons(Resource):
    @auth.login_required
    def get(self):
        persons = Persons.query.all()
        response = [{'id': i.id, 'name': i.name, 'age': i.age} for i in persons]
        return response

    def post(self):
        data = request.json
        person = Persons(name=data['name'], age=data['age'])
        person.save()
        response = {
            'id': person.id,
            'name': person.name,
            'age': person.age
        }
        return response


class Activity(Resource):
    def get(self, person):
        person_ = Persons.query.filter_by(name=person).first()
        if person_ == None:
            message = 'Person Not Found'
            response = {'status': 'Error', 'message': message}
            return response
        else:
            activity = Activities.query.filter_by(person=person_).all()
            response = [{'activity': [i.activity for i in activity]}]
            return response

class Activity_Status(Resource):
    def get(self, id):
        activity = Activities.query.filter_by(id=id).first()
        try:
            response = {
                'id': activity.id,
                'activity': activity.activity,
                'status': activity.status,
                'person': activity.person.name,
            }
        except AttributeError:
            message = f'Activity ID {id} Not Found'
            response = {'status': 'Error', 'message': message}
        except Exception:
            message = 'Unknown Error'
            response = {'status': 'Error', 'message': message}
        return response

    def put(self, id):
        activity = Activities.query.filter_by(id=id).first()
        try:
            data = request.json
            if 'status' in data:
                activity.status = data['status']
            activity.save()
            response = {
                'activity': activity.activity,
                'status': activity.status,
                'id': activity.id
            }
        except AttributeError:
            message = f'Activity ID {id} Not Found'
            response = {'status': 'Error', 'message': message}
        except Exception:
            message = 'Error Unknown'
            response = {'status': 'Error', 'message': message}
        return response



class List_Activities(Resource):
    @auth.login_required
    def get(self):
        activity = Activities.query.all()
        response = [{'id': i.id, 'activity': i.activity, 'person': i.person.name, 'status': i.status} for i in activity]
        return response

    def post(self):
        data = request.json
        person = Persons.query.filter_by(name=data['person']).first()
        activity = Activities(activity=data['activity'], person=person)
        activity.save()
        response = {
            'person': activity.person.name,
            'activity': activity.activity,
            'id': activity.id
        }
        return response


api.add_resource(Person, '/person/<string:name>/')
api.add_resource(List_Persons, '/person/')
api.add_resource(Activity, '/activity/<string:person>/')
api.add_resource(Activity_Status, '/activity/<int:id>/')
api.add_resource(List_Activities, '/activity/')


if __name__ == '__main__':
    app.run(debug=True)
