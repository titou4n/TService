from Data.database_handler import DatabaseHandler
import os
from os import getenv
from hashlib_blake2b import hashlib_blake2b
from flask import (Flask, flash, render_template, request, session, redirect, url_for)
import requests
from flask_session import Session
import datetime
from ipv4_address import ipv4_address

database_handler=DatabaseHandler()

app = Flask(__name__)
app.secret_key= os.getenv("COOKIES_KEYS")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def not_connected():
    if "id" in session:
        id=session["id"]
        database_handler.date_connected(id,datetime.datetime.now(),ipv4_address())
        return render_template('home_connected.html',id = id, name=database_handler.name_db(id), pay=database_handler.pay_db(id))
    else:
        return render_template('not_connected.html',number_account=database_handler.number_account())

@app.route('/conditions_uses/')
def conditions_uses():
    return render_template('conditions_uses.html')


@app.route('/api/')
def api():
    if "id" in session:
        return render_template('api.html')
    else:
        return render_template('/')

#https://api.nasa.gov/planetary/apod?api_key=dXKQTIoz5WmceiaZoIptVaRhCdQdAhYrfOwbe3qU
#api nasa

#https://www.data.gouv.fr/fr/datasets/repertoire-national-des-associations/

@app.route('/search_movie/', methods=('GET', 'POST'))
def search_movie(movie_title=""):
    if "id" in session:
        id = session["id"]
        if request.method == 'POST':
            movie = request.form['movie']
            if not movie or movie == None:
                flash('Movie is required.')
                return render_template('search_movie.html')
            else:
                key = "1509a239"
                requestURL = "http://www.omdbapi.com/?apikey=" + key + "&t=" + movie
                r = requests.get(requestURL)
                infosMovie = r.json()
                if infosMovie["Response"] == "False":
                    infos_movie_error = infosMovie["Error"]
                    flash('"{}"'.format(infos_movie_error))
                    return render_template('search_movie.html')
                else:
                    movie_title     = infosMovie["Title"]
                    database_handler.insert_movie_search(id, movie_title, datetime.datetime.now())
                    return render_template('infosmovie.html',   movie_title     = movie_title,
                                                                movie_year      = infosMovie["Year"],
                                                                movie_released  = infosMovie["Released"],
                                                                movie_runtime   = infosMovie["Runtime"],
                                                                movie_genre     = infosMovie["Genre"],
                                                                movie_director  = infosMovie["Director"],
                                                                movie_plot      = infosMovie["Plot"],
                                                                movie_poster    = infosMovie["Poster"],
                                                                movie_rating    = infosMovie["imdbRating"],
                                                                )
        else:
            return render_template("search_movie.html", all_movie_search=database_handler.all_movie_search(id))
    else:
        return redirect("/")

@app.route('/register/', methods=('GET', 'POST'))
def register():
    if "id" in session:
        id = session["id"]
        return render_template('home_connected.html',id = id, name=database_handler.name_db(id), pay=database_handler.pay_db(id))
    else:
        if request.method == 'POST':
            username        = request.form['username']
            password        = request.form['password']
            verif_password  = request.form['verif_password']
            name            = request.form['name'].capitalize()
            if not username or username == None:
                flash('Username is required.')
                return render_template('register.html')
            if not password or password == None:
                flash('Password is required.')
                return render_template('register.html')
            if not verif_password or verif_password == None:
                flash('Verif Password is required.')
                return render_template('register.html')
            if not name or name == None:
                flash('Name is required.')
                return render_template('register.html')
            if request.form.get('contitions_uses')==None:
                flash('Please accept the terms and conditions of use')
                return render_template('register.html')
            else:
                if database_handler.user_exists_with(username):
                    flash("Username is already used.")
                    return render_template('register.html')
                else:
                    if database_handler.name_exists_with(name):
                        flash("Name is already used.")
                        return render_template('register.html')
                    else:
                        password=hashlib_blake2b(password)
                        verif_password=hashlib_blake2b(verif_password)
                        if password == verif_password:
                            database_handler.create_account(username, password, name)
                            id = database_handler.id_db(username)
                            session["id"]=id
                            database_handler.date_connected(id,datetime.datetime.now(),ipv4_address())
                            return render_template('home_connected.html',id = id, name=database_handler.name_db(id), pay=database_handler.pay_db(id))
                        else:
                            flash('Passwords must be identical.')
                            return render_template('register.html')
        else:
            return render_template('register.html')
            
