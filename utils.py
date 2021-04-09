from models import Person


def insert_person():
    person = Person(name="Ricardo", age=50)
    print(person)
    person.save()


def query_all_person():
    person = Person.query.all()
    print(person)


def query_person():
    person = Person.query.filter_by(name="Ricardo").first()
    print(person.age, person.name, person.id)


def alter_person():
    person = Person.query.filter_by(name="Ricardo").first()
    person.age = 49
    person.save()


def delete_person():
    person = Person.query.filter_by(name="Ricardo").first()
    person.delete()


if __name__ == '__main__':
    # insert_person()
    # alter_person()
    delete_person()
    query_all_person()
    # query_person()
