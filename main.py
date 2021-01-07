import mysql.connector

cnx = mysql.connector.connect(user='root', password='ayk123', host='localhost', database='cinema')
mycursor = cnx.cursor();
mycursor.execute("TRUNCATE TABLE users;")
mycursor.execute("TRUNCATE TABLE tickets;")

ticketid = 0
userid = 0

class Ticket:
    def __init__(self, row, column, price):
        self.row = row
        self.column = column
        self.price = price


class User: 
    def __init__(self, ticket, name="", gender="", age=1, phn_no=""):
        self.name = name
        self.gender = gender
        self.age = age
        self.phn_no = phn_no
        self.ticket = ticket
   
    def buyTicket(self):
        global ticketid
        ticketid += 1
        global userid
        userid += 1
        self.name = input("Enter name: ")
        self.gender = input("Enter gender: ")
        self.age = input("Enter age: ")
        self.phn = input("Enter phn: ")
        mycursor.execute('INSERT INTO tickets VALUES (%s, %s, %s, %s)', (ticketid, self.ticket.row, self.ticket.column, self.ticket.price));
        cnx.commit()
        mycursor.execute('INSERT INTO users VALUES (userid, %s, %s, %s, %s, %s)',( self.name, self.gender, self.age, self.phn, ticketid));
        cnx.commit()
        print("\nTicket booked successfully!")


rows = int(input("Enter number of rows in Cinema: "))
columns = int(input("Enter number of rows each row: "))
price = 0
users = []
tickets = []


def showSeats():
    global users
    global tickets
    mycursor.execute("SELECT * FROM users;")
    users = mycursor.fetchall()
    mycursor.execute("SELECT * FROM tickets;")
    tickets = mycursor.fetchall()
    print("  ", end="")
    for i in range(columns):
        print(i+1, end=" ")
    print()
    for i in range(rows):
        print(i+1, end=" ")
        for j in range(columns):
            for t in tickets:
                if t[1] - 1 == i and t[2] - 1 == j:
                    print("B", end=" ")
                    break
            else:
                print("S", end=" ")
        print()

def statistics():
    global users
    global tickets
    mycursor.execute("SELECT * FROM users;")
    users = mycursor.fetchall()
    mycursor.execute("SELECT * FROM tickets;")
    tickets = mycursor.fetchall()
    print("Number of purchased tikets: ", len(tickets), sep="")
    total_seats = rows * columns
    perc = len(tickets)/total_seats*100
    print("Percentage: %.2f"%perc,"%", sep="")
    current_income = 0
    if rows * columns <= 60:
        current_income = 10 * len(tickets)
    else:
        for t in tickets:
            if t[1] <= rows//2:
                current_income += 10
            else:
                current_income += 8

    print("Current income: $", current_income, sep="")

    total_income = 0
    if rows * columns <= 60:
        total_income = rows * columns * 10
    else:
        div = rows // 2
        total_income = div * columns * 10 + (rows - div) * columns * 8

    print("Total income: $", total_income, sep="")

def showUserInfo(row, column):
    mycursor.execute("SELECT users.name, users.gender, users.age, users.phn_no, tickets.price FROM users INNER JOIN tickets ON users.ticketid = tickets.ticketid where tickets.rowno = %s and tickets.columnno = %s;", (row, column))
    userinfo = mycursor.fetchall()
    print("\nName: ", userinfo[0][0], "\nGender: ", userinfo[0][1], "\nAge: ", userinfo[0][2], "\nTicket price: ", userinfo[0][4], "\nPhone No: ", userinfo[0][3], sep="")

while True:
    print("\n\n1. Show the seats\n2. Buy a ticket\n3. Statistics\n4. Show booked tickets user info\n0. Exit")
    ch = int(input())
    if not ch:
        print("Thank you.")
        break
    if ch==1 or ch==2 or ch==3 or ch==4:
        if ch == 1:
            showSeats()

        if ch == 2:
            r = int(input("Enter row: "))
            c = int(input("Enter column: "))
            flag = True
            for ticket in tickets:
                if ticket[1] == r and ticket[2] == c:
                    print("Seat is already booked.")
                    break
            else:
                if rows * columns <= 60:
                    price = 10
                elif r <= rows//2:
                    price = 10
                else:
                    price = 8
                print("The price of your selected seat is: ", price)
                if(input("Do you wish to book the ticket?(y/n)").lower() == 'y'):
                    ticket = Ticket(r, c, price)
                    u = User(ticket)
                    u.buyTicket()

        if ch == 3:
            statistics()

        if ch == 4:
            r = int(input("Enter row: "))
            c = int(input("Enter column: "))
            showUserInfo(r, c)

    else:
        print("Enter valid option.")    