# Ce programme fait des statistiques sur les résolutions de cstimer.
# 1) depuis cstimer, exporter vers, en fichier texte
# 2) enregister ce fichier dans un dossier, et copier/coller le chemin du repertoire si dessous (entre les guillements):
repertoire_enregistrement = "D:\docs provisoires\Autre\coding\Python\cstimer statistiques résolutions\cstimer_sauvergarde_utilisee"
# 3) lancer le programme et repondre aux questions


import time

from fonctions_statistiques import *
import os


def obtenir_les_temps(sessions):
    """Cette fonction prend en entrée une liste de sessions et renvoie trois listes : liste_temps_chaque_session, liste_dnf_chaque_session et liste_chaque_session_temps_avec_dnf_comme_inf.
    liste_temps_chaque_session contient les temps de résolution de chaque session.
    liste_dnf_chaque_session contient les temps de résolution "Did Not Finish" (DNF) de chaque session.
    liste_chaque_session_temps_avec_dnf_comme_inf contient les temps de résolution de chaque session, où les DNF sont représentés par l'infini."""
    liste_temps_chaque_session = []  # liste de listes des temps
    liste_dnf_chaque_session = []
    liste_chaque_session_temps_avec_dnf_comme_inf = []

    # obtenir chaque temps, séparé pour chaque sessions
    for session in sessions:
        session = session[4:]  # on enlève le début

        liste_des_resolutions = session.split("[[")

        liste_des_temps = []  # uniquement dans la session actuelle
        liste_des_dnf = []  # pour pouvoir compter le temps passé, même lorsque le cube n'est pas résolu
        liste_temps_avec_dnf_comme_inf = []

        for solve in liste_des_resolutions[1:]:  # [0] correspond au numéro de la session (et pas à une résolution)
            tranchage_temps_avant_brackets = solve.split("]")[0]  # avant le bracket (])

            tranchage_informations_resolutions = tranchage_temps_avant_brackets.split(",")

            temps_de_la_resolution_en_ms = tranchage_informations_resolutions[
                1]  # prend juste l'information du temps principal
            temps_de_la_resolution_en_ms = int(temps_de_la_resolution_en_ms)

            temps_de_la_resolution_en_s = temps_de_la_resolution_en_ms / 1000  # conversion, car cs timer compte en ms

            if tranchage_informations_resolutions[0] == "2000":  # un +2 est noté avec un 2000
                temps_de_la_resolution_en_s += 2

            if tranchage_informations_resolutions[0] != "-1":  # c'est un ok, un dnf est noté avec un -1
                liste_des_temps.append(temps_de_la_resolution_en_s)
                liste_temps_avec_dnf_comme_inf.append(temps_de_la_resolution_en_s)

            else:  # la résolution est dnf (car pas ok ni +2)

                liste_des_dnf.append(temps_de_la_resolution_en_s)
                liste_temps_avec_dnf_comme_inf.append(float("inf"))

        liste_dnf_chaque_session.append(liste_des_dnf)
        liste_temps_chaque_session.append(liste_des_temps)
        liste_chaque_session_temps_avec_dnf_comme_inf.append(liste_temps_avec_dnf_comme_inf)

    return (liste_temps_chaque_session, liste_dnf_chaque_session, liste_chaque_session_temps_avec_dnf_comme_inf)


def separer_sessions(donne_chaque_sessions, temps_chaque_sessions):
    """Cette fonction prend en entrée le contenu et les données de chaque session et renvoie une liste d'informations
    pour chaque session. Les informations de chaque session sont stockées sous la forme [nom_session, index_session]."""
    informations_chaque_session = [0] * len(
        donne_chaque_sessions)  # on veut ranger les sessions dans leur ordre de choix dans cstimer (on ne peut pas juste append)

    for index_session_chronologique in range(
            len(donne_chaque_sessions)):  # l'index correspond à l'ordre de création des sessions, et est donc inchangeable. Il commence par 0
        session = donne_chaque_sessions[index_session_chronologique]

        tranchage_avant_opt = session.split("opt")[
            0]  # on prend tout ce qui est avant le 0 (je crois j'ai fait une erreur, je signifie opt pas 0), pour pouvoir garder le nom et d'autres trucs relous
        nom_session = tranchage_avant_opt[
                      5:-5]  # on enlève les 5 premiers caractères et les 5 derniers, ce sont juste des / et des * ...

        tranchage_apres_rank = session.split("rank")[
            1]  # on enleve tout ce qui est avant le rank, il nous reste (en plus de d'autres trucs) ce qui correspond à la place dans le menu déroulant de la sélection de la session sur cstimer
        second_tranchage_avant_stats = tranchage_apres_rank.split("stat")[
            0]  # on prend tout ce qui est avant l'indicateur des stats
        rank_session_choisi = second_tranchage_avant_stats[
                       3:-3]  # c'est à dire son emplacement dans le déroulé de cs timer qui est changeable par l'utilisateur. Il commence par 1

        if rank_session_choisi.isnumeric():  # jsp pk mais dans certains fichier rank_session pourrait ne pas être un nombre  (c'est un bug de cstimer je pense)
            liste_nom_et_position_dans_text = [nom_session, index_session_chronologique, rank_session_choisi, len(temps_chaque_sessions[index_session_chronologique])]
            informations_chaque_session[
                int(rank_session_choisi) - 1] = liste_nom_et_position_dans_text  # on place chaque nom de session basé sur leur rang (-1 car les index commencent par 0)

        else:
            print(
                "Le paramètrage des sessions rencontre un problème : un des rang est marqué avec l'utilisation de caractères autres que des chiffres. Pour fixer le problème, il faut changer de fichier.")

    return informations_chaque_session


