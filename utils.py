import json
import random
import string
import hashlib
from pathlib import Path

database = 'data.json'

def load_data():
    data = []
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("No such file exists")
    except Exception as err:
        print(f"Error occured as {err}")
    return data

def update(data):
    with open(database, 'w') as fs:
        fs.write(json.dumps(data, indent=4))

def accountgenerate(acNo):
    alpha = random.choices(string.ascii_letters, k = 3)
    num = random.choices(string.digits, k = 3)
    spchar = random.choices("@#%^%*&^!", k = 1)
    id = alpha + num + spchar
    random.shuffle(id)
    accNo = "".join(id)
    for i in acNo:
        if i == accNo:
            return accountgenerate(acNo)
    return accNo

def hashed_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()