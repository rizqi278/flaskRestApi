
# A very simple Flask Hello World app for you to get started with...
import mysql.connector
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
mydb = mysql.connector.connect(
    host="rizqi.mysql.pythonanywhere-services.com",
    user="rizqi",
    passwd="taffware",
    database="rizqi$user")
mycursor = mydb.cursor()

cors = CORS(app)
app.config['CORS_ORIGIN'] = '*'
app.config['CORS_METHODS'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'

@app.route('/user', methods=['GET','OPTIONS'])
@cross_origin()
def get(id=None):
    id = request.args.get('id')
    if id:
        sql = 'SELECT * FROM users WHERE id ='+id
        mycursor.execute(sql)
        data = [
                    {
                        'id': row[0],
                        'firstname': row[1],
                        'lastname':row[2],
                        'email':row[3]
                    } for row in mycursor.fetchall()
                ]
        return jsonify(data)

        if len(data)== 0:
            return {
            'status': 500,
            'message': 'Data kosong.',
            'data': None
        }
        else :
            return jsonify(data)
    else :
        mycursor.execute("SELECT * FROM users")
        data = [
                    {
                        'id': row[0],
                        'firstname': row[1],
                        'lastname':row[2],
                        'email':row[3]
                    } for row in mycursor.fetchall()
                ]
        return jsonify(data)

@app.route('/user', methods=['DELETE','OPTIONS'])
@cross_origin()
def deletewithid(id=None):
    id = request.args.get('id')
    if id :
        sql = 'DELETE FROM users WHERE id ='+id
        mycursor.execute(sql)
        mydb.commit()
        return {
            'code': 200,
            'message': 'Data user berhasil dihapus.'
        }
    else :
        return {
            'status': 500,
            'message': 'ID belum di masukkan.'
        }

@app.route('/user', methods=['POST','OPTIONS'])
@cross_origin()
def adddata(firstname=None, lastname=None, email=None):
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    email = request.args.get('email')
    if (firstname, lastname, email):
        mycursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (firstname, lastname, email))
        mydb.commit()
        return {
            'code': 200,
            'message': 'Data user berhasil ditambahkan.'
        }
    else :
        return {
            'code': 500,
            'message': 'Data user gagal ditambahkan.'
        }
@app.route('/cekuser')
def cekuser() :
    return render_template('hello.html')


if __name__ == "__main__":
    app.run()