from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(   
        host="postgres", 
	database="mydb",
	user="admin",
	password="admin123"
    )

@app.route('/')
def home():
    return "DevOps Lab App is running.."
@app.route('/add', methods=['POST'])
def add():
    data = request.json.get('message')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, text TEXT)")
    cur.execute("INSERT INTO messages (text) VALUES (%s)", (data,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "saved", "message": data})

@app.route('/messages')
def messages():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
