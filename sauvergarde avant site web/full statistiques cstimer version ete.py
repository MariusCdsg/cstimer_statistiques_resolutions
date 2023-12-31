# mettre les 3 fichiers finis
# Ce programme fait des statistiques sur les résolutions de cstimer.
# 1) depuis cstimer, exporter vers, en fichier texte
# 2) enregister ce fichier dans un dossier, et copier/coller le chemin du repertoire si dessous (entre les guillements):
repertoire_enregistrement = ""
# 3) lancer le programme et repondre aux questions


import time
import os
import matplotlib.pyplot as plt



def isfloat(num):
    """The function test if the string is a number (a float or integer...). See https://www.programiz.com/python-programming/examples/check-string-number"""
    try:
        float(num)
        return True
    except ValueError:
        return False


def truncate_number(num, value):
    """Cette fonction permet de tronquer un nombre, mais pas forcément à un multiple de dix. Par exemple, 27 avec 5
     donne 25 ; 35 avec 6 donne 30..."""
    # en gros la première partie
    return min(num // value * value, num)


def sort_dict_by_value(dictionnaire):
    """Cette fonction trie un dictionnaire en fonction de ces valeurs (du plus grand au plus petit). Voir https://realpython.com/python-sort/#using-sorted-with-a-reverse-argument"""
    sorted_dict = dict(sorted(dictionnaire.items(), key=lambda x: x[1], reverse=True))
    return sorted_dict



def remove_duplicates_from_list(list):
    """Cette fonction permet d'enlever chaque élément dupliqué d'une liste. voir https://www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/"""
    new_list_without_duplicates = []
    [new_list_without_duplicates.append(x) for x in list if x not in new_list_without_duplicates]
    return new_list_without_duplicates


def demander_et_garder_last_solves(session):
    """Cette fonction demande à l'utilisateur combien de résolutions il veut garder. Elle retourne la liste qui contient
     uniquement le nombre de résolutions répondu."""

    # pour optimiser j'aurai pu juste utiliser ask something fonction
    reponse_valide = False
    while not reponse_valide:
        reponse = input("Tapez le nombre de résolution que vous voulez garder (0 si vous voulez garder toutes les résolutions).")
        if reponse.isnumeric():  # on s'assure que la réponse est bonne, pour ne pas déclencher d'erreur
            reponse = int(reponse)  # on transforme en nombre entier
            return session[-reponse:]  # on garde uniquement les reponses des dernières solves

        else:
            print(f"Votre réponse ({reponse}) n'est pas un nombre.")

# cette fonction est inutile, car son utilisation est pas pratique (les conditions sont pas pratiques, car il faut utiliser des lambda...)
def ask_something(question, condition):
    """Cette fonction pose une question à l'utilisateur (le premier paramètre de type str). Elle return la reponse, sauf
     si elle ne reprend pas les conditions (c'est une fonctoin qui prend seulement en paramètre la réponse)."""

    while True:
        reponse = input(question)
        if condition(reponse):
            return reponse
        print("Votre réponse n'est pas valide.")




def trouver_le_plus_commun(session, nom="3 par 3"):
    """Fonction qui permet à l'interieur d'une session de trouver le temps qui est le plus fréquement effectué. Le deuxième paramètre correspond à la précision du calcul (la séparation entre chaque tranche de temps), qui doit être entière (int) ou égale à 0.1 ou 0.01."""

    # plt.hist(session)
    # je pense utiliser plt dès le début aurait été beaucoup plus rapide mais pas grave

    session = demander_et_garder_last_solves(session)

    reponse_est_nombre_valide = False  # un nombre entier positif ou bien 0.1 ou 0.01
    while not (reponse_est_nombre_valide):

        reponse = input("Tapez la précision des encadrements.")

        if not (isfloat(reponse)):
            print("Attention, il faut tapez un nombre.")
        else:
            precision = float(reponse)

            if not (precision >= 1 or precision == 0.1 or precision == 0.01):
                print(f"La précision doit être un nombre entier ou être égale à 0.1 ou 0.01. Vous avez tapé {reponse}")

            else:
                reponse_est_nombre_valide = True
                print(f"Vous avez choisi une précision de {precision}.")

    unique_temps_dans_session_list = []  # contient un tuple pour chaque temps, avec le nombre d'occurrence

    for temps in session:

        temps_tronque = truncate_number(temps, precision)

        # on enlève les 0 si entier
        if type(precision) == int:
            temps_tronque = int(temps_tronque)
        elif precision == 0.1:
            temps_tronque = round(temps_tronque, 1)
        elif precision == 0.01:
            temps_tronque = round(temps_tronque, 2)
        unique_temps_dans_session_list.append([temps_tronque, 0])  # 0 correspond au nombre d'occurence initial (il augmentera plus tard)

    unique_temps_dans_session_list = remove_duplicates_from_list(unique_temps_dans_session_list)
    unique_temps_dans_session_list.sort()


    for solve in session:
        deja_trouve_la_tranche = False
        for index in range(len(unique_temps_dans_session_list)):

            if index + 1 == len(unique_temps_dans_session_list) and not(deja_trouve_la_tranche):
                pass
                unique_temps_dans_session_list[-1][1] += 1  # on ajoute à la dernière tranche de temps directement 1
            # todo je dois aussi gérer quand il y a la solve la plus lente (qui est juste tout supérieure)
            elif unique_temps_dans_session_list[index][0] <= solve and unique_temps_dans_session_list[index + 1][0] > solve:

                unique_temps_dans_session_list[index][1] = unique_temps_dans_session_list[index][1] + 1
                deja_trouve_la_tranche = True  # on évite de redonner 1


    # trouver le maximum d'occurence
    maximum_nombre_occurences = 0
    for index in range(len(unique_temps_dans_session_list)):
        if unique_temps_dans_session_list[index][1] > maximum_nombre_occurences:
            maximum_nombre_occurences = unique_temps_dans_session_list[index][1]



    # trouver les temps avec le maximum d'occurences
    index_with_max_value = []  # initialiser une liste pour stocker les clés correspondantes
    value_of_max_keys = []

    # peut être il y a moyen de combiner les 2 boucles (en écransant si supérieur, si égal ajouter...), la flemme
    for encadrement_temps, nombre_occurrences in unique_temps_dans_session_list:  # parcourir le dictionnaire
        if nombre_occurrences == maximum_nombre_occurences:

            index_with_max_value.append(encadrement_temps)  # ajouter les clés correspondant à la valeur maximale
            value_of_max_keys.append(nombre_occurrences)

    if len(value_of_max_keys) == 1:
        print(f"Le temps le plus fréquent est : {index_with_max_value[0]}, avec comme nombre occurrences : {value_of_max_keys[0]}")
    else:
        print(f"Les temps qui sont les plus fréquents sont : {index_with_max_value}, avec respectivement comme nombre d'occurences : {value_of_max_keys}")

    input("Pour plus de détail, presser entrée.")  # on voit le message d'après que si l'on répond


    # en faire un graphique
    liste_tranches_temps = []
    liste_occurrences_tranches = []
    for index in range(len(unique_temps_dans_session_list)):

        liste_tranches_temps.append(unique_temps_dans_session_list[index][0])
        liste_occurrences_tranches.append(unique_temps_dans_session_list[index][1])

    # Tracé du graphique

    plt.bar(liste_tranches_temps, liste_occurrences_tranches)

    # ajouter des étiquettes et un titre
    plt.xlabel('Temps')
    plt.ylabel('Fréquence')
    plt.title(f'Graphique des occurrences des temps pour {nom}')

    plt.show()



def encadrement(session):
    """Les barrières sont des nombres (type int) qui définissent les valeurs maximale et minimale pour l'encadrement."""

    # obtenir l'encadrement
    liste_messages = ["temps à ne pas dépasser", "temps à dépasser"]
    liste_variables = [0, 0]  # on les changera par la suite par leur valeur
    for i in range(2):
        reponse_est_nombre_valide = False  # un nombre entier positif ou bien 0.1 ou 0.01
        while not (reponse_est_nombre_valide):

            reponse = input(f"Tapez la valeur du {liste_messages[i]}.")

            if not (isfloat(reponse)):
                print("Attention, il faut tapez un nombre.")
            else:
                liste_variables[i] = float(reponse)
                reponse_est_nombre_valide = True
                print(f"Vous avez choisi un {liste_messages[i]} de {reponse}.")
    barriere_up = liste_variables[0]
    barriere_down = liste_variables[1]


    # compter le nombre de résolution dans l'encadrement
    compteur = 0
    for solve in session:
        if solve < barriere_up and solve > barriere_down:
            compteur += 1

    print(f"Le nombre de résolutions sous {barriere_up} secondes et au dessus de {barriere_down} seconde(s) est {compteur} résolution(s).")  # formating string voir https://realpython.com/python-string-formatting/


def temps_passe(temps_session, nom_session):  # todo fix la fonction, car je dois peut être enlever ses paramètres (ce sera toujours juste temps session, mais peut etre que je devrais garder les paramètres pour lecture, et testage, ou alors je peux les supprimer puis mettre des varaialbes qui permettront dde faire des test en les changeant juste eux (et pas directement toutes le valeurs))
    """Cette fonction affiche le temps passé à résoudre sur la session (le paramètre)."""

    temps_total_passe_en_s = 0  # initialisation du résutlat

    for temps_resolution in temps_session:
        temps_total_passe_en_s += temps_resolution

    temps_total_passe_en_h = temps_total_passe_en_s / 3600

    print(f"Le temps total passé à résoudre sur la session {nom_session} est de {temps_total_passe_en_s} secondes, ce qui corresponnd à {temps_total_passe_en_h} heures...")






def creer_nuage_temps(session, nom):
    """Cette fonction affiche un nuage de points des temps de la session (en fonction du numéro de solve). Le nom est de
     type string est est utilisé pour le schéma."""
    session = demander_et_garder_last_solves(session)

    TAILLE_POINTS = 3

    # placer chaque points
    x = range(len(session))  # définir l'abscisse comme le numéro de solve
    y = session

    plt.scatter(x, y,  # créer le nuage de points des temps en fonction du numéro
                s=TAILLE_POINTS,  # changer la taille des points
                c="blue")  # changer la couleur

    # demander le nombre de résolutions de la moyenne
    while True:
        reponse = input("Quelle le nombre de résolution dans la moyenne ?")
        if reponse.isdigit() and int(reponse) > 1 and int(reponse) <= len(session):  # and peut court circuiter : https://stackoverflow.com/questions/2580136/does-python-support-short-circuiting
            moyenne_de_x = int(reponse)
            break
        print("Votre réponse n'est pas valide.")


    liste_moyennes = []  # les aox de chaque solves

    for index_solve in range(moyenne_de_x-1, len(session)):  # on exclu les x-1 premières solves qui n'ont pas de moyenne de x
        moyenne_de_x_de_cette_solve = session[index_solve] / moyenne_de_x  # on divise direct par x pour ne pas refaire de calcul après
        for index_solve_de_la_moyenne in range(moyenne_de_x-1):
            solve_de_la_moyenne = session[index_solve - index_solve_de_la_moyenne]
            moyenne_de_x_de_cette_solve += solve_de_la_moyenne / moyenne_de_x
        liste_moyennes.append(moyenne_de_x_de_cette_solve)

    x = range(moyenne_de_x-1, len(session))
    y = liste_moyennes
    plt.scatter(x, y, s=TAILLE_POINTS, c="green")  # changer la taille des points


    # todo faire un truc qui ban la moyenne si dnf, ou qui la change


    # gérer les pb
    x_tous_les_pb_single = []
    y_tous_les_pb_single = []
    pb_actuel_single = session[0]  # on comparera chaque résolution au pb actuel. Mais la première solve ne comptera pas comme un pb

    x_tous_les_pb_moyenne = []
    y_tous_les_pb_moyenne = []
    pb_actuel_moyenne = liste_moyennes[0]

    for index_solve in range(1, len(session)):
        solve = session[index_solve]
        if solve <= pb_actuel_single:  # si égalité avec un pb, c'est pb anyway
            pb_actuel_single = solve  # maintenant on compare au nouveau pb (on oublie l'ancien)
            x_tous_les_pb_single.append(index_solve)
            y_tous_les_pb_single.append(solve)

        if index_solve > (moyenne_de_x-1):  # on s'assure qu'une moyenne pour cette résolution existe
            index_dans_la_moyenne = index_solve - (moyenne_de_x-1)  # les moyenens sont décalés dans leur liste (les x-1 premiers slots sont vides)
            moyenne = liste_moyennes[index_dans_la_moyenne]
            if moyenne <= pb_actuel_moyenne:
                pb_actuel_moyenne = moyenne
                x_tous_les_pb_moyenne.append(index_solve)
                y_tous_les_pb_moyenne.append(moyenne)

    plt.scatter(x_tous_les_pb_single, y_tous_les_pb_single, c="red")  # on affiche chaque nouveau pb en rouge
    plt.scatter(x_tous_les_pb_moyenne, y_tous_les_pb_moyenne, c="purple")  # on affiche chaque nouveau pb en rouge

    # pb single de toutes les solves
    y_pb_overall = min(session)  # le meilleur sur la session actuellement
    x_pb_overall = session.index(y_pb_overall)  # ne prends pas en compte pour les dupliqués, mais c'est pas grave
    plt.scatter(x_pb_overall, y_pb_overall, c="yellow")  # on affiche le pb overall en noir

    # pb average
    y_pb_overall_moyenne = min(liste_moyennes)
    x_pb_overall_moyenne = liste_moyennes.index(y_pb_overall_moyenne)
    plt.scatter(x_pb_overall_moyenne, y_pb_overall_moyenne, c="pink")

    # autres displays
    plt.xlabel('Index')
    plt.ylabel('Temps')
    plt.title(f'Nuage de points pour {nom}')

    # légende :
    blue_patch = plt.scatter([], [], c='b', label='Temps')
    red_patch = plt.scatter([], [], c='r', label='Anciens pb single')
    yellow_patch = plt.scatter([], [], c='y', label='Dernier pb single')

    green_patch = plt.scatter([], [], c='g', label=f'ao{moyenne_de_x}')
    purple_patch = plt.scatter([], [], c='purple', label=f'Anciens pb ao{moyenne_de_x}')
    pink_patch = plt.scatter([], [], c='pink', label=f'Dernier pb ao{moyenne_de_x}')
    plt.legend(handles=[blue_patch, red_patch, yellow_patch, green_patch, purple_patch, pink_patch],  # la liste contient chaque données de la légende ranger de haut en bas
               loc='upper right')  # loc permet de placer la légende
    plt.show()


def mo10_bo3(liste_resolutions):
    """Cette fonction calcule la moyenne de 10 bo3 (pour calculer le global)."""

    derniere_30_resolutions = liste_resolutions[-30:]
    # todo gérer les cas avec - de 30 solves
    liste_chaque_bo3 = []
    for index_resolution in range(30):
        if index_resolution % 3 == 0:  # l'index est un multiple de 3
            bo3 = min(derniere_30_resolutions[index_resolution], derniere_30_resolutions[index_resolution + 1], derniere_30_resolutions[index_resolution + 2])
            liste_chaque_bo3.append(bo3)
            # print(f"La meilleure résolution du bo3 {index_resolution + 1} est de {bo3} secondes.")
    moyenne_tous_bo3 = sum(liste_chaque_bo3)/10
    print(f"La moyenne des 10 derniers bo3 est de {moyenne_tous_bo3}")

    # nombre_bo3_enleve = 4  # on supprime x solves les plus nulles et x meilleures solves ( on garde 10 - 2*x sovles )
    # liste_chaque_bo3 = sorted(liste_chaque_bo3)
    # liste_elaguee_bo3 = liste_chaque_bo3[nombre_bo3_enleve: len(liste_chaque_bo3)-nombre_bo3_enleve]
    # moyenne_elague_bo3 = sum(liste_elaguee_bo3) / len(liste_elaguee_bo3)
    # print(f"La moyenne elaguée en gardant {10 - nombre_bo3_enleve * 2} bo3 est de {moyenne_elague_bo3} s.")

    return moyenne_tous_bo3



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
        (lambda: creer_nuage_temps(session_statistiques_temps, nom_session_statistiques), "Nuage des temps"),
        (lambda: encadrement(session_statistiques_temps), "Encadrement des temps"),
        (lambda: trouver_le_plus_commun(session_statistiques_temps, nom_session_statistiques), "La tranche de temps la plus commune"),
        (lambda: temps_passe(session_statistiques_temps_et_dnf, nom_session_statistiques), "Le temps passé"),
        (lambda: mo10_bo3(session_statistiques_dnf_comme_inf), "La moyenne des 10 derniers bo3")
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
    generer_statistiques_fichier(dernier_fichier_telecharge)
else:
    print("Aucun fichier téléchargé dans le répertoire spécifié.")
