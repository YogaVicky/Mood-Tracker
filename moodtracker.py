from flask import Flask, render_template, request, jsonify, flash, redirect, session
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms.fields import DateField
import os
import random
from pymysql import connect
from datetime import datetime , date , timedelta
import json
import calendar
app = Flask(__name__)

def get_lcl(sql):
    result = []
    db = connect(host='localhost', database='test', user='root', password='1234')
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    for i in cursor.fetchall():
        result.append(i)
    cursor.close()
    return result

def get_lcl2(sql):
    result = []
    db = connect(host='localhost', database='test', user='root', password='1234')
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)

@app.route('/')
@app.route('/dailystat')
def dailystat():
    datenow = (datetime.now().strftime("%Y-%m-%d"))
    print(datenow)
    sql = "SELECT * from mood_tracker WHERE date = '{0}'".format(datenow)
    # sql = "SELECT * from mood_tracker"
    data = get_lcl(sql)
    print(data)
    return render_template('dailytrack.html' , data = data)

@app.route('/weekstat')
def weekstat():
    datenow = (datetime.now().strftime("%Y-%m-%d"))
    print(datenow)
    newdate = (datetime.strptime(datenow, "%Y-%m-%d") + timedelta(days=-7)).strftime("%Y-%m-%d")
    print(newdate)
    sql = "SELECT * from mood_tracker WHERE date = '{0}'".format(datenow)
    # sql = "SELECT * from mood_tracker"
    data = get_lcl(sql)
    data2 = []
    for i in range(7):
        sql = "SELECT * from mood_tracker WHERE date BETWEEN '{1}' AND '{0}'".format((datetime.strptime(datenow, "%Y-%m-%d") + timedelta(days=-1-i)),(datetime.strptime(datenow, "%Y-%m-%d") + timedelta(days=-2-i)))
        print(sql)
        data1 = get_lcl(sql)
        print(data1)
        data2.append(data1)
    print(data2)

    week = [[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0]]
    for i in range(7):
        for artist in data2[i]:
            if artist[3] == 1:
                week[0][i] = week[0][i] + 1
            if artist[5] == 1:
                week[0][i] = week[0][i] + 1
            if artist[7] == 1:
                week[0][i] = week[0][i] + 1
            if artist[3] == 2:
                week[1][i] = week[1][i] + 1
            if artist[5] == 2:
                week[1][i] = week[1][i] + 1
            if artist[7] == 2:
                week[1][i] = week[1][i] + 1
            if artist[3] == 3:
                week[2][i] = week[2][i] + 1
            if artist[5] == 3:
                week[2][i] = week[2][i] + 1
            if artist[7] == 3:
                week[2][i] = week[2][i] + 1
            print(week)
    print(week)
    my_date = date.today()  + timedelta(days=-1)
    print(my_date)
    j = 0
    my_day = calendar.day_name[my_date.weekday()]
    days = {1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5: 'Friday', 6: 'Saturday', 7 :'Sunday'}
    for i in range(7):
        if my_day == days[i+1]:
            j = i+1
    print(j)
    weekday = []
    for i in range(j,7):
        weekday.append(days[i+1])
    for i in range(0,j):
        weekday.append(days[i+1])
    print(weekday)
    print(type(weekday[0]))
    week[0].reverse()
    week[1].reverse()
    week[2].reverse()
    return render_template('weeklytrack.html' , data = data , week = week , weekday = weekday)

@app.route('/monthstat', methods=['GET', 'POST'])
def monthstat():
    n = 4
    if request.method == 'POST':
        start = request.form.get('weekpick')
        n = int(start)
        print(n)
        print(type(n))
    datenow = (datetime.now().strftime("%Y-%m-%d"))
    print(datenow)
    newdate = [datenow,0,0,0,0,0,0,0,0,0,0]
    for i in range(n):
        newdate[i+1] = (datetime.strptime(newdate[i], "%Y-%m-%d") + timedelta(days=-7)).strftime("%Y-%m-%d")
    print(newdate)
    week = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for i in range(n):
        sql = "SELECT * from mood_tracker WHERE date BETWEEN '{1}' AND '{0}'".format((datetime.strptime(newdate[i], "%Y-%m-%d") + timedelta(days=-1)).strftime("%Y-%m-%d"),newdate[i+1])
        print(sql)
        data = get_lcl(sql)
        print(data)
        for artist in data:
            if artist[3] == 1:
                week[0][i] = week[0][i] + 1
            if artist[5] == 1:
                week[0][i] = week[0][i] + 1
            if artist[7] == 1:
                week[0][i] = week[0][i] + 1
            if artist[3] == 2:
                week[1][i] = week[1][i] + 1
            if artist[5] == 2:
                week[1][i] = week[1][i] + 1
            if artist[7] == 2:
                week[1][i] = week[1][i] + 1
            if artist[3] == 3:
                week[2][i] = week[2][i] + 1
            if artist[5] == 3:
                week[2][i] = week[2][i] + 1
            if artist[7] == 3:
                week[2][i] = week[2][i] + 1
            print(week)
    print(week)
    datenow = (datetime.now().strftime("%Y-%m-%d"))
    print(datenow)
    sql = "SELECT * from mood_tracker WHERE date = '{0}'".format(datenow)
    # sql = "SELECT * from mood_tracker"
    data = get_lcl(sql)
    return render_template('monthlytrack.html' , data = data ,week = week , n = n)

@app.route('/yearstat', methods=['GET', 'POST'])
def yearstat():
    yearnow = (datetime.now().strftime("%Y"))
    print(type(yearnow))
    print(yearnow)
    if request.method == 'POST':
        start = request.form.get('monthpick')
        n = int(start)
        yearnow = n
        print(n)
        print(type(n))
    month = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    sql = "SELECT * from mood_tracker WHERE date LIKE '{0}%'".format(yearnow)
    data = get_lcl(sql)
    print(len(data))
    sObject = slice(5, 7)
    for i in range(len(data)):
        m = int(data[i][2][sObject])
        print(m)
        if data[i][3] == 1:
            month[0][m-1] = month[0][m-1] +1
        if data[i][5] == 1:
            month[0][m - 1] = month[0][m - 1] + 1
        if data[i][7] == 1:
            month[0][m-1] = month[0][m-1] +1
        if data[i][3] == 2:
            month[1][m-1] = month[1][m-1] +1
        if data[i][5] == 2:
            month[1][m-1] = month[1][m-1] +1
        if data[i][7] == 2:
            month[1][m-1] = month[1][m-1] +1
        if data[i][3] == 3:
            month[2][m-1] = month[2][m-1] +1
        if data[i][5] == 3:
            month[2][m-1] = month[2][m-1] +1
        if data[i][7] == 3:
            month[2][m-1] = month[2][m-1] +1
    print(month)
    datenow = (datetime.now().strftime("%Y-%m-%d"))
    print(datenow)
    sql = "SELECT * from mood_tracker WHERE date = '{0}'".format(datenow)
    data = get_lcl(sql)
    print(data)
    return render_template('yearlytrack.html' , data = data , month = month)

if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=True)
