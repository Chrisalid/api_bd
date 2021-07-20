from models import Persons, Activities, db_session


def insert_person():
    person = Persons(name='Glauber', age=22)
    print(person)
    person.save()


def update_person():
    person = Persons.query.filter_by(name='Chris').first()
    person.age = 21
    person.save()


def delete_person():
    person = Persons.query.filter_by(name='Glauber').first()
    person.delete()


def query_persons():
    person = Persons.query.all()
    print(person)
    person = Persons.query.filter_by(name='Glauber').first()
    print(person.id)


def insert_activity():
    activity = Activities(activity='Front-End', person_id= 1)
    print(activity)
    activity.save()


def update_activity():
    # activity = Activities.query.filter_by(name=).first()
    activity.save()


def delete_activity():
    activity = Activities.query.filter_by(activity='Front-End').first()
    activity.delete()


def query_activity():
    activity = Activities.query.all()
    print(activity)
    # activity = Activities.query.filter_by(activity='Front-End').first()
    # print(activity)


if __name__ == '__main__':
    # insert_person()
    # update_person()
    # delete_person()
    # query_persons()
    # insert_activity()
    # query_activity()
    # delete_activity()
    pass