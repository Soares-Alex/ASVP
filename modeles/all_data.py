from .. app import db

# our model to collect data from user to our database
class Statistique(db.Model):

    statistique_id = db.Column(db.Integer, unique=True, autoincrement=True, primary_key=True, nullable=False)
    categorie = db.Column(db.String(100))
    entree = db.Column(db.String(50))
    annee = db.Column(db.String(100))
    mois = db.Column(db.String(100))
    totaux = db.Column(db.String(100))
    description = db.Column(db.String(500))
