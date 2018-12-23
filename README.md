# microdb
In-memory, Hash-mapping, Disk-writable, Thread-safe database.

Installation with pip
```
$ pip install microdb
```

This database works as list of dictionaries.
```
>>> import microdb
>>> mdb = microdb.MicroDB("testdata/mdb.json", partition_keys=['job', 'name'])
>>> mdb.pprint_all()
[{'job': 'clean', 'name': 'Alice', 'status': 'undone'},
 {'job': 'study', 'name': 'Alice', 'status': 'undone'},
 {'job': 'clean', 'name': 'Bob', 'status': 'undone'},
 {'job': 'study', 'name': 'Bob', 'status': 'undone'}]
 >>> mdb.pprint_all_as_grid()
 [['name', 'status', 'job'],
  ['Alice', 'undone', 'clean'],
  ['Alice', 'undone', 'study'],
  ['Bob', 'undone', 'clean'],
  ['Bob', 'undone', 'study']]
```  
Only 'upsert' method add data, or overwrite if the "key" is already in use.
```
>>> mdb.upsert({'job': 'clean', 'name': 'Alice', 'status': 'finished'})
>>> mdb.upsert({'job': 'clean', 'name': 'Eve', 'status': 'undone'})
>>> mdb.pprint_all()
[{'job': 'clean', 'name': 'Alice', 'status': 'finished'}, # overwritten
 {'job': 'study', 'name': 'Alice', 'status': 'undone'},
 {'job': 'clean', 'name': 'Bob', 'status': 'undone'},
 {'job': 'study', 'name': 'Bob', 'status': 'undone'},
 {'job': 'clean', 'name': 'Eve', 'status': 'undone'}] # new
```  
Key is tupled values of partition_keys. Use 'gen_key' method to see.
key can be checked the existence in database.  
```
>>> mdb.gen_key({'job': 'clean', 'name': 'Bob', 'what': 'ever'})
('clean', 'Bob')
```
'get' method and 'in' operator as same as dict
```
>>> {'job': 'clean', 'name': 'Bob', 'what': 'ever'} in mdb
True
>>> mdb.get({'job': 'study', 'name': 'Alice'})
{'status': 'undone', 'job': 'study', 'name': 'Alice'}
>>> mdb.get({'wrong': 'key'},'when_not_exist') # same as dict.get
'when_not_exist'
```  
Write on disk when you want.
```
>>> mdb.save()

>>> mdb.save_as_grid() # good to reduce amount when all keys are common
$ cat testdata/mdb.json
[['status', 'job', 'name'], ['undone', 'clean', 'Alice'], ['undone', 'study', 'Alice'], ['undone', 'clean', 'Bob'], ['undone', 'study', 'Bob']]

>>> mdb.save('another_file_name.json') # you can write anywhere
$ cat another_file_name.json
[{'job': 'clean', 'name': 'Alice', 'status': 'undone'}, {'job': 'study', 'name': 'Alice', 'status': 'undone'}, {'job': 'clean', 'name': 'Bob', 'status': 'undone'}, {'job': 'study', 'name': 'Bob', 'status': 'undone'}]
```

All operation is already thread-safe by threading.rlock().
In case if you need to block while operations in a row,
```
>>> with mdb.lock():
...    bob_clean_status=mdb.get({'job': 'clean', 'name': 'Bob'})['status']
...    if bob_clean_status != 'finished':
...       mdb.upsert({'job': 'pay_penalty', 'name': 'Bob','status':'undone'})
```
