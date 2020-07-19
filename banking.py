import  random
import sqlite3

def create_db():
    cur = con.cursor()
    query_text = create_table()
    cur.execute(query_text)
    con.commit()

def create_table():
    text = '''CREATE TABLE IF NOT EXISTS card (id INTEGER,
           number TEXT,
           pin TEXT,
           balance INTEGER DEFAULT 0);'''
    # text = 'DROP table card'
    return text

def add_to_db(id, card_number, PIN):
    text = 'INSERT INTO card (id, number, pin)' \
           'VALUES ('+ str(id) +',' + card_number + ',' + PIN + ' );'
    cur = con.cursor()
    cur.execute(text)
    con.commit()

def create_account(id):
    card_number = '400000' + str(random.randint(0, 999999999)).zfill(9)
    card_number_list = list(map(int, card_number))
    #  Luhn algorithm
    for i in range(0, 15,2):
        card_number_list[i] *= 2
        if card_number_list[i] > 9:
            card_number_list[i] -= 9
    sum_digits = sum(card_number_list)
    i = 0
    while (i + sum_digits) % 10 != 0:
        i+= 1
    card_number += str(i)

    PIN = str(random.randint(0,9)).zfill(4)
    add_to_db(id, card_number, PIN)
    return card_number, PIN

def check_Luhn_algorithm(recipient):
    card_number_list = list(map(int, recipient))
    for i in range(0, 15,2):
        card_number_list[i] *= 2
        if card_number_list[i] > 9:
            card_number_list[i] -= 9
    sum_digits = sum(card_number_list) - card_number_list[-1]
    i = 0
    while (i + sum_digits) % 10 != 0:
        i+= 1

    if i == card_number_list[-1]:
        return True
    return False

def print_card_info(card_number, PIN):
    print(f'''Your card has been created
Your card number:
{card_number}
Your card PIN:
{PIN}\n''''')


def logged_in(card_number, PIN):
    print('''1. Balance
    2. Add income
    3. Do transfer
    4. Close account
    5. Log out
    0. Exit\n''')

    user_input = input()
    if user_input == '1': # balance
        # balance = cards[card_number]['balance']
        balance = check_balance(card_number)
        print(f'Balance: ' + balance+'\n')
        return logged_in(card_number, PIN)
    elif user_input == '2': # add income
        income = int(input("Enter income:"))
        add_income(card_number, income)
        print('Income was added!')
        return logged_in(card_number, PIN)
    elif user_input == '3': # do transfer
        do_transfer(card_number)
        return logged_in(card_number, PIN)
    elif user_input == '4': # close account
        close_account(card_number)
        print('The account has been closed!')
    elif user_input == '5': # log out
        print('You have successfully logged out!\n')
    elif user_input == '0':
        print('Bye!')
        return 'exit'

def greetings():
    print('''1. Create an account
2. Log into account
0. Exit\n''')

def check_PIN(card_number, PIN):
    text = '''SELECT pin
     FROM card 
     WHERE number = ''' + card_number + ';'
    cur = con.cursor()
    cur.execute(text)
    row = cur.fetchone()
    try:
        if len(row):
            PIN_in_db = str(row[0]).zfill(4)
            if PIN_in_db == PIN:
                return True
    except TypeError:
        return False

def check_balance(card_number):
    text = '''SELECT balance
       FROM card 
       WHERE number = ''' + card_number + ';'
    cur = con.cursor()
    cur.execute(text)
    balance = cur.fetchone()[0]
    return balance

def check_card(recipient):
    text = 'SELECT number FROM card WHERE number = ' + recipient + ';'
    cur = con.cursor()
    cur.execute(text)
    try:
        len(cur.fetchone())
        return True
    except:
        return False

def add_income(card_number, income):
    text = 'UPDATE card SET balance = balance +' +\
    str(income)  + ' WHERE number = ' + card_number +';'
    cur = con.cursor()
    cur.execute(text)
    con.commit()

def close_account(card_number):
    text = 'DELETE FROM card WHERE number = ' + card_number + ';'
    cur = con.cursor()
    cur.execute(text)
    con.commit()

def do_transfer(card_number):
    print('Transfer')
    recipient = input('Enter card number:')
    Luhn = check_Luhn_algorithm(recipient)
    if not Luhn:
        print('Probably you made mistake in the card number. Please try again!')
        return
    card_exists = check_card(recipient)
    if card_exists:
        amount = int(input('Enter how much money you want to transfer:'))
        balance = check_balance(card_number)
        if balance < amount:
            print('Not enough money!')
        else: # Transfering
            transfer_money(card_number, recipient, amount)
            print('Success!')
    else:
        print('Such a card does not exist.')

def transfer_money(card_number, recipient, income):
    text = 'UPDATE card SET balance = balance +' + \
           str(income) + ' WHERE number = ' + recipient + ';'
    cur = con.cursor()
    cur.execute(text)
    con.commit()

    text = 'UPDATE card SET balance = balance - ' + \
           str(income) + ' WHERE number = ' + card_number + ';'
    cur = con.cursor()
    cur.execute(text)
    con.commit()

global con
con = sqlite3.connect('card.s3db')
create_db()
greetings()
# cards = {}
id = 0
while True:
    user_input = input()
    if user_input == '1':
        id += 1
        card_number, PIN = create_account(id)
        # cards[card_number] = {'PIN' : PIN, 'balance' : 0}
        print_card_info(card_number, PIN)
        greetings()
    elif user_input == '2':
        card_number = input('Enter your card number:')
        PIN = input('Enter your PIN:')
        PIN_correct = check_PIN(card_number, PIN)
        # try:
        #     if cards[card_number]['PIN'] == PIN:
        if PIN_correct:
            print('You have successfully logged in!')
            res = logged_in(card_number, PIN),
            if res[0] == 'exit' or res == 'exit':
                break
        else:
            print('Wrong card number or PIN!')
            greetings()
        # except KeyError:
            # print('Wrong card number or PIN!')
            # greetings()
    elif user_input == '0':
        print('Bye!')
        break

con.close()