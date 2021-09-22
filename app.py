from flask import Flask
# une application Flask est une instanciation de la classe Flask, que l'on commence par importer.
from flask_sqlalchemy import SQLAlchemy
import os
# le module OS de Python permet d'utiliser les fonctionnalités du système d'exploitation sur lequel s'exécute python.
from .constantes import SECRET_KEY
# import de la clé secrète pour le mot de passe des sessions utilisatrices
from flask_login import LoginManager
# plugin permettant la gestion des usagers
# ce plugin se souvient de l'activité des usagers

# le module os permet d'indiquer un chemin à n'importe quel système d'exploitation sur lequel s'exécute python.
# il indique ici les chemins des dossiers de templates et d'images (statics).
real_track = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(real_track, "templates")
statics = os.path.join(real_track, "static")

# instanciation de l'application
app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics
    )

# mise en place de la gestion d'usagers
login = LoginManager(app)

# configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# configuration du secret
app.config['SECRET_KEY'] = SECRET_KEY

# initiation de l'extension
db = SQLAlchemy(app)

#import the principal way to make the app runs
from .routes import generic