@app.route('/login/', methods=('GET', 'POST'))
def login():
    if "id" in session:
            id = session["id"]
            return render_template('home_connected.html',id = id, name=database_handler.name_db(id), pay=database_handler.pay_db(id))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = hashlib_blake2b(request.form['password'])
            if not username or username == None:
                flash('Username is required.')
                return render_template('login.html')
            if not password or password == None:
                flash('Password is required.')
                return render_template('login.html')
            else:
                if database_handler.user_exists_with(username):
                    id = database_handler.id_db(username)
                    session["id"]=id
                    if password == database_handler.password_db(id) :
                        database_handler.date_connected(id,datetime.datetime.now(),ipv4_address())
                        return render_template('home_connected.html',id = id, name=database_handler.name_db(id), pay=database_handler.pay_db(id))
                    else:
                        flash('Password is not correct.')
                        return render_template('login.html')
                else:
                    flash('Username is not correct.')
                    return render_template('login.html')
        else:
            return render_template('login.html')

@app.route('/home_connected/', methods=('GET', 'POST'))
def home_connected():
    if "id" in session:
        id=session["id"]
        if request.method == 'POST':
                return render_template('home_connected.html',name=database_handler.name_db(id))
        else:
            return render_template('home_connected.html', name=database_handler.name_db(id))
    else:
        return redirect("/")

@app.route('/titoubank/', methods=('GET', 'POST'))
def titoubank():
    if "id" in session:
        id=session["id"]
        return render_template('titoubank.html', pay=database_handler.pay_db(id))
    else:
        return redirect("/")

@app.route('/thank_you/', methods=('GET', 'POST'))
def thank_you():
    return render_template('thank_you.html')

@app.route('/personal_information/', methods=('GET', 'POST'))
def personal_information():
    if "id" in session:
        id=session["id"]
        return render_template('personal_information.html', id=id, name=database_handler.name_db(id), pay=database_handler.pay_db(id))
    else:
        return redirect("/")

@app.route('/delete_account/', methods=('GET', 'POST'))
def delete_account():
    if "id" in session:
        id=session["id"]
        if request.method == 'POST':
            database_handler.delete_account(id)
            session["id"] = None
            session.pop("id", None)
            session.clear()
            flash('Your account was successfully deleted!')
            return redirect("/")
        else:
            return render_template('personal_information.html', id=id, name=database_handler.name_db(id), pay=database_handler.pay_db(id))
    else:
        return redirect("/")

@app.route('/change_password/', methods=('GET', 'POST'))
def change_password():
    if "id" in session:
        id=session["id"]
        if request.method == 'POST':
            new_password       = hashlib_blake2b(request.form['new_password'])
            verif_new_password = hashlib_blake2b(request.form['verif_new_password'])
            if not new_password or new_password == None:
                flash('New password is required !')
            if not verif_new_password or verif_new_password == None:
                flash('Verif New password is required !')
            else:
                if new_password == verif_new_password:
                    database_handler.change_password(id, new_password)
                    flash('Your password has been updated')
                    return render_template('personal_information.html', id=id, name=database_handler.name_db(id), pay=database_handler.pay_db(id))
                else:
                    flash('Les Passwords sont differents')
                    return render_template('change_password.html', id=id)
        else:
            return render_template('change_password.html', id=id)
       
    else:
        return render_template('/')
    
