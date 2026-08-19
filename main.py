import sys
from bank import Bank


user = Bank()
accNo, pin = user.login()

if accNo is None:
    user.create_account()
    sys.exit()

menu = True
while menu == True:
    print("press 1 for Creating an account")
    print("press 2 for Deposit money in your account")
    print("press 3 for Withdraw money")
    print("press 4 for Details")
    print("press 5 for Updating the account details")
    print("press 6 for Deleting your account")
    print("press 7 for transaction History\n")
    try:
        check = int(input("Enter your response: "))
        print("\n\n")
        if check == 1:
            accNo, pin = user.create_account()

        elif check == 2:
            amount = int(input("Enter the amount you want to deposit: "))
            user.deposit_money(accNo, pin, amount)

        elif check == 3:
            amount = int(input("Enter the amount you want to withdraw: "))
            user.withdraw_money(accNo, pin, amount)

        elif check == 4:
            user.details(accNo, pin)

        elif check == 5:
            user.update_details(accNo, pin)
            pin = user.acNo[accNo]

        elif check == 6:
            user.delete_account(accNo, pin)

        elif check == 7:
            user.transaction_history(accNo, pin)

        else:
            print("You entered invalid response, Please try to login again\n")
            sys.exit()

    except Exception as err:
        print(f"Error occur as {err}")

    try:
        proceed = int(input("Enter 1 to logout or enter 2 to continue: "))
        print("\n")
        if proceed == 1:
            menu = False
            print("You are logged out\n")
        else:
            menu = True

    except Exception as err:
        print(f"Error occur as {err}")