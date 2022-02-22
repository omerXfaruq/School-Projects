import sqlite3

from flask import Flask, render_template, request
import json
import pymysql
import pymysql.cursors

conn = pymysql.connect(host='localhost', user='root', password='new_password', db='cmpe321', charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

c = conn.cursor()


def delete_tables():
    c.execute('DROP TABLE IF EXISTS AUTHOR')
    c.execute('DROP TABLE IF EXISTS PAPER')
    c.execute('DROP TABLE IF EXISTS PAPER2')
    c.execute('DROP TABLE IF EXISTS PAPER3')
    c.execute('DROP TABLE IF EXISTS SOTA')

    conn.commit()


def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS AUTHOR(nameSurname TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS PAPER(title TEXT ,abstract TEXT,result INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS PAPER2(title TEXT,topic TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS PAPER3(title TEXT,nameSurname TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS SOTA(topic TEXT,SOTA INTEGER)')
    c.execute(
        'DELIMITER $$ CREATE TRIGGER updateSota1 AFTER INSERT ON PAPER FOR EACH ROW BEGIN UPDATE SOTA    SET SOTA=(select max(paper.result) from paper,paper2 where paper2.topic=sota.topic and paper.title=paper2.title); END$$ DELIMITER')
    c.execute(
        'DELIMITER $$ CREATE TRIGGER updateSota2 AFTER INSERT ON PAPER2 FOR EACH ROW BEGIN UPDATE SOTA    SET SOTA=(select max(paper.result) from paper,paper2 where paper2.topic=sota.topic and paper.title=paper2.title); END$$ DELIMITER')
    c.execute(
        'DELIMITER $$ CREATE TRIGGER updateSota3 AFTER DELETE ON PAPER FOR EACH ROW BEGIN UPDATE SOTA    SET SOTA=(select max(paper.result) from paper,paper2 where paper2.topic=sota.topic and paper.title=paper2.title); END$$ DELIMITER')
    c.execute(
        'DELIMITER $$ CREATE TRIGGER updateSota4 AFTER DELETE ON PAPER2 FOR EACH ROW BEGIN UPDATE SOTA    SET SOTA=(select max(paper.result) from paper,paper2 where paper2.topic=sota.topic and paper.title=paper2.title); END$$ DELIMITER')
    c.execute(
        'DELIMITER // CREATE PROCEDURE SelectCoAuthors (IN con VARCHAR(50)) BEGIN SELECT DISTINCT P2.nameSurname FROM PAPER3 AS P1, PAPER3 AS P2 WHERE P1.nameSurname = con AND P1.TITLE = P2.TITLE AND P2.nameSurname<>con; END // ')

    conn.commit()


def data_entry():
    c.execute('INSERT INTO AUTHOR VALUES("Ahmed Akar")')
    c.execute('INSERT INTO AUTHOR VALUES("Vei Cakar")')
    c.execute('INSERT INTO PAPER VALUES(\"Ali Keser\",\"myAbstract\",123)')
    c.execute('INSERT INTO PAPER2 VALUES(\"Ali Keser\",\"topic1\")')
    c.execute('INSERT INTO PAPER2 VALUES(\"Ali Keser\",\"topic2\")')
    c.execute('INSERT INTO PAPER3 VALUES("Ali Keser", "Ahmed Akar")')
    c.execute('INSERT INTO PAPER3 VALUES("Ali Keser", "Vei Cakar")')

    conn.commit()


def data_delete():
    c.execute('DELETE FROM PAPER WHERE title=\"Ali Keser\"')
    c.execute('DELETE FROM PAPER2 WHERE title=\"Ali Keser\"')

    conn.commit()


def data_retrieval():
    (c.execute('SELECT PAPER.title,PAPER3.nameSurname FROM PAPER,PAPER3 WHERE PAPER.title=PAPER3.title'))
    # (c.execute('SELECT * FROM AUTHOR'))

    for i in (c.fetchall()):
        s = ""
        for k in i:
            s += str(k)
            s += " "
        print(s, '-----', i)


def exit():
    c.close()
    conn.close()


# delete_tables()
# create_tables()
# data_entry()
# data_retrieval()

exit()


def exit(c, conn):
    c.close()
    conn.close()


#####

@app.route('/')
def form_post():
    return render_template('about.html')


@app.route("/endAuthor", methods=['POST'])
def endAuthor():
    #    conn = sqlite3.connect("tutorial.db")
    #    c = conn.cursor()

    conn = pymysql.connect(host='localhost', user='root', password='new_password', db='cmpe321', charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    c = conn.cursor()
    if request.method == 'POST':
        if (request.form["type"] == "ADD"):
            name = request.form["authorName"]
            sql = "INSERT INTO AUTHOR VALUES (%s)"
            c.execute(sql, (name))
            conn.commit()
            return "" + '<br> <a href=" / "> Return to home page </a>'
        elif request.form["type"] == "UPDATE":
            sql = 'UPDATE AUTHOR SET nameSurname=%s WHERE nameSurname=%s'
            c.execute(sql, (request.form["newAuthorName"], request.form["oldAuthorName"]))

            sql = 'UPDATE PAPER3 SET nameSurname=%s WHERE nameSurname=%s'
            c.execute(sql, (request.form["newAuthorName"], request.form["oldAuthorName"]))

            conn.commit()
            return " " + '<br> <a href=" / "> Return to home page </a>'
        elif request.form["type"] == "DELETE":
            sql = 'DELETE FROM AUTHOR WHERE nameSurname=%s'
            c.execute(sql, (request.form["authorName"]))

            sql = 'DELETE FROM PAPER3 WHERE nameSurname=%s'
            c.execute(sql, (request.form["authorName"]))

            conn.commit()
            return " " + '<br> <a href=" / "> Return to home page </a>'

    exit(c, conn)
    return (request.form["type"])


@app.route("/endTopic", methods=['POST'])
def endTopic():
    conn = pymysql.connect(host='localhost', user='root', password='new_password', db='cmpe321', charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    c = conn.cursor()

    if request.method == 'POST':
        if (request.form["type"] == "ADD"):
            name = request.form["topicName"]
            sql = "INSERT INTO SOTA VALUES (%s,%s)"
            c.execute(sql, (name, 0))
            conn.commit()
            return " " + '<br> <a href=" / "> Return to home page </a>'
        elif request.form["type"] == "UPDATE":
            sql = 'UPDATE SOTA SET topic=%s WHERE topic=%s'
            c.execute(sql, (request.form["newTopicName"], request.form["oldTopicName"]))
            sql = 'UPDATE PAPER2 SET topic=%s WHERE topic=%s'
            c.execute(sql, (request.form["newTopicName"], request.form["oldTopicName"]))

            conn.commit()
            return " " + '<br> <a href=" / "> Return to home page </a>'
        elif request.form["type"] == "DELETE":
            sql = 'DELETE FROM SOTA WHERE topic=%s'
            c.execute(sql, (request.form["topicName"]))

            sql = 'DELETE FROM PAPER2 WHERE topic=%s'
            c.execute(sql, (request.form["topicName"]))

            conn.commit()
            return " " + '<br> <a href=" / "> Return to home page </a>'

    exit(c, conn)
    return (request.form["type"])


@app.route("/endPaper", methods=['POST'])
def endPaper():
    # conn = sqlite3.connect("tutorial.db")
    # c = conn.cursor()

    conn = pymysql.connect(host='localhost', user='root', password='new_password', db='cmpe321', charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    c = conn.cursor()

    if request.method == 'POST':
        if (request.form["type"] == "ADD"):
            authorList = request.form["paperAuthors"].split(",")
            topicList = request.form["paperTopics"].split(",")
            sql = "INSERT INTO PAPER VALUES (%s,%s,%s)"
            c.execute(sql, (request.form["paperTitle"], request.form["paperAbstract"], request.form["paperResult"]))

            sql = "INSERT INTO PAPER3 VALUES (%s,%s)"
            for i in authorList:
                c.execute(sql, (request.form["paperTitle"], i))

            sql = "INSERT INTO PAPER2 VALUES (%s,%s)"
            for i in topicList:
                c.execute(sql, (request.form["paperTitle"], i))

            conn.commit()

            return " " + '<br> <a href=" / "> Return to home page </a>'
        elif request.form["type"] == "UPDATE":
            authorList = request.form["paperAuthors"].split(",")
            topicList = request.form["paperTopics"].split(",")

            sql = "DELETE FROM PAPER WHERE title=%s"
            c.execute(sql, (request.form["paperOldTitle"]))

            sql = "DELETE FROM PAPER2 WHERE title=%s"
            c.execute(sql, (request.form["paperOldTitle"]))

            sql = "DELETE FROM PAPER3 WHERE title=%s"
            c.execute(sql, (request.form["paperOldTitle"]))

            sql = "INSERT INTO PAPER VALUES (%s,%s,%s)"
            c.execute(sql, (request.form["paperNewTitle"], request.form["paperAbstract"], request.form["paperResult"]))

            sql = "INSERT INTO PAPER3 VALUES (%s,%s)"
            for i in authorList:
                c.execute(sql, (request.form["paperNewTitle"], i))

            sql = "INSERT INTO PAPER2 VALUES (%s,%s)"
            for i in topicList:
                c.execute(sql, (request.form["paperNewTitle"], i))

            conn.commit()

            return '<br> <a href=" / "> Return to home page </a>'
        elif request.form["type"] == "DELETE":

            sql = 'DELETE FROM PAPER WHERE title=%s'
            c.execute(sql, (request.form["paperTitle"]))
            sql = 'DELETE FROM PAPER2 WHERE title=%s'
            c.execute(sql, (request.form["paperTitle"]))
            sql = 'DELETE FROM PAPER3 WHERE title=%s'
            c.execute(sql, (request.form["paperTitle"]))

            conn.commit()
            return " " + '<br> <a href=" / "> Return to home page </a>'

    exit(c, conn)
    return (request.form["type"])


@app.route('/endUser', methods=['POST'])
def endUser():
    # conn = sqlite3.connect("tutorial.db")
    # c = conn.cursor()

    conn = pymysql.connect(host='localhost', user='root', password='new_password', db='cmpe321', charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    c = conn.cursor()

    if request.method == 'POST':
        if request.form["type"] == "AUTHOR":
            c.execute('SELECT * FROM AUTHOR')
            s = (c.fetchall())
            string = ""
            for i in s:
                string += (i["nameSurname"]) + "<br><br><br>"
            string = "<h1>NAMES </h1><br>" + string
            return string + "<br> " + '<br><br> <a href=" / "> Return to home page </a>'

        elif request.form["type"] == "PAPER":
            c.execute('SELECT * FROM PAPER')
            s = (c.fetchall())
            string = "<h1> AUTHORS ------ TITLE ------ ABSTRACT ------ TOPICS ------ RESULT</h1><br>"
            for i in s:
                sql = 'SELECT nameSurname FROM PAPER3 WHERE title=%s'
                c.execute(sql, (i["title"]))
                names = c.fetchall()
                authors = ""
                for k in names:
                    authors += k["nameSurname"] + ", "
                sql = 'SELECT topic FROM PAPER2 WHERE title=%s'
                c.execute(sql, (i["title"]))
                names = c.fetchall()
                topics = ""
                for k in names:
                    topics += k["topic"] + ", "
                authors = authors[:len(authors) - 2]
                topics = topics[:len(topics) - 2]
                string += authors + " ------ " + i["title"] + " ------ " + i[
                    "abstract"] + " ------ " + topics + " ------ " + str(i["result"]) + "<br><br><br> "
            return (string + "<br> " + '<br> <a href=" / "> Return to home page </a>')


        elif request.form["type"] == "TOPIC":
            c.execute("SELECT * FROM SOTA")
            all = c.fetchall()
            string = "<h1> TOPIC NAME ------- SOTA </h1>"
            for i in all:
                string += i["topic"] + " ----- " + str(i["SOTA"]) + "<br><br><br><br>"
            return string + '<br> <a href=" / "> Return to home page </a>'



        elif request.form["type"] == "getAuthorPapers":
            sql = "SELECT PAPER.title,PAPER.abstract,PAPER.result FROM PAPER,PAPER3 WHERE PAPER3.nameSurname=%s AND PAPER.title=PAPER3.title"
            c.execute(sql, (request.form["authorName"]))

            mem = c.fetchall()
            string = 'ALL PAPERS OF ' + request.form["authorName"] + "<br>"
            string += "<h1> AUTHORS ------ TITLE ------ ABSTRACT ------ TOPICS ------ RESULT</h1><br>"
            for i in mem:
                sql = 'SELECT nameSurname FROM PAPER3 WHERE title=%s'
                c.execute(sql, (i["title"]))
                names = c.fetchall()
                authors = ""
                for k in names:
                    authors += k["nameSurname"] + ", "
                sql = 'SELECT topic FROM PAPER2 WHERE title=%s'
                c.execute(sql, (i["title"]))
                names = c.fetchall()
                topics = ""
                for k in names:
                    topics += k["topic"] + ", "
                authors = authors[:len(authors) - 2]
                topics = topics[:len(topics) - 2]
                string += authors + " ------ " + i["title"] + " ------ " + i[
                    "abstract"] + " ------ " + topics + " ------ " + str(i["result"]) + "<br> <br> <br> "
            return (string + "<br> " + '<br> <a href=" / "> Return to home page </a>')

        elif request.form["type"] == "sotaResultByTopic":
            sql = 'select sota.topic,sota.sota,paper2.title from sota,paper,paper2 where paper2.topic=sota.topic and paper.title=paper2.title and paper.result=sota.sota order by sota.sota desc'
            c.execute(sql)

            mem = c.fetchall()

            string = "SOTA RESULT BY TOPIC <br>" + "<h1>TOPIC ----- SOTA  ------------------- IN WHICH PAPER </h1><br>"

            for i in mem:
                string += i["topic"] + " ----- " + str(i["sota"]) + " ------------------- "  # i["title"] + "<br>"

                sql = 'SELECT * FROM PAPER WHERE title=%s'
                c.execute(sql, (i["title"]))
                tit = c.fetchall()
                j = tit[0]
                sql = 'SELECT nameSurname FROM PAPER3 WHERE title=%s'
                c.execute(sql, (i["title"]))
                names = c.fetchall()
                authors = ""
                for k in names:
                    authors += k["nameSurname"] + ", "
                sql = 'SELECT topic FROM PAPER2 WHERE title=%s'
                c.execute(sql, (i["title"]))
                names = c.fetchall()
                topics = ""
                for k in names:
                    topics += k["topic"] + ", "
                authors = authors[:len(authors) - 2]
                topics = topics[:len(topics) - 2]
                string += authors + " ------ " + j["title"] + " ------ " + j[
                    "abstract"] + " ------ " + topics + " ------ " + str(j["result"]) + "<br><br>  "

            return string + '<br> <a href=" / "> Return to home page </a>'



        elif request.form["type"] == "getPapersByTopic":
            sql = "SELECT PAPER.title,PAPER.abstract,PAPER.result FROM PAPER,PAPER2 WHERE PAPER2.topic=%s AND PAPER.title=PAPER2.title"
            c.execute(sql, (request.form["topicName"]))

            mem = c.fetchall()
            string = 'ALL PAPERS BY TOPIC ' + request.form["topicName"] + "<br>"

            string += "<h1> AUTHORS ------ TITLE ------ ABSTRACT ------ TOPICS ------ RESULT</h1><br>"
            for i in mem:
                sql = 'SELECT nameSurname FROM PAPER3 WHERE title=%s'
                c.execute(sql, (i["title"]))
                names = c.fetchall()
                authors = ""
                for k in names:
                    authors += k["nameSurname"] + ", "
                sql = 'SELECT topic FROM PAPER2 WHERE title=%s'
                c.execute(sql, (i["title"]))
                names = c.fetchall()
                topics = ""
                for k in names:
                    topics += k["topic"] + ", "
                authors = authors[:len(authors) - 2]
                topics = topics[:len(topics) - 2]
                string += authors + " ------ " + i["title"] + " ------ " + i[
                    "abstract"] + " ------ " + topics + " ------ " + str(i["result"]) + "<br> <br> <br> "
            return (string + "<br> " + '<br> <a href=" / "> Return to home page </a>')

        elif request.form["type"] == "rankAuthorsBySotaResult":
            string = "AUTHORS RANKED BY SOTA RESULT"
            string += "<h1> SOTA  ----  AUTHOR </h1> <br>"

            sql = "SELECT * FROM AUTHOR"
            c.execute(sql)
            mem = c.fetchall()
            sotasAndAuthors = []
            for i in mem:
                author = i["nameSurname"]

                sql = "SELECT COUNT(PAPER.title) FROM PAPER,PAPER2,PAPER3,SOTA WHERE PAPER3.nameSurname=%s AND PAPER2.title=PAPER3.title AND PAPER2.title=PAPER.title AND PAPER2.topic=SOTA.topic AND PAPER.result=SOTA.SOTA"

                c.execute(sql, (author))
                lel = c.fetchall()
                sotasAndAuthors.append([lel[0]["COUNT(PAPER.title)"], author])

            for i in sorted(sotasAndAuthors):
                string += str(i[0]) + " ----- " + i[1] + "<br>"
            return string + '<br> <a href=" / "> Return to home page </a>'


        elif request.form["type"] == "searchKeyword":
            sql = "SELECT title,abstract,result FROM PAPER WHERE title LIKE %s OR abstract LIKE %s"
            c.execute(sql, ('%' + request.form["keyword"] + '%', '%' + request.form["keyword"] + '%'))

            mem = c.fetchall()
            string = 'ALL PAPERS CONTAINING THE KEYWORD "' + request.form[
                "keyword"] + '" IN THEIR TITLE OR ABSTRACT<br>'
            string += "<h1> AUTHORS ------ TITLE ------ ABSTRACT ------ TOPICS ------ RESULT</h1><br>"
            for i in mem:
                sql = 'SELECT nameSurname FROM PAPER3 WHERE title=%s'
                c.execute(sql, (i["title"]))
                names = c.fetchall()
                authors = ""
                for k in names:
                    authors += k["nameSurname"] + ", "
                sql = 'SELECT topic FROM PAPER2 WHERE title=%s'
                c.execute(sql, (i["title"]))
                names = c.fetchall()
                topics = ""
                for k in names:
                    topics += k["topic"] + ", "
                authors = authors[:len(authors) - 2]
                topics = topics[:len(topics) - 2]
                string += authors + " ------ " + i["title"] + " ------ " + i[
                    "abstract"] + " ------ " + topics + " ------ " + str(i["result"]) + "<br> <br> <br> "
            return (string + "<br> " + '<br> <a href=" / "> Return to home page </a>')

        elif request.form["type"] == "searchCo-authors":
            sql = ("CALL SelectCoAuthors(%s)")
            c.execute(sql, (request.form["authorName"]))
            mem = c.fetchall()
            string = '<h1>CoAuthors Of Author "' + request.form[
                "authorName"] + '"</h1><br>'
            for i in mem:
                string += i["nameSurname"] + "<br><br> <br> "
            return string + '<br> <a href=" / "> Return to home page </a>'

    exit(c, conn)
    return "error"


@app.route('/user')
def user():
    return render_template("user.html")


@app.route('/admin')
def admin():
    return render_template("admin.html")


@app.route('/topic')
def topic():
    return render_template("topic.html")


@app.route('/author')
def author():
    return render_template("author.html")


@app.route('/paper')
def paper():
    return render_template("paper.html")


@app.route('/viewTopic')
def viewTopic():
    conn = sqlite3.connect("tutorial.db")
    c = conn.cursor()
    (c.execute('SELECT topic FROM SOTA'))
    returning = ""
    for i in (c.fetchall()):
        s = ""
        for k in i:
            s += str(k)
            s += " "
        returning += s + "<br>"

    exit(c, conn)
    return returning + '<a href=" / "> Return to home page </a>'


@app.route('/viewAuthor')
def viewAuthor():
    conn = sqlite3.connect("tutorial.db")
    c = conn.cursor()
    (c.execute('SELECT * FROM AUTHOR'))
    returning = ""
    for i in (c.fetchall()):
        s = ""
        for k in i:
            s += str(k)
            s += " "
        returning += s + "<br>"

    exit(c, conn)
    return returning + '<a href=" / "> Return to home page </a>'


@app.route('/viewPaper')
def viewPaper():
    conn = sqlite3.connect("tutorial.db")
    c = conn.cursor()  # JOINS FOR PAPERS
    (c.execute('SELECT PAPER3.nameSurname topic FROM SOTA'))
    returning = ""
    for i in (c.fetchall()):
        s = ""
        for k in i:
            s += str(k)
            s += " "
        returning += s + "<br>"

    exit(c, conn)
    return returning + '<a href=" / "> Return to home page </a>'


if __name__ == '__main__':
    app.run()
