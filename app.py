from flask import Flask, request
from flask_restful import Resource, Api
from models import Persons, Activities

app = Flask(__name__)
api = Api(app)


class Person(Resource):
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


class List_Activities(Resource):
    def get(self):
        activity = Activities.query.all()
        response = [{'id': i.id, 'activity': i.activity, 'person': i.person.name} for i in activity]
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
api.add_resource(List_Activities, '/activity/')


if __name__ == '__main__':
    app.run(debug=True)
