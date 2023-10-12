from utils_petites_fonctions import *

import matplotlib.pyplot as plt

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

    session = demander_et_garder_last_solves(session)
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


    # faire un truc qui ban la moyenne si dnf, ou qui la change


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
    print(derniere_30_resolutions)
    # todo gérer les cas avec - de 30 solves
    liste_chaque_bo3 = []
    for index_resolution in range(30):
        if index_resolution % 3 == 0:  # l'index est un multiple de 3
            bo3 = min(derniere_30_resolutions[index_resolution], derniere_30_resolutions[index_resolution + 1], derniere_30_resolutions[index_resolution + 2])
            liste_chaque_bo3.append(bo3)
            # print(f"La meilleure résolution du bo3 {index_resolution + 1} est de {bo3} secondes.")
    moyenne_tous_bo3 = sum(liste_chaque_bo3)/10
    print(f" La liste des bo3 est {liste_chaque_bo3}")
    print(f"La moyenne des 10 derniers bo3 est de {moyenne_tous_bo3}")


    # while True:  # tant que l'utilisateur n'a pas bien répondu

    # améliorer la fonction (ajouter une demande, ...)
    nombre_bo3_enleve = 4  # on supprime x solves les plus nulles et x meilleures solves ( on garde 10 - 2*x sovles )
    liste_chaque_bo3 = sorted(liste_chaque_bo3)
    liste_elaguee_bo3 = liste_chaque_bo3[nombre_bo3_enleve: len(liste_chaque_bo3)-nombre_bo3_enleve]
    moyenne_elague_bo3 = sum(liste_elaguee_bo3) / len(liste_elaguee_bo3)
    print(f"La moyenne elaguée en gardant {10 - nombre_bo3_enleve * 2} bo3 est de {moyenne_elague_bo3} s.")

    return moyenne_tous_bo3


def sum_x_last_solves(listes_resolutions, nom_session):
    """Cette fonction fait la somme des temps des x dernières résolutions. x est déterminé grâce à un input vers l'utilisateur. C'est très similaire a la fonction temps_passé, juste ici on peut limiter le nombre de résolutions."""

    listes_resolutions_a_additionner = demander_et_garder_last_solves(listes_resolutions)
    print(listes_resolutions_a_additionner)
    temps_passe(listes_resolutions_a_additionner, nom_session)