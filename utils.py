from models import Persons, Activities, db_session


def insert_person():
    person = Persons(name='Josue', age=23)
    print(person)
    person.save()


def update_person():
    person = Persons.query.filter_by(name='Chris').first()
    # person.status = 'Pendant'
    person.save()


def delete_person():
    person = Persons.query.filter_by(name='Glauber').first()
    person.delete()


def query_persons():
    person = Persons.query.all()
    print(person)
    for i in person:
        print(i.name, i.id)


def insert_activity():
    activity = Activities(activity='Front-End', person_id= 2, status= 'Pendant')
    print(activity)
    activity.save()


def update_activity():
    activity = Activities.query.filter_by(activity='Python').first()
    activity.status = 'Pendant'
    activity.save()


def delete_activity():
    activity = Activities.query.filter_by(activity='Python').first()
    activity.delete()


def query_activity():
    activity = Activities.query.all()
    print(activity)
    for i in activity:
        print(i.id, i.activity, i.person_id)


if __name__ == '__main__':
    # insert_person()
    # update_person()
    # delete_person()
    # query_persons()
    # insert_activity()
    # update_activity()
    query_activity()
    # delete_activity()
    pass