@app.route('/change_name/', methods=('GET', 'POST'))
def change_name():
    if "id" in session:
        id=session["id"]
        if request.method == 'POST':
            new_name = request.form['new_name'].capitalize()
            if not new_name or new_name == None:
                flash('Name is required !')
            else:
                database_handler.change_name(id, new_name)
                database_handler.change_name_in_post(id, new_name)
                flash('Your name has been updated')
                return render_template('personal_information.html', id=id, name=database_handler.name_db(id), pay=database_handler.pay_db(id))
        else:
            return render_template('change_name.html', id=id, name=database_handler.name_db(id))
    else:
        return render_template('/')
    
@app.route("/withdrawl/", methods=('GET', 'POST'))
def withdrawl():
    if "id" in session:
        id=session["id"]
        if request.method == 'POST':
            withdrawl = int(request.form['withdrawl'])
            print(withdrawl)
            if withdrawl < 0:
                flash("un retrait nul ou négatif est impossible j'ai deja essayé")
            else:
                pay = database_handler.pay_db(id)
                new_pay= pay - withdrawl
                database_handler.new_pay_db(id, new_pay)
                return render_template('home_connected.html', id=id, name=database_handler.name_db(id), pay=database_handler.pay_db(id))
        else:
            return render_template('withdrawl.html', id=id)
    else:
        return redirect("/")

@app.route('/chatroom/', methods=('GET', 'POST'))
def chatroom():
    if "id" in session:
        id = session["id"]
        return render_template('chatroom.html',id=id, posts=database_handler.post_in_chatroom())
    else:
        return redirect("/")

@app.route('/create_post/', methods=('GET', 'POST'))
def create_post():
    if "id" in session:
        id = session["id"]
        if request.method == 'POST':
            id = session["id"]
            #name = request.form['name']
            name=database_handler.name_db(id)
            title = request.form['title']
            content = request.form['content']
            if not name:
                flash('Name is required!, You thought life was chicken?')
            if not title:
                flash('Title is required!, You thought life was chicken?')
            elif not content:
                flash('Content is required!, You thought life was chicken?')
            else:
                database_handler.create_post(id, name, title, content)
                return render_template('chatroom.html',id = id, posts = database_handler.post_in_chatroom())
        else:
            return render_template('create_post.html', id=id)
    else:
        return redirect("/")

@app.route('/edit_post/<int:id_post>/', methods=('GET', 'POST'))
def edit_post(id_post):
    if "id" in session:
        id=session["id"]
        if request.method == 'POST':
            #name  = request.form['name']
            name = database_handler.name_db(id)
            title = request.form['title']
            content = request.form['content']
            if not name:
                flash('Name is required!, You thought life was chicken?')
            if not title:
                flash('Title is required!, You thought life was chicken?')
            elif not content:
                flash('Content is required!, You thought life was chicken?')
            else:
                database_handler.edit_post(id_post, name, title, content)
                return render_template('chatroom.html',id=id, posts = database_handler.post_in_chatroom())
        else:
            return render_template('edit_post.html',id=id, post=database_handler.get_post(id_post))
    else:
        return redirect("/")

@app.route('/delete/<int:id_post>/', methods=('POST',))
def delete_post(id_post):
    if "id" in session:
        id=session["id"]
        if request.method == 'POST':
            post = database_handler.get_post(id_post)
            database_handler.delete_post(id_post)
            flash('"{}" was successfully deleted!'.format(post['title']))
            return render_template('chatroom.html',id=id, posts = database_handler.post_in_chatroom())
        else:
            return render_template('edit_post.html',id=id, post=database_handler.get_post(id_post))
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    if "id" in session:
        #session["id"] = None
        session.pop("id", None)
        session.clear()
        return render_template('not_connected.html',number_account=database_handler.number_account())

if __name__ == "__main__":
    app.run(debug=True)