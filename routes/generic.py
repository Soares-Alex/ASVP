# import des methodes necessaires
from flask import render_template, url_for, request, flash, redirect

from asvp.app import app, login, db

# import des tables de la base de donnees
from asvp.modeles.all_data import Statistique
from asvp.modeles.all_user import User
#import login menager
from flask_login import login_user, current_user, logout_user, login_required
#row per pages
ROWS_PER_PAGE= 10


#home
@app.route("/")
@app.route("/index")
def index():
    """" Route permettant d'afficher la page d'accueil
       """

    page=request.args.get('page', 1,type=int)
    all_data = Statistique.query.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template("pages/index.html", new_data=all_data, nom="asvp")

### session categorie index ###
@app.route("/index_femmes/")
def index_femmes():

    woman = Statistique.query.filter_by(categorie="Femmes")

    return render_template("pages/index_femmes.html", woman=woman)


@app.route("/index_hommes/")
def index_hommes():

    men = Statistique.query.filter_by(categorie="Hommes")

    return render_template("pages/index_hommes.html", men=men)

@app.route("/index_enfants/")
def index_enfants():

    kids = Statistique.query.filter_by(categorie="Enfants")

    return render_template("pages/index_enfant.html", kids=kids)


@app.route("/index_militaires/")
def index_militaires():

    military = Statistique.query.filter_by(categorie="Militaires")

    return render_template("pages/index_militaire.html", military=military)


@app.route("/index_lycees/")
def index_lycees():
    student = Statistique.query.filter_by(categorie="Lycées, sociétés postscolaires et patronages")

    return render_template("pages/index_lycee.html", student=student )


@app.route("/index_societes/")
def index_societes():
    sport = Statistique.query.filter_by(categorie="Sociétés sportives")

    return render_template("pages/index_sportives.html", sport=sport)


@app.route("/index_totaux/")
def index_totaux():
    total = Statistique.query.filter_by(categorie="Totaux")

    return render_template("pages/index_totaux.html", total=total)

### session annee index ###
@app.route("/index_1935/")
def index_1935():
    index_35 = Statistique.query.filter_by(annee="1935")

    return render_template("pages/index_1935.html", index_35=index_35)

@app.route("/index_1936/")
def index_1936():
    index_36 = Statistique.query.filter_by(annee="1936")

    return render_template("pages/index_1936.html", index_36=index_36)


@app.route("/index_1937/")
def index_1937():
    index_37 = Statistique.query.filter_by(annee="1937")

    return render_template("pages/index_1937.html", index_37=index_37)


### session a propos de l'app ###

@app.route("/about_app")
def about_app():

    return render_template("partials/metadata.html")

###one data insert equal one data line
@app.route("/line/<int:statistique_id>")
def line(statistique_id):

    unique_line = Statistique.query.get(statistique_id)
    return render_template("pages/data.html", nom="ASVP", line=unique_line)

@app.route("/search" , methods =['GET'])
def search():
    # Method "get"
    #  we use [] to avoid a big list of "if"
    word_key = request.args.get("keyword", None)
    # we create a variable empty
    #   is there are not key_word
    outcome = []
    # as we search only by categories, nothing more is needed
    if word_key:
        #if the keyword searched is presented in our database
        outcome = Statistique.query.filter(
            Statistique.categorie.like("%{}%".format(word_key))).all()

    return render_template("pages/search.html", outcome=outcome)


#this route is for inserting data to database via html forms
@app.route('/insert', methods = ['POST', 'GET'])
@login_required
def insert():

    if request.method == 'POST':

        categorie = request.form.get("categorie", None)
        entree = request.form.get("entree", None)
        annee = request.form.get("annee", None)
        mois = request.form.get("mois", None)
        totaux = request.form.get("totaux", None)
        description = request.form.get("description", None)

        new_statistique = Statistique( categorie=request.form['categorie'], entree=request.form['entree'], annee=request.form['annee'], mois=request.form['mois'], totaux=request.form['totaux'], description=request.form['description'])
        db.session.add(new_statistique)
        db.session.commit()

        flash("Data Inserted Successfully")

        return redirect(url_for('index'))

#this is our update route where we can update to update our information
@app.route("/update/", methods = ['GET', 'POST'])
@login_required
def update():

    if request.method == 'POST':

        new_statistique = Statistique.query.get(request.form.get('statistique_id'))

        new_statistique.categorie = request.form['categorie']
        new_statistique.entree = request.form['entree']
        new_statistique.annee = request.form['annee']
        new_statistique.mois = request.form['mois']
        new_statistique.totaux = request.form['totaux']
        new_statistique.description = request.form['description']

        db.session.commit()
        flash("Data Updated Successfully")

        return redirect(url_for('index'))

#This route is for deleting our imformation
@app.route('/delete/<int:statistique_id>', methods = ['GET', 'POST'])
@login_required
def delete(statistique_id):


    new_statistique = Statistique.query.get(statistique_id)
    db.session.delete(new_statistique)
    db.session.commit()
    flash("Data Deleted Successfully")

    return redirect(url_for('index'))


@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    """ Route pour gérer les connexions
       :return: On renvoie à la page d'accueil si la connexion est déjà faite,
       on y renvoie également si les informations rentrées sont correctes et sinon,
       on renvoie à la page connexion pour réessayer.
       """
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )

        if statut is True:
            flash("Well done! you are part of the group", )
            return redirect("/")
        else:
            flash("Ops! Sorry, we faced a problem! : " + ",".join(donnees), "error")
            return render_template("pages/join.html")
    else:
        return render_template("pages/join.html")

@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    # we verify if the user's name and password is true
    if current_user.is_authenticated is True:
        flash("You are connected.", "info")
        return redirect("/")

    if request.method == "POST":
        user = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            # if the login is not correct, this message will pop up
            flash("Ops! it did not work, try again.", "error")
    # otherwise the user will be redirected to main page and the user's name will be written there
    return render_template("pages/login.html", user=User)

login.login_view = 'connexion'

@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    # if user is connected, he/she will be disconnected.
    if current_user.is_authenticated is True:
        logout_user()
    flash("Bye bye! You are out", "info")
    return redirect("/")



