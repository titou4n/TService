from Data.database_handler import DatabaseHandler
import os
from hashlib_blake2b import hashlib_blake2b
from flask import (Flask, flash, render_template, request, session, redirect, url_for)
import requests
from flask_session import Session
import datetime
from ipv4_address import ipv4_address

database_handler=DatabaseHandler()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.secret_key= os.getenv("COOKIES_KEYS")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    if "id" in session:
        id=session["id"]
        database_handler.insert_metadata(id,datetime.datetime.now(),ipv4_address())
        return render_template('dashboard.html',id = id, name=database_handler.get_name(id), pay=database_handler.get_pay(id))
    else:
        return render_template('index.html',number_account=database_handler.get_number_account())

@app.route('/conditions_uses/')
def conditions_uses():
    return render_template('conditions_uses.html')

@app.route('/register/', methods=('GET', 'POST'))
def register():
    if "id" in session:
        id = session["id"]
        return render_template('dashboard.html',id = id, name=database_handler.get_name(id), pay=database_handler.get_pay(id))
    else:
        if request.method == 'POST':
            username        = request.form['username']
            password        = hashlib_blake2b(request.form['password'])
            verif_password  = hashlib_blake2b(request.form['verif_password'])
            name            = request.form['name'].capitalize()
            if database_handler.verif_user_exists(username):
                flash("Username is already used.")
                return render_template('register.html')
            else:
                if database_handler.verif_name_exists(name):
                    flash("Name is already used.")
                    return render_template('register.html')
                else:
                    if password == verif_password:
                        database_handler.create_account(username, password, name)
                        id = database_handler.get_id(username)
                        session["id"]=id
                        database_handler.insert_metadata(id,datetime.datetime.now(),ipv4_address())
                        return render_template('dashboard.html',id = id, name=database_handler.get_name(id), pay=database_handler.get_pay(id))
                    else:
                        flash("Passwords must be identical.")
                        return render_template('register.html')
        else:
            return render_template('register.html')
            
@app.route('/login/', methods=('GET', 'POST'))
def login():
    if "id" in session:
            id = session["id"]
            return render_template('dashboard.html',id = id, name=database_handler.get_name(id), pay=database_handler.get_pay(id))
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
                if database_handler.verif_user_exists(username):
                    id = database_handler.get_id(username)
                    session["id"]=id
                    if password == database_handler.get_password(id) :
                        database_handler.insert_metadata(id,datetime.datetime.now(),ipv4_address())
                        return render_template('dashboard.html',id = id, name=database_handler.get_name(id), pay=database_handler.get_pay(id))
                    else:
                        flash('Password is not correct.')
                        return render_template('login.html')
                else:
                    flash('Username is not correct.')
                    return render_template('login.html')
        else:
            return render_template('login.html')

@app.route('/dashboard/', methods=('GET', 'POST'))
def dashboard():
    if "id" in session:
        id=session["id"]
        if request.method == 'POST':
                return render_template('dashboard.html',name=database_handler.get_name(id))
        else:
            return render_template('dashboard.html', name=database_handler.get_name(id))
    else:
        return redirect("/")

@app.route('/personal_information/', methods=('GET', 'POST'))
def personal_information():
    if "id" in session:
        id=session["id"]
        return render_template('personal_information.html', id=id, name=database_handler.get_name(id), pay=database_handler.get_pay(id))
    else:
        return redirect("/")

@app.route('/change_password/', methods=('GET', 'POST'))
def change_password():
    if "id" in session:
        id=session["id"]
        if request.method == 'POST':
            actual_password    = hashlib_blake2b(request.form['actual_password'])
            new_password       = hashlib_blake2b(request.form['new_password'])
            verif_new_password = hashlib_blake2b(request.form['verif_new_password'])
            if actual_password  == database_handler.get_password(id):
                if new_password == verif_new_password:
                    database_handler.update_password(id, new_password)
                    flash('Your password has been updated')
                    return render_template('personal_information.html', id=id, name=database_handler.get_name(id), pay=database_handler.get_pay(id))
                else:
                    flash("Passwords must be identical.")
                    return render_template('change_password.html', id=id)
            else:
                flash('Password is not correct.')
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
            new_name = request.form['new_name']
            if not new_name:
                flash('Name is required !')
            else:
                database_handler.update_name(id, new_name.capitalize())
                database_handler.update_name_in_post(id, new_name.capitalize())
                flash('Your name has been updated')
                return render_template('personal_information.html', id=id, name=database_handler.get_name(id), pay=database_handler.get_pay(id))
        else:
            return render_template('change_name.html', id=id, name=database_handler.get_name(id))
    else:
        return render_template('/')

