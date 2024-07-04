from openDAO import openDAO

from flask import Flask, url_for, request, redirect, abort, jsonify, render_template, session
from markupsafe import escape
#from flask_cors import CORS
app = Flask(__name__, static_url_path='', static_folder='staticpages')

# map username to user data
users = {"admin":("admin","1234")}

@app.route('/')
def index():
    if 'username' in session:
         return 'Logged in as %s' % escape(session['username']) +\
            '<br><a href="'+'/home.html'+'">home</a>' +\
             '<br><a href="'+url_for('admin')+'">Admin</a>'

    return 'Welcome to the application. <br/> You are not logged in <br/>' +\
        'You can search for datasets, publishers of datasets on the Irish open data portal using the links at the top of the home page.<br/>' +\
        '' +\
        '<br><a href="'+'/home.html'+'">home</a>'
        
        
@app.route('/admin', methods = ['GET'])
def adminOnly():
    if 'username' in session:
        return render_template("/admin.html")
    elif not 'username' in session:
        return redirect(url_for('login'))
    
@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username][1] == password:
            session['username'] = username
            return redirect(url_for('admin'))
        return render_template("/login.html")
    
@app.route('/logout')
def logout():
    session.pop('counter', None)
    return 'done'

@app.route('/packages_load', methods = ['GET'])
def loadPackages():
    if not 'username' in session:
        return redirect(url_for('login'))
    elif 'username' in session:
        openDAO.truncateDatasetsTable()
        openDAO.loadDatasetsTable()
        return "The dataset_list table has been loaded from Irish Open data portal " +\
        '<br><a href="'+url_for('logout')+'">logout</a>' +\
        '<br><a href="/home.html">home</a>'
        
@app.route('/tags_load', methods=['GET'])
def loadTags():
    if not 'username' in session:
        return redirect(url_for('login'))
    elif 'username' in session:
        openDAO.truncateTagsTable()
        openDAO.loadTagsTable()
        return "The tag_list table has been loaded from Irish Open data portal " +\
        '<br><a href="'+url_for('logout')+'">logout</a>' +\
        '<br><a href="/home.html">home</a>'
        
@app.route('/orgs_load', methods=['GET'])
def loadOrgs():
    if 'username' in session:
    # clear table if already populated so it is not duplicated
        openDAO.truncateOrgsTable()
        openDAO.loadOrgsTable()
        return "The org_list table has been loaded from Irish Open data portal " +\
        '<br><a href="'+url_for('logout')+'">logout</a>' +\
        '<br><a href="/home.html">home</a>'

    elif not 'username' in session:
        #abort(401)
        return redirect(url_for('login'))
    
@app.route('/tags', methods=['GET'])
def getAllTags():
    results = dataDOA.getAllTags()
    return jsonify(results)
    