def choix_session(informations_chaque_session, liste_temps_chaque_session, liste_dnf_chaque_session, liste_chaque_session_temps_avec_dnf_comme_inf, liste_chaque_toutes_sessions_combinees):
    """Cette fonction permet à l'utilisateur de choisir une session spécifique à partir des informations fournies.
    Elle affiche la liste des sessions disponibles et demande à l'utilisateur de taper le numéro correspondant à la
    session souhaitée. Elle renvoie les informations de la session choisie : nom_session_statistiques,
     session_statistiques_temps, session_statistiques_dnf, """
    for index_session in range(len(informations_chaque_session)):  # afficher chaque session

        try:  # parfois si aucun nom il peut y avoir un problème
            print(str(index_session + 1) + " : " + str(informations_chaque_session[index_session][0]))


        except:
            print("Aucune session")

    reponse_est_nombre = False
    while not (reponse_est_nombre):

        reponse = input("Tapez le numéro de la session dont vous voulez avoir les informations.")

        if not (reponse.isnumeric()):
            print("Attention, il faut tapez un nombre.")
        else:

            reponse = int(reponse) - 1  # on donne -1 car l'index commence à 0

            if reponse == -1:  # 0, pour toutes les sessions
                return ("Toutes les sessions combinées", *liste_chaque_toutes_sessions_combinees)

            if not(0 <= reponse < len(informations_chaque_session)):
                print("Attention, votre réponse ne correspond à aucune session.")
            else:

                reponse_est_nombre = True

                nom_session_statistiques = informations_chaque_session[reponse][0]
                print(f"Vous avez choisi la session {nom_session_statistiques}")

                index_session_statistiques = informations_chaque_session[reponse][1]

                session_statistiques_temps = liste_temps_chaque_session[
                    index_session_statistiques]  # les temps réussi (on exclut les dnf)
                session_statistiques_dnf = liste_dnf_chaque_session[index_session_statistiques]  # le temps de chaque dnf
                session_statistiques_temps_et_dnf = session_statistiques_temps + session_statistiques_dnf
                session_statistiques_dnf_comme_inf = liste_chaque_session_temps_avec_dnf_comme_inf[index_session_statistiques]

    return (nom_session_statistiques, session_statistiques_temps, session_statistiques_temps_et_dnf, session_statistiques_dnf_comme_inf)



def choix_fonction(nom_session_statistiques, session_statistiques_temps, session_statistiques_temps_et_dnf, session_statistiques_dnf_comme_inf):
    """"""
    # savoir quelle fonction exécuter
    # todo finir (ou pas) car ne fonctionne pas. faire qlq chose de simple, juste des commentaires

    reponse_est_nombre_valide = False  # un nombre entier positif ou bien 0.1 ou 0.01
    liste_fonctions_et_nom = [
        (lambda: creer_nuage_temps(session_statistiques_dnf_comme_inf, nom_session_statistiques), "Nuage des temps"),
        (lambda: encadrement(session_statistiques_dnf_comme_inf), "Encadrement des temps"),
        (lambda: trouver_le_plus_commun(session_statistiques_temps, nom_session_statistiques), "La tranche de temps la plus commune"),
        (lambda: temps_passe(session_statistiques_temps_et_dnf, nom_session_statistiques), "Le temps passé"),
        (lambda: mo10_bo3(session_statistiques_dnf_comme_inf), "La moyenne des 10 derniers bo3"),
        (lambda: sum_x_last_solves(session_statistiques_temps, nom_session_statistiques), "La somme des x derniers temps"),

    ]


    for index_fonction in range(len(liste_fonctions_et_nom)):
        print(f"{index_fonction + 1} : {liste_fonctions_et_nom[index_fonction][1]}")


    # todo utiliser des lambda c'est très stylé
    while not (reponse_est_nombre_valide):

        reponse = input("Tapez le type de statistiques.")

        if not reponse.isdigit():
            print("Attention, il faut tapez un nombre.")
        else:
            reponse = int(reponse)
            if not(reponse<=len(liste_fonctions_et_nom) and reponse !=0):  # la réponse appartient bien à l'intervalle des fonctions possibles
                print("Réponser invalide")

            else:  # on va exécuter la fonction


                fonction_pour_statistiques, nom_fonction_pour_statistiques = liste_fonctions_et_nom[reponse - 1]

                print(f"Vous avez choisi la fonction : {nom_fonction_pour_statistiques}.")
                reponse_est_nombre_valide = True

                try:
                    # Exécution de la fonction choisie avec ses arguments
                    fonction_pour_statistiques()
                    print("La fonction a été exécutée avec succès.")
                except TypeError as e:
                    print(f"Erreur lors de l'exécution de la fonction : {e}")


