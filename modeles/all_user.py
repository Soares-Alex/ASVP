from werkzeug.security import generate_password_hash, check_password_hash
# en ajoutant UserMixin à db.Model, on indique à python que User est à la fois un UserMixin et un db.Model
# un mixin implémente des propriétés et méthodes que pourra hériter la classe utilisée

from flask_login import UserMixin
from .. app import db, login

db.metadata.clear()
class User(db.Model, UserMixin):
    Id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    Nom = db.Column(db.Text, nullable=False)
    Login = db.Column(db.String(45), nullable=False, unique=True)
    Email = db.Column(db.Text, nullable=False)
    Mdp = db.Column(db.String(64), nullable=False)

# si tous les paramètres sont remplis, cette fonction renvoie les données de l'utilisateur-ice si l'identification fonctionne.
    @staticmethod
    def identification(login, motdepasse):
        user = User.query.filter(User.Login == login).first()
        if user and check_password_hash(user.Mdp, motdepasse):
            return user
        return None

# fonction pour créer un compte user.
# elle retourne un tuple (booléen, User ou liste) et renvoie une erreur s'il y en a une.
    @staticmethod
    def creer(login, email, nom, motdepasse):
        erreurs = []
        if not login:
            erreurs.append("Insérez un login")
        if not email:
            erreurs.append("Insérez une adresse email")
        if not nom:
            erreurs.append("Insérez un nom")
        # le mot de passe doit être supérieur à 6 caractères
        if not motdepasse :
            erreurs.append("Insérez un mot de passe contenant au moins 6 caractères")
        if len(motdepasse) < 6:
            erreurs.append("Le mot de passe doit contenir au moins 6 caractères")

        # On vérifie que l'email ou le login sont uniques
        uniques = User.query.filter(
            db.or_(User.Email == email, User.Login == login)
        ).count()
        if uniques > 0:
            erreurs.append("L'email ou le login existent déjà")

        # S'il y a au moins une erreur
        if len(erreurs) > 0:
            return False, erreurs

        # Création d'user
        user = User(
            Nom=nom,
            Login=login,
            Email=email,
            Mdp=generate_password_hash(motdepasse)
        )

        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(user)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'user
            return True, user
        except Exception as erreur:
            return False, [str(erreur)]

    def get_id(self):
        # retourne l'identifiant de l'user
        return self.Id

    #fonction permettant de récupérer un user en fonction de son identifiant
    @login.user_loader
    def trouver_utilisateur_via_id(id):
        return User.query.get(int(id))