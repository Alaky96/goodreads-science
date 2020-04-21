from flask import Flask, render_template, request
import psycopg2
import dbconfig
import json

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index'


@app.route('/hello')
def hello():
    return render_template('hello.html')


@app.route('/getdata', methods=['GET'])
def getdata():
    minrating = request.args.get("minrating") if request.args.get("minrating") else 0
    maxrating = request.args.get("maxrating") if request.args.get("maxrating") else 5
    minpages = request.args.get("minpages") if request.args.get("minpages") else 0
    maxpages = request.args.get("maxpages") if request.args.get("maxpages") else 100000
    conn = (psycopg2.connect
            (host=dbconfig.host, database=dbconfig.database, user=dbconfig.username, password=dbconfig.password))
    cur = conn.cursor()
    cur.execute("select * from books where nb_pages > 0 and average_ratings >= %s and average_ratings <= %s and nb_pages >= %s and nb_pages <= %s", (minrating, maxrating, minpages, maxpages))
    books = cur.fetchall()
    list_book = []
    for row in books:
        list_book.append({"id": row[0], "title": row[8], "nb_pages": row[2], "average_ratings": str(row[4])})
    cur.close()
    return json.dumps(list_book)


if __name__ == '__main__':
    app.run()
