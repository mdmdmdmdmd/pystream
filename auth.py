import os
import json
import hashlib
import binascii
import getpass


db_name = 'auth.db'

def check_db():
    if not os.path.isfile(db_name):
        db = open(db_name,'w')
        db.close()

def read_db():
    try:
        db = open(db_name, "r")
    except:
        check_db()
        read_db()
    try:
        list = json.load(db)
        db.close()
        return list
    except:
        return {}

def update_db(username, password):
    data = read_db()
    data.update({username: password})
    db = open(db_name, 'w')
    json.dump(data, db)
    db.close()

def main():
    username = input('username: ')
    hashpass = binascii.b2a_base64(hashlib.pbkdf2_hmac('sha512', bytes(getpass.getpass(prompt='password: '), encoding='utf-8'), b'gDR%AEtgewt4qT43', 100000))[:-1].decode('utf-8')
    update_db(username, hashpass)
    print(read_db())

if __name__ == '__main__':
    main()
