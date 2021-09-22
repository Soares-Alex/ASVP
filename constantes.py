from warnings import warn

# clé secrète pour les mots de passe usagers
SECRET_KEY = "annuaire statistique de la ville de paris"

# avertissement pour la personne ne connaissant pas la clé secrète
if SECRET_KEY == "les chiffres de l'histoire des services":
    warn("the default secret was changed, you should do it", Warning)