def generer_statistiques_fichier(fichier_et_chemin_acces):
    """Cette fonction prend en entrée le chemin d'accès au fichier et effectue les statistiques sur les temps de
    résolution des sessions.
    Elle lit le contenu du fichier et extrait les données de résolution de chaque session.
    Elle appelle la fonction obtenir_les_temps pour obtenir les temps de résolution de chaque session.
    Ensuite, elle sépare les sessions et les attribue à chaque session respective en utilisant la fonction
     separer_sessions.
    Elle permet à l'utilisateur de choisir une session spécifique en utilisant la fonction choix_session."""

    with open(# with permet d'ouvrir le fichier et de le refermer automatiquement
            fichier_et_chemin_acces,
            'r',
            encoding="utf8") as fichier:  # sinon problème de décodage, voir https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
            # charger les données

        contenu = fichier.read()  # la longueur est de plus de 1 millions...
    toutes_les_resolutions = contenu.split("]],\"properties\":{\"sessionData\"")[0]  # on exclu tout ce qui est après le long truc contenant les paramètres de cs timer

    sessions = toutes_les_resolutions.split("\"session")  # todo fixer , car si j'écrit session cela fait planter
    sessions = sessions[1:]  # on enlève ce qui est avant la première session

    liste_temps_chaque_session, liste_dnf_chaque_session, liste_chaque_session_temps_avec_dnf_comme_inf = obtenir_les_temps(sessions)

    toutes_les_sessions_combinees_dnf_supprime = [solve for session in liste_temps_chaque_session for solve in session]  # liste de tous les temps, voir https://datascienceparichay.com/article/python-flatten-a-list-of-lists-to-a-single-list/
    toutes_les_sessions_combinees_dnf_comme_reussis = [solve for session in (liste_temps_chaque_session + liste_dnf_chaque_session) for solve in session]
    toutes_les_sessions_combinees_dnf_comme_inf = [solve for session in liste_chaque_session_temps_avec_dnf_comme_inf for solve in session]

    liste_chaque_toutes_sessions_combinees = [toutes_les_sessions_combinees_dnf_supprime, toutes_les_sessions_combinees_dnf_comme_reussis, toutes_les_sessions_combinees_dnf_comme_inf]

    # séparer les sessions
    donnees_tout = contenu.split("sessionData")[1]  # on prend tout ce qui est après l'indication

    donnees_temps_sessions = donnees_tout.split("}}")[0]  # on prend tout ce qui est avant l'indicateur des paramètres
    donnees_parametres = donnees_tout.split("}}")[1]  # on prend tout ce qui est après, cela correspond aux couleurs du background...

    donne_chaque_sessions = donnees_temps_sessions.split("name")[1:]  # on sépare chaque sessions selon leur nom, et on ignore tout ce qui  est avant la première

    # variables inutiles, mais stylées
    nombre_de_dnf = contenu.count("[[-1")  # [[-1" correspond à un dnf
    nombre_de_plus_deux = contenu.count("[[2000")  # [[2000 est mis à chaque début de résolution qui ont un +2


    # avoir le nom de la session:
    informations_chaque_session = separer_sessions(donne_chaque_sessions, liste_temps_chaque_session)

    # utiliser input pour savoir le numéro de session que le gars veut
    (nom_session_statistiques, session_statistiques_temps, session_statistiques_temps_et_dnf, session_statistiques_dnf_comme_inf) = choix_session(informations_chaque_session, liste_temps_chaque_session, liste_dnf_chaque_session, liste_chaque_session_temps_avec_dnf_comme_inf, liste_chaque_toutes_sessions_combinees)
    print(session_statistiques_temps_et_dnf)
    # il peut y avoir une erreur si toutes les sessions ne sont pas nommées

    choix_fonction(nom_session_statistiques, session_statistiques_temps, session_statistiques_temps_et_dnf, session_statistiques_dnf_comme_inf)





# Obtenez la liste des fichiers dans le répertoire de téléchargement
fichiers = os.listdir(repertoire_enregistrement)
# Triez les fichiers par date de modification (le plus récent en premier)
fichiers_tries = sorted(fichiers, key=lambda x: os.path.getmtime(os.path.join(repertoire_enregistrement, x)), reverse=True)

# Vérifiez si des fichiers ont été téléchargés
if fichiers_tries:
    dernier_fichier_telecharge = os.path.join(repertoire_enregistrement, fichiers_tries[0])
    print("Dernier fichier téléchargé :", dernier_fichier_telecharge)
    #todo afficher la date
    generer_statistiques_fichier(dernier_fichier_telecharge)

else:
    print("Aucun fichier téléchargé dans le répertoire spécifié.")




