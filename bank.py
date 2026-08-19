import datetime
import hashlib
from utils import load_data, update, accountgenerate, hashed_pin


class Bank:
    database = 'data.json'
    data = load_data()

    acNo = {x['accountNo.'] : x['pin'] for x in data }

    def get_user(self, accNo, pin):
        for user in Bank.data:
            if user['accountNo.']==accNo and user['pin']==pin:
                return user
        return None


    #Login()
    def login(self):
        accNo = input("Press Enter to Create new account or Enter your account Number:")

        if accNo == "":
            return None, None

        if accNo not in self.acNo:
            print("Account number not found")
            return None, None

        pin = input("Enter your 4 digit pin: ")
        hashed = hashlib.sha256(pin.encode()).hexdigest()

        if hashed != self.acNo[accNo]:
            print("Incorrect Pin")
            return None, None

        print("Login successful\n\n")
        return accNo, hashed


    #Hashed-pin
    def hashed_pin(self, pin):
        return hashed_pin(pin)


    def create_account(self):
        n = True
        while n == True:
            Name = input("Enter Full name: ")
            if Name.replace(" ","").isalpha() == False:
                print("Please enter a valid name.")
            else:
                n = False

        x = True
        while x == True:
            pin = input("Create 4 digit pin : ")
            if pin.isdigit() == False or len(pin) != 4:
                print("Please enter valid pin of 4 digits")
                x = True
            else:
                x = False

        m = True
        while m == True:
            mail = input("Enter your mail id: ")
            email_exist = False
            for i in Bank.data:
                    if i['email'] == mail:
                        print("Sorry, This email already exist, you cannot create 2 account with one email.")
                        email_exist = True
                        break
            if email_exist:
                continue
            if mail.endswith("@gmail.com") == False or mail == "@gmail.com" or mail == "":
                print("Please enter valid email")
            else:
                m = False

        try:
            info = {
                "name" : Name,
                "age"  : int(input("Enter your age: ")),
                "email": mail,
                "pin" : self.hashed_pin(pin),
                "accountNo." : accountgenerate(self.acNo),
                "balance" : 0,
                "transaction" : []
            }

            if info['age'] < 18:
                print("Sorry, you must be atleast 18yrs old.")
                return

            else:
                print("Your account has been successfully created")
                for i in info:
                    print(f"{i} : {info[i]}")
                print("please note down your account number")

            Bank.data.append(info)
            self.acNo[info['accountNo.']] = info['pin']
            update(Bank.data)
            return info["accountNo."], info["pin"]

        except Exception as err:
            print(f"Error occured as {err}")
            return


    #Deposit Money
    def deposit_money(self, accNo, pin, amount):
        userdata = self.get_user(accNo, pin)
        try:
            if not userdata:
                print("Sorry, no account found")
            else:
                money = amount

                if money >= 10001 or money <= 0:
                    print("transaction cannot be processed, amount must be below 10000 and above 0")
                else:
                    userdata['balance'] += money
                    x = datetime.datetime.now()
                    new_transaction = {
                        'type' : "Deposit",
                        'transactionID' : f"TXN-{userdata['accountNo.']}-{len(userdata['transaction'])+1}",
                        'amount' : money,
                        'date' : x.strftime("%d-%B-%Y"),
                        'time' : x.strftime("%H:%M:%S"),
                        'new_Balance' : userdata['balance']
                    }

                    userdata['transaction'].append(new_transaction)
                    update(Bank.data)
                    print(f"Your money deposited successfully and your txnID : {new_transaction['transactionID']}")
        except Exception as err:
            print(f"Error occured as {err}")


    def withdraw_money(self, accNo, pin, amount):
        userdata = self.get_user(accNo,pin)
        try:
            if not userdata:
                print("Sorry, we couldn't find your account, please login again.")
            else:
                money = amount
                if money > 10001 or money < 1:
                    print("you cannot withdraw amount above Rs.10000 or less than Rs.1")
                elif money > userdata['balance']:
                    print("You don't have sufficient balance")
                else:
                    userdata['balance'] -= money
                    x = datetime.datetime.now()
                    new_transaction = {
                        'type' : "Withdraw",
                        'transactionID' : f"TXN-{userdata['accountNo.']}-{len(userdata['transaction'])+1}",
                        'amount' : money,
                        'date' : x.strftime("%d-%B-%Y"),
                        'time' : x.strftime("%H:%M:%S"),
                        'new_Balance' : userdata['balance']
                    }

                    userdata['transaction'].append(new_transaction)
                    update(Bank.data)
                    print(f"Your withdrawal is successful and your txnID : {new_transaction['transactionID']}")
        except Exception as err:
            print(f"Exception occur as {err}")


    def details(self, accNo, pin):
        userdata = self.get_user(accNo, pin)
        if not userdata:
            print("Sorry, this account doesn't exists.\n")
        else:
            print(f"Your account details are:\n{userdata}\n")


    def update_details(self, accNo, pin):
        userdata = self.get_user(accNo,pin)
        if not userdata:
            print("Sorry, this account doesn't exists\n")
        else:
            print("Userdata is : \n\n", userdata)
            print("you cannot change age, account number and balance")
            ihash = input("Write new pin or enter your current pin:  ")
            newdata = {
            'name' : input("Write new NAME or press Enter to skip: "),
            'email' : input("Write new EMAIL or press Enter to skip"),
            'pin' : hashlib.sha256(ihash.encode()).hexdigest()
            }

            if newdata["name"] == "":
                newdata["name"] = userdata['name']
            if newdata["email"] == "":
                newdata["email"] = userdata['email']
            if ihash == "":
                newdata["pin"] = userdata["pin"]
            else:
                newdata["pin"] = self.hashed_pin(ihash)

            newdata['age'] = userdata['age']
            newdata['accountNo.'] = userdata['accountNo.']
            newdata['balance'] = userdata['balance']

            for i in newdata:
                if newdata[i] == userdata[i]:
                    continue
                else:
                    userdata[i] = newdata[i]

            self.acNo[accNo] = newdata['pin']
            update(Bank.data)
            print("Account updated succesfully\n")


    def delete_account(self, accNo, pin):
        userdata = self.get_user(accNo,pin)
        if not userdata:
            print("This account doesn't exists\n")
        else:
            check = input("press y if you wanna actually delete this account, otherwise press n: ")
            if check == 'n' or check == 'N':
                pass
            else:
                index = Bank.data.index(userdata)
                Bank.data.pop(index)
                print('\n')
                del self.acNo[userdata["accountNo."]]
                print("Your account deleted successfully\n")
                update(Bank.data)


    def transaction_history(self, accNo, pin):
        userdata = self.get_user(accNo,pin)
        if not userdata:
            print("No user found")
        else:
            print(f"Transaction history for account number: {accNo} is: " )
            trsxn = userdata['transaction']
            for i in reversed(trsxn):
                print(f"{i['type']} : {i.get('transactionID', 'N/A')} : ₹{i['amount']}, Balance: {i.get('new_Balance', i.get('new_Banlance'))}, {i['date']} - {i['time']}\n\n")