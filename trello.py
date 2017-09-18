import sqlite3
from flask import Flask, redirect, url_for, request, jsonify, abort, make_response, render_template

#: connect to database
conn = sqlite3.connect('C:///data\\test.db')
c = conn.cursor()

trello= Flask(__name__)

#: create lists and cards tables
c.execute('''CREATE TABLE IF NOT EXISTS lists(title TEXT, o INTEGER UNIQUE PRIMARY KEY, id INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS cards(title TEXT, description TEXT, listid INTEGER NOT NULL UNIQUE, id INTEGER PRIMARY KEY)''')

#: route to list URL
@trello.route('/list',methods = ['GET', 'POST'])
def addlist():
  #: pull up addList html, which has input boxes 
  render_template('addList.html') 
  list = {
    'title': request.form['title'],
    'id': 1233+o,
    'o': o
  }
  #: create list
  c.execute("INSERT INTO lists VALUES (title, o, id)")
  #: add list to lists table
  conn.commit()
  conn.close()
  return jsonify({'status code': 200})
  #: return list to screen

#: route to card URL
@trello.route('/card', methods = ['GET', 'POST'])
def addcard():
  #: pull up addcard html, which has input boxes
  render_template('addcard.html')
  card = {
    'title': request.form['title'],
    'listid':request.form['listid'],
    'description':request.form['description'],
    'id': id
  }
  #: create card
  c.execute("INSERT INTO cards VALUES (title, description, listid, id)")
  #: add card to cards table
  conn.commit()
  conn.close()
  return jsonify({'status code': 200})
  #: return card to screen

#: route to card/cardID URL
@trello.route('/card/<int:card_id>', methods = ['GET', 'DELETE'])
def getCard(card_id):
  #: set cursor to cards
  c.execute('''SELECT title, description, listid, id FROM cards''')
  if request.method == 'GET':
    #: see if card_id exists in the table
    for row in c.fetchall():
      #: if it does, return that card
      if row[3] == card_id:
        return jsonify({'status code': 200, 'card': {'title': row[0], 'description': row[1], 'listid': row[2], 'id': row[3]}})
    #: otherwise, return error
    return make_response(jsonify({'error': 'Not found'}), 404)
  else:
    for row in c.fetchall():
      if row[3] == card_id:
        #: delete that card from the table
        c.execute('''DELETE FROM cards WHERE id = ?''', (card_id))
        conn.commit()
        conn.close()
        return jsonify({'card': {'status code': 200, 'title': row[0], 'description': row[1], 'listid': row[2], 'id': row[3]}})
    return make_response(jsonify({'error': 'Not found'}), 404) 

#: route to list/listID URL
@trello.route('/list/<int:list_id>', methods = ['GET', 'DELETE'])
def getList(list_id):
  #: set cursor to lists
  c.execute('''SELECT title, order, id FROM lists''')
  if request.method == 'GET':
    #: see if list_id exists in the table
    for row in c.fetchall():
      #: if it does, return that list
      if row[2] == list_id:
        return jsonify({'status code': 200, 'list': {'title': row[0], 'order': row[1], 'id': row[2]}})
    #: otherwise, return error
    return make_response(jsonify({'error': 'Not found'}), 404)
  else:
    for row in c.fetchall():
      if row[2] == list_id:
        #: delete that row from the table
        c.execute('''DELETE FROM lists WHERE id = ?''', (list_id))
        #: delete all cards that belong to this list
        c.execute('''SELECT title, description, listid, id FROM cards''')
        for row in c.fetchall():
          if row[2] == list_id:
            c.execute('''DELETE FROM cards WHERE listid = ?''', (list_id))
        conn.commit()
        conn.close()
        return jsonify({'status code: 200'})
    return make_response(jsonify({'error': 'Not found'}), 404) 

#: route to editlist/listID URL
@trello.route('/editlist/<int:list_id>', methods = ['GET', 'POST'])
def editList(list_id):
  #: pull up editlist html template
  render_template('editlist.html')
  #: get title and new order
  title = request.form['newtitle']
  neworder = request.form['order']
  #: see if list_id exists in the table
  for row in c.fetchall():
      #: if it does, update and return that list
      if row[2] == list_id:
        #: update lists table
        c.execute('''UPDATE lists SET order = ? WHERE title = ?''', (neworder, title))
        conn.commit()
        return jsonify({'status code': 200, 'list': {'title': row[0], 'order': row[1], 'id': row[2]}})
  #: otherwise, return error
  return make_response(jsonify({'error': 'Not found'}), 404)

if __name__=='__main__':
    trello.run(debug = True)