@app.route('/delete_account/', methods=('GET', 'POST'))
def delete_account():
    if "id" in session:
        id=session["id"]
        if request.method == 'POST':
            database_handler.delete_all_post_from_id(id)
            database_handler.delete_account(id)
            session["id"] = None
            session.pop("id", None)
            session.clear()
            flash('Your account was successfully deleted!')
            return redirect("/")
        else:
            return render_template('personal_information.html', id=id, name=database_handler.get_name(id), pay=database_handler.get_pay(id))
    else:
        return redirect("/")

@app.route('/chatroom/', methods=('GET', 'POST'))
def chatroom():
    if "id" in session:
        id = session["id"]
        return render_template('chatroom.html',id=id, posts=database_handler.get_posts())
    else:
        return redirect("/")

@app.route('/create_post/', methods=('GET', 'POST'))
def create_post():
    if "id" in session:
        id = session["id"]
        if request.method == 'POST':
            id = session["id"]
            title = request.form['title']
            content = request.form['content']
            if not title or not content:
                flash('Error: Title and Content is required')
                return render_template('create_post.html', id=id)
            else:
                name=database_handler.get_name(id)
                database_handler.create_post(id, name, title, content)
                return render_template('chatroom.html',id = id, posts = database_handler.get_posts())
        else:
            return render_template('create_post.html', id=id)
    else:
        return redirect("/")

@app.route('/edit_post/<int:id_post>/', methods=('GET', 'POST'))
def edit_post(id_post):
    if "id" in session:
        id=session["id"]
        if id == database_handler.get_id_from_id_post(id_post):
            if request.method == 'POST':
                title = request.form['title']
                content = request.form['content']
                if not title or not content:
                    flash('Error: Title and Content is required')
                    return render_template('create_post.html', id=id)
                else:
                    name = database_handler.get_name(id)
                    database_handler.update_post(id_post, name, title, content)
                    return render_template('chatroom.html',id=id, posts = database_handler.get_posts())
            else:
                return render_template('edit_post.html',id=id, post=database_handler.get_post_from_id(id_post))
        else:
            flash("You cannot edit this post.")
            return render_template('chatroom.html',id=id, posts = database_handler.get_posts())
    else:
        return redirect("/")

@app.route('/delete/<int:id_post>/', methods=('POST',))
def delete_post(id_post):
    if "id" in session:
        id=session["id"]
        if request.method == 'POST':
            post = database_handler.get_post_from_id(id_post)
            database_handler.delete_post(id_post)
            flash('"{}" was successfully deleted!'.format(post['title']))
            return render_template('chatroom.html',id=id, posts = database_handler.get_posts())
        else:
            return render_template('edit_post.html',id=id, post=database_handler.get_post(id_post))
    else:
        return redirect("/")

@app.route('/titoubank/', methods=('GET', 'POST'))
def titoubank():
    if "id" in session:
        id=session["id"]
        return render_template('titoubank.html', pay=database_handler.get_pay(id))
    else:
        return redirect("/")

@app.route("/withdrawl/", methods=('GET', 'POST'))
def withdrawl():
    if "id" in session:
        id=session["id"]
        if request.method == 'POST':
            withdrawl = int(request.form['withdrawl'])
            if withdrawl <= 0:
                flash("Zero or negative withdrawal is impossible.")
                return render_template('withdrawl.html', id=id)
            else:
                pay = database_handler.get_pay(id)
                if pay - withdrawl < 0:
                    flash("Your Balance is not high enough.")
                    return render_template('withdrawl.html', id=id)
                else:
                    new_pay= pay - withdrawl
                    database_handler.update_pay(id, new_pay)
                    flash('"{}" TC have been withdrawn from your account.'.format(withdrawl))
                    return render_template('withdrawl.html', id=id)
        else:
            return render_template('withdrawl.html', id=id)
    else:
        return redirect("/")

@app.route('/api/')
def api():
    if "id" in session:
        return render_template('api.html')
    else:
        return render_template('/')

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
            return render_template("search_movie.html", all_movie_search=database_handler.get_movie_search(id))
    else:
        return redirect("/")

@app.route('/thank_you/', methods=('GET', 'POST'))
def thank_you():
    return render_template('thank_you.html')

@app.route("/logout")
def logout():
    if "id" in session:
        session.pop("id", None)
        session.clear()
        return render_template('index.html',number_account=database_handler.get_number_account())

if __name__ == "__main__":
    app.run(debug=True)