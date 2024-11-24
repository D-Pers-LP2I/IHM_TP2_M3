import sys
import re  # Importer re pour les expressions régulières
import requests  # Importer requests pour effectuer la requête API
from PyQt5.QtWidgets import QApplication, QMainWindow
from interface_connexion import Ui_Form  # Importer l'IHM

class ConnexionApp(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Connecter le bouton Valider à une fonction
        self.bouton_valider.clicked.connect(self.valider_formulaire)

    def valider_formulaire(self):
        # Récupérer les valeurs des champs de saisie
        identifiant = self.lineEdit_identifiant.text()
        mot_de_passe = self.lineEdit_motDePasse.text()
        email = self.lineEdit_email.text()

        # Vérifier si les champs sont correctement remplis
        if not identifiant or not mot_de_passe or '@' not in email:
            self.afficher_message("Erreur : veuillez remplir correctement tous les champs.")
            return

        # Analyser la robustesse du mot de passe
        resultat_analyse = self.analyser_mot_de_passe(mot_de_passe)
        if resultat_analyse != "Le mot de passe est robuste.":
            self.afficher_message(resultat_analyse)
            return

        # Vérifier si l'adresse e-mail est compromise
        if self.verifier_email_compromis(email):
            self.afficher_message("Attention : cette adresse e-mail a été compromise.")
            return

        # Si toutes les vérifications passent
        self.afficher_message("Connexion réussie.")

    def analyser_mot_de_passe(self, mot_de_passe):
        # Vérifier la longueur du mot de passe
        if len(mot_de_passe) < 8:
            return "Le mot de passe doit contenir au moins 8 caractères."
        elif not re.search(r"[A-Z]", mot_de_passe):
            return "Le mot de passe doit contenir au moins une majuscule."
        elif not re.search(r"[0-9]", mot_de_passe):
            return "Le mot de passe doit contenir au moins un chiffre."
        elif not re.search(r"[@#$%^&*!]", mot_de_passe):
            return "Le mot de passe doit contenir au moins un caractère spécial."
        else:
            return "Le mot de passe est robuste."

    # Fonction pour vérifier si l'adresse e-mail est compromise
    def verifier_email_compromis(self, email):
        try:
            headers = {
                "hibp-api-key": "YOUR_API_KEY",  # Remplacez par votre clé API HIBP
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", headers=headers)
            if response.status_code == 200:
                return True  # L'email a été compromis
            elif response.status_code == 404:
                return False  # L'email n'a pas été compromis
            else:
                # Pour gérer d'autres codes de réponse ou des erreurs
                print(f"Erreur API : {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"Erreur lors de la requête API : {e}")
            return False

    # Fonction pour afficher un message dans le QLabel
    def afficher_message(self, message):
        self.label_message.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = ConnexionApp()
    fenetre.show()
    sys.exit(app.exec_())
