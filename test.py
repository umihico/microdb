
from microdb import MicroDB
import os

filename = "testdata/mdb.json"
test_data = [
    {'job': 'clean', 'name': 'Alice', 'status': 'undone'},
    {'job': 'study', 'name': 'Alice', 'status': 'undone'},
    {'job': 'clean', 'name': 'Bob', 'status': 'undone'},
    {'job': 'study', 'name': 'Bob', 'status': 'undone'},
    {'job': 'clean', 'name': 'Alice', 'status': 'finished'},
]
testpartition_keys = ['job', 'name']


def test():
    if os.path.exists(filename):
        os.remove(filename)

    mdb = MicroDB(filename, testpartition_keys)
    mdb.erase_all()
    mdb = MicroDB(filename, testpartition_keys)
    for d in test_data:
        mdb.upsert(d)
    mdb.save()
    mdb.pprint_all()

    mdb2 = MicroDB(filename, testpartition_keys)
    for d in mdb2.all():
        print(d)
    mdb2.save_as_grid()
    mdb3 = MicroDB(filename, testpartition_keys)
    for d in mdb3.all():
        print(d)
    mdb4 = MicroDB(filename, testpartition_keys)
    mdb4.upsert({'job': 'study', 'name': 'Bob',
                 'status': 'undone', 'extra-info': 'hogehoge'})
    try:
        mdb4.save_as_grid()
    except Exception as e:
        print(e)
    mdb4.save()
    mdb4


if __name__ == '__main__':
    test()
