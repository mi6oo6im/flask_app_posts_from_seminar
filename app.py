from flask import Flask, request
import sqlite3 as sql

# We will use super simple db and we will write row 
# slq queries for this example. Tha aim will be to have
# two endpoints – for fetching all posts from db and
# for creating a post via request arguments.
# example url for a new post: 
# http://127.0.0.1:5000/posts/create/?title=sometitle&text=here%20some%20text
# this creates a post with title "sometitle" and text: "here some text"

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/posts/')
def posts():
    con = sql.connect("posts.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from post")
    res = {}
    rows = cur.fetchall()

    index = 0
    for entry in rows:
         
        res[index] = dict(entry)
        index += 1
    return {"rows": res}


@app.route('/posts/create/')
def create():
    title = request.args.get('title')
    text = request.args.get('text')
    with sql.connect("posts.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO post (title,text) VALUES(?, ?)", (title, text))

        con.commit()
    return {"title": title, "text": text}


if __name__ == '__main__':
    app.run()
