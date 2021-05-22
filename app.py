from flask import Flask, render_template, request, redirect
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect('myBank.db')
c = conn.cursor()
#c.execute('''CREATE TABLE CustomerDetails (rowid INT, customerName VARCHAR(20), email VARCHAR(50), transacId INT PRIMARY KEY, Balance INT)''')
#c.execute('''CREATE TABLE TransferDetails (rowid INTEGER PRIMARY KEY AUTOINCREMENT, SenderName VARCHAR(20), senderId INT, ReceiverName VARCHAR(20), receiverId INT, amountTransferred INT)''')
#records = [(1, 'Peter', 'pet@gmail.com', 101, 10000),
#              (2, 'Amy', 'amy@gmail.com', 102, 50000),
#              (3, 'Bob', 'bob@gmail.com', 103, 5000),
#               (4, 'Hannah', 'han@gmail.com', 104, 3000),
#              (5, 'Sandy', 'San@gmail.com', 105, 9000),
#              (6, 'Betty', 'betty@gmail.com', 106, 1000),
#              (7, 'Richard', 'Richard@gmail.com', 107, 2000),
#              (8, 'Vicky', 'vicky@gmail.com', 108, 6500),
#              (9, 'Ben', 'Ben@gmail.com', 109, 5555),
#              (10, 'Willaim', 'william@gmail.com', 110, 20000)]
#c.executemany('INSERT INTO CustomerDetails VALUES (?,?,?,?,?);', records)
#conn.commit()
#conn.close()

@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/transfer/<int:senderid>/')
def transferpage(senderid):
    return render_template('transfer.html')
    

@app.route('/transferamount/<int:sid>/<int:rid>/<int:amt>/')
def addAmount(sid, rid, amt):
    conn = sqlite3.connect('myBank.db')
    c = conn.cursor()

    c.execute("SELECT * FROM CustomerDetails WHERE transacId = "+str(sid))
    sen_details = c.fetchall()
    sen_bal = sen_details[0][4] - amt
    
    c.execute("SELECT * FROM CustomerDetails WHERE transacId = "+str(rid))
    rec_details = c.fetchall()
    rec_bal = rec_details[0][4] + amt

    c.execute("UPDATE customerDetails SET Balance ="+str(sen_bal)+" WHERE transacId ="+str(sid))
    c.execute("UPDATE customerDetails SET Balance ="+str(rec_bal)+" WHERE transacId ="+str(rid))
    transfer_details = [sen_details[0][1], sid, rec_details[0][1], rid, amt]
    c.execute('INSERT INTO TransferDetails(SenderName, senderId, ReceiverName, receiverId, amountTransferred) VALUES (?,?,?,?,?)', transfer_details)

    conn.commit()
    conn.close()
    return "transferred"


@app.route('/getParticularTransferHistory/<int:Id>/')
def getParticularTransferHistory(Id):
    conn = sqlite3.connect('myBank.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM TransferDetails WHERE senderId ="+str(Id)+" OR receiverId ="+str(Id)+";")
    transferDetails = c.fetchall()
    conn.commit()
    conn.close()
    return render_template('transferhistory.html', transferDetails=transferDetails)



@app.route('/getAllCustomerDetails/')
def getAllCustomerDetails():
    conn = sqlite3.connect('myBank.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM CustomerDetails")
    customerDetails = c.fetchall()
    conn.commit()
    conn.close()
    return render_template('details.html', customerDetails=customerDetails)



@app.route('/getAllTransferHistory/')
def getAllTransferHistory():
    conn = sqlite3.connect('myBank.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM TransferDetails")
    transferDetails = c.fetchall()
    conn.commit()
    conn.close()
    return render_template('transferhistory.html', transferDetails=transferDetails)

if __name__ == "__main__":
    app.run(debug=True)
