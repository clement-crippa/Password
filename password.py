import re
import hashlib
import json


def mdp_valide(mdp):
    # Vérifie si le mot de passe fait minimum 8 caractères
    if len(mdp) < 8:
        return False
    # Vérifie s'il y a une lettre minuscule entre a et z dans le mot de passe
    if not re.search("[a-z]", mdp):
        return False
    # Vérifie s'il y a une lettre majuscule entre a et z dans le mot de passe
    if not re.search("[A-Z]", mdp):
        return False
    # Vérifie s'il y a un chiffre entre 0 et 9 dans le mot de passe
    if not re.search("[0-9]", mdp):
        return False
    # Vérifie s'il y a un des symboles de la liste dans le mot de passe
    if not re.search("[!@#$%^&*]", mdp):
        return False
    return True


def mdp_crypter(mdp):
    # Permet d'encoder les caractères spéciaux comme les accents et les symboles
    mdp_a_crypter = mdp.encode()
    # Définie le hachage en SHA-256
    hachage = hashlib.sha256(mdp_a_crypter)
    # Hache le mot de passe en hexadécimal
    mdp_digest = hachage.hexdigest()
    return mdp_digest


def mdp_identique(mdp_digest, mdp_liste):
    # Vérifie si le mot de passe crypté existe déjà
    for x in mdp_liste:
        if mdp_digest == x["Mot_de_passe_crypte"]:
            return True
    return False


while True:
    mdp = input("Entrer un mot de passe valide: ")
    if mdp_valide(mdp):
        mdp_crypter_final = mdp_crypter(mdp)
        # Chargement des informations du fichier
        with open("mdp.txt", "r") as file:
            mdp_liste = [json.loads(line) for line in file.readlines()]
            # Si le mot de passe est déjà présent dans le fichier
        if mdp_identique(mdp_crypter_final, mdp_liste):
            print("Le mot de passe existe déjà. Veuillez entrer un nouveau mot de passe.")
        else:
            print("Le mot de passe est valide.")
            print("Mot de passe crypté:", mdp_crypter_final)
            # Ajout des informations au fichier
            with open("mdp.txt", "a") as file:
                file.write(json.dumps({"Mot_de_passe": mdp, "Mot_de_passe_crypte": mdp_crypter_final}) + "\n")
            break
    else:
        # Si le mot de passe ne correspond pas au critère
        print("Le mot de passe n'est pas valide. Veuillez entrer un mot de passe valide.")

# Affichage de tous les mots de passe du fichier txt
with open("mdp.txt", "r") as file:
    mdps = [json.loads(line) for line in file.readlines()]
    print(mdps)
