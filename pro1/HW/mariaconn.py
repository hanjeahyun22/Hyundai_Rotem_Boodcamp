import pickle

config = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'password' : '123',
    'database' : 'test',
    'port' : 3306,
    'charset' : 'utf8'
}

with open('mydb.dat', mode = 'wb') as obj:
    pickle.dump(config, obj)