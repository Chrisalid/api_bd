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

api.add_resource(Person, '/person/<string:name>/')

if __name__ == '__main__':
    app.run(debug=True)
