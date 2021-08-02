from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from models import Persons, Activities, Users

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Python Flask With DB',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'
})
docs = FlaskApiSpec(app)


class Flask_DB_ResponseSchema(Schema):
    message = fields.Str(default='Success')


class Flask_DB_RequestSchema(Schema):
    api_type = fields.String(required=True, description='API Flask With DB')


@auth.verify_password
def verification(username, password):
    if not (username, password):
        return False
    return Users.query.filter_by(user=username, password=password).first()


class Person(MethodResource, Resource):
    # @auth.login_required
    @doc(description='Get Persons With Name.', tags=['Person'])
    @marshal_with(Flask_DB_ResponseSchema)
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

    @doc(description='Get Persons With Name', tags=['Person'])
    @use_kwargs(Flask_DB_RequestSchema, location=('json'))
    @marshal_with(Flask_DB_ResponseSchema)
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

    @doc(description='Delete Person With Name', tags=['Person'])
    @marshal_with(Flask_DB_ResponseSchema)
    def delete(self, name):
        person = Persons.query.filter_by(name=name).first()
        message = f'Person {person.name} Has Been Deleted'
        person.delete()
        return {'status': 'Success', 'message': message}


class List_Persons(MethodResource, Resource):
    # @auth.login_required
    @doc(description='Get All Persons.', tags=['All Persons'])
    @marshal_with(Flask_DB_ResponseSchema)
    def get(self):
        persons = Persons.query.all()
        response = [{'id': i.id, 'name': i.name, 'age': i.age} for i in persons]  # noqa: E501
        return response

    @doc(description='Get All Persons', tags=['All Persons'])
    @use_kwargs(Flask_DB_RequestSchema, location=('json'))
    @marshal_with(Flask_DB_ResponseSchema)
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


class Activity(MethodResource, Resource):
    @doc(description='Get Activity With Name.', tags=['Activity'])
    @marshal_with(Flask_DB_ResponseSchema)
    def get(self, person):
        person_ = Persons.query.filter_by(name=person).first()
        if person_ == None:  # noqa: E711
            message = 'Person Not Found'
            response = {'status': 'Error', 'message': message}
            return response
        else:
            activity = Activities.query.filter_by(person=person_).all()
            response = [{'activity': [i.activity for i in activity]}]
            return response


class Activity_Status(MethodResource, Resource):
    @doc(description='Get Activity Status.', tags=['Id'])
    @marshal_with(Flask_DB_ResponseSchema)
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

    @doc(description='Get Activity With Name', tags=['Id'])
    @use_kwargs(Flask_DB_RequestSchema, location=('json'))
    @marshal_with(Flask_DB_ResponseSchema)
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


class List_Activities(MethodResource, Resource):
    # @auth.login_required
    @doc(description='Get All Activities.', tags=['All Activities'])
    @marshal_with(Flask_DB_ResponseSchema)
    def get(self):
        activity = Activities.query.all()
        response = [{'id': i.id, 'activity': i.activity, 'person': i.person.name, 'status': i.status} for i in activity]   # noqa: E501
        return response

    @doc(description='Get All Activities', tags=['All Activities'])
    @use_kwargs(Flask_DB_RequestSchema, location=('json'))
    @marshal_with(Flask_DB_ResponseSchema)
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


class Begin(Resource):
    def get(self):
        return {'status': 'Online', 'message': 'Bem Vindo'}


api.add_resource(Begin, '/')
api.add_resource(Person, '/person/<string:name>/')
api.add_resource(List_Persons, '/person/')
api.add_resource(Activity, '/activity/<string:person>/')
api.add_resource(Activity_Status, '/activity/<int:id>/')
api.add_resource(List_Activities, '/activity/')

docs.register(Person)
docs.register(List_Persons)
docs.register(Activity)
docs.register(Activity_Status)
docs.register(List_Activities)


if __name__ == '__main__':
    app.run(debug=True)
