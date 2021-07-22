from models import Persons, Activities, Users


def insert_person(name, age):
    person = Persons(name=name, age=age)
    print(person)
    person.save()


def update_person(name):
    person = Persons.query.filter_by(name=name).first()
    # person.status = 'Pendant'
    person.save()


def delete_person(name):
    person = Persons.query.filter_by(name=name).first()
    person.delete()


def query_persons():
    person = Persons.query.all()
    print(person)
    for i in person:
        print(i.name, i.id)


def insert_activity(activity, person_id, status):
    activity = Activities(activity=activity, person_id=person_id, status=status)  # noqa: E501
    print(activity)
    activity.save()


def update_activity(activity, status):
    activity = Activities.query.filter_by(activity=activity).first()
    activity.status = status
    activity.save()


def delete_activity():
    activity = Activities.query.filter_by(activity='Python').first()
    activity.delete()


def query_activity():
    activity = Activities.query.all()
    print(activity)
    for i in activity:
        print(i.id, i.activity, i.person_id)


def user_insert(user, password):
    user_ = Users(user=user, password=password)
    print(user_)
    user_.save()


def update_user(user, password):
    user_ = Users.query.filter_by(user=user).first()
    user_.password = password
    user_.save()


def query_users():
    user_ = Users.query.all()
    print(user_)


if __name__ == '__main__':
    # insert_person()
    # update_person()
    # delete_person()
    # query_persons()
    # insert_activity()
    # update_activity()
    # query_activity()
    # delete_activity()
    # user_insert('Chris_0', '1710')
    # user_insert('Chris_1', '1017')
    update_user('Chris_0', '2717')
    query_users()
    pass
