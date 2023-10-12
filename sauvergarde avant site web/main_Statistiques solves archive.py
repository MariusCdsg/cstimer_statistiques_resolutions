
from fonctions_statistiques import *

def faire_statistiques(fichier_et_chemin_acces):
    # with open('D:\docs provisoires\Autre\coding\Python\cstimer statistiques résolutions\cstimer_save_exemple.txt', 'r') as fichier:  # with permet d'ouvrir le fichier et de le refermer automatiquement
    with open(# with permet d'ouvrir le fichier et de le refermer automatiquement
            fichier_et_chemin_acces,
            'r',
            encoding="utf8") as fichier:  # sinon problème de décodage, voir https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character
        # charger les données

        contenu = fichier.read()  # la longueur est de plus de 1 millions...
    toutes_les_resolutions = contenu.split("]],\"properties\":{\"sessionData\"")[0]  # on exclu tout ce qui est après le long truc contenant les paramètres de cs timer

    sessions = toutes_les_resolutions.split("session")
    sessions = sessions[1:]  # on enlève ce qui est avant la première session

    liste_temps_chaque_session = []  # liste de listes des temps
    liste_dnf_chaque_session = []


    # obtenir chaque temps, séparé pour chaque sessions
    for session in sessions:



        session = session[4:]  # on enlève le début

        liste_des_resolutions = session.split("[[")
        liste_des_temps = []  # uniquement dans la session actuelle
        liste_des_dnf = []  # pour pouvoir compter le temps passé, même lorsque le cube n'est pas résolu

        for solve in liste_des_resolutions[2:]:
            tranchage_temps_avant_brackets = solve.split("]")[0]  # avant le bracket (])

            tranchage_informations_resolutions = tranchage_temps_avant_brackets.split(",")



            temps_de_la_resolution_en_ms = tranchage_informations_resolutions[1]  # prend juste l'information du temps principal
            temps_de_la_resolution_en_ms = int(temps_de_la_resolution_en_ms)


            temps_de_la_resolution_en_s = temps_de_la_resolution_en_ms / 1000  # conversion, car cs timer compte en ms

            if tranchage_informations_resolutions[0] == "2000":  # un +2 est noté avec un 2000
                temps_de_la_resolution_en_s += 2

            if tranchage_informations_resolutions[0] != "-1":  # c'est un ok un dnf est noté avec un -1
                liste_des_temps.append(temps_de_la_resolution_en_s)


            else:  # la résolution est dnf (car pas ok ni +2)


                liste_des_dnf.append(temps_de_la_resolution_en_s)


        liste_dnf_chaque_session.append(liste_des_dnf)
        # todo remove after test
        # liste_des_temps.append(liste_des_temps)  # on ajoute le temps du dnf à la fin, on l'enlevera plus tard
        liste_temps_chaque_session.append(liste_des_temps)

    # print("bonjour"[3:])
    # for index_session in range(len(liste_temps_chaque_session)):
    #     print(f"l'index est : {index_session}. Voici les 10 premières solve de celle ci : ")
    #     print(liste_temps_chaque_session[index_session][:10])
    # print("la session de sq1")
    # print(liste_temps_chaque_session[21])
    # print(liste_temps_chaque_session)
    #
    # # print(liste_temps_chaque_session[22])

    # le problème se trouve avant cette ligne #todo le trouver

    # séparer les sessions
    donnees_tout = contenu.split("sessionData")[1]  # on prend tout ce qui est après l'indication

    donnees_temps_sessions = donnees_tout.split("}}")[0]  # on prend tout ce qui est avant l'indicateur des paramètres
    donnees_parametres = donnees_tout.split("}}")[1]  # on prend tout ce qui est après, cela correspond aux couleurs du background...

    donne_chaque_sessions = donnees_temps_sessions.split("name")[1:]  # on sépare chaque sessions selon leur nom, et on ignore tout ce qui  est avant la première


    informations_chaque_session = [0] * len(donne_chaque_sessions)  # on veut ranger les sessions dans leur ordre de choix dans cstimer (on ne peut pas juste append)


    toutes_les_session_combinees = [solve for session in liste_temps_chaque_session for solve in session]  # liste de tous les temps, voir https://datascienceparichay.com/article/python-flatten-a-list-of-lists-to-a-single-list/


    # fixer les sessions, certaines sont vides (jsp pk)
    if True:  # todo remove aftert test
    # try:
        # avoir le nom de la session:
        for index_session in range(len(donne_chaque_sessions)):  # l'index correspond à l'ordre de création des sessions, et est donc inchangeable
            session = donne_chaque_sessions[index_session]

            tranchage_avant_opt = session.split("opt")[0]  # on prend tout ce qui est avant le 0 (je crois j'ai fait une erreur, je signifie opt pas 0), pour pouvoir garder le nom et d'autres trucs relous
            nom_session = tranchage_avant_opt[5:-5]  # on enlève les 5 premiers caractères et les 5 derniers, ce sont juste des / et des * ...

            tranchage_apres_rank = session.split("rank")[1]  # on enleve tout ce qui est avant le rank, il nous reste (en plus de d'autres trucs) ce qui correspond à la place dans le menu déroulant de la sélection de la session sur cstimer
            second_tranchage_avant_stats = tranchage_apres_rank.split("stat")[0]  # on prend tout ce qui est avant l'indicateur des stats
            rank_session = second_tranchage_avant_stats[3:-3]  # c'est à dire son emplacement dans le déroulé de cs timer qui est changeable par l'utilisateur


            if rank_session.isnumeric():  # jsp pk mais dans certains fichier rank_session pourrait ne pas être un nombre  (c'est un bug de cstimer je pense)
                liste_nom_et_position_dans_text = [nom_session, index_session]
                informations_chaque_session[int(rank_session)-1] = liste_nom_et_position_dans_text  # on place chaque nom de session basé sur leur rang (-1 car les index commencent par 0)
            else:
                print("Le paramètrage des sessions rencontre un problème : un des rang est marqué avec l'utilisation de caractères autres que des chiffres. Pour fixer le problème, il faut changer de fichier.")


        # print(informations_chaque_session)
        # print(liste_temps_chaque_session[20])
        # utiliser input pour savoir le numéro de session que le gars veut
        for index_session in range(len(informations_chaque_session)):  # afficher chaque session


            try:  # parfois si aucun nom il peut y avoir un problème
                print(str(index_session + 1) + " : " + str(informations_chaque_session[index_session][0]))
            except:
                print("Aucune session")


        reponse_est_nombre = False
        while not(reponse_est_nombre):

            reponse = input("Tapez le numéro de la session dont vous voulez savoir les informations.")

            if not(reponse.isnumeric()):
                print("Attention, il faut tapez un nombre.")
            else:
                reponse = int(reponse) - 1  # on donne -1 car l'index commence à 0
                reponse_est_nombre = True

                nom_session_statistiques = informations_chaque_session[reponse][0]

                index_session_statistiques = informations_chaque_session[reponse][1]

                temps_session_statistiques = liste_temps_chaque_session[index_session_statistiques]  # les temps réussi (on exclut les dnf)
                dnf_session_statistiques = liste_dnf_chaque_session[index_session_statistiques]  # le temps de chaque dnf
                temps_et_dnf_session_statistiques = temps_session_statistiques + dnf_session_statistiques




                print(f"Vous avez choisi la session {nom_session_statistiques}")

    # except Exception as e:  # erreur peut être si toutes les sessions ne sont pas nommées ? (genre pour papa)
    #     print(f"La boucle des attributions de nom aux sessions a déclenché une erreur : {e}")
    #     temps_session_statistiques = toutes_les_session_combinees
    #     nom_session_statistiques = "3 par 3"

    # todo prendre uniquement les x last solves, pour rendre les stats représentatives

    print(temps_session_statistiques)

    # chaque fonction appelée individuellement :

    #creer_graphique(temps_session_statist  iques)
    # encadrement(temps_session_statistiques)
    # trouver_le_plus_commun(temps_session_statistiques, nom_session_statistiques)
    # creer_nuage_temps(temps_session_statistiques, nom_session_statistiques)
    # temps_passe(temps_et_dnf_session_statistiques, "dnf sessions")

    # print(temps_session_statistiques)  # temporaire pour savoiur si le prblm est fixé


    # savoir quel fonction exécuter

    reponse_est_nombre_valide = False  # un nombre entier positif ou bien 0.1 ou 0.01
    liste_fonctions_et_nom = [[creer_nuage_temps, "Nuage des temps"], [encadrement, "Encadrement des temps"], [trouver_le_plus_commun, "La tranche de temps la plus commune"], [temps_passe, "Le temps passé"]]  # chaque fonction avec leur nom
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
                fonction_pour_statistiques = liste_fonctions_et_nom[reponse-1][0]  # on prend la fonction au niveau de l'index de la réponse (on enlève donc 1 pour le décalage)
                nom_fonction_pour_statistiques = liste_fonctions_et_nom[reponse-1][1]
                print(f"Vous avez choisi la fonction : {nom_fonction_pour_statistiques}.")
                reponse_est_nombre_valide = True


                # Essai d'exécution de la fonction avec chaque tuple d'arguments possibles
                arguments_possibles = [
                    (temps_session_statistiques, nom_session_statistiques),
                    (temps_session_statistiques,)  #  , pour montrer que c'est un tuple et non des parenthèses de calculs

                ]
                for args in arguments_possibles:
                    try:
                        if len(args) >1:
                            fonction_pour_statistiques(*args)
                        else:  # un seul argument, on ne veut pas le toucher si c'est une liste
                            fonction_pour_statistiques(args)
                        print("La fonction a été exécutée avec succès avec les arguments :", args)
                        break
                    except TypeError as e:
                        # print(e)
                        continue
                else:  # si on break pas
                    print("aucune fonction avec ces arguements")

            #         print("nope")

    # fixe rcette fonction
    temps_passe(temps_session_statistiques, nom_session_statistiques)

    # temps_passe(nom_session_statistiques)
    # trouver_le_plus_commun(temps_session_statistiques)
    # encadrement(temps_session_statistiques)


    nombre_de_dnf = contenu.count("[[-1")  # [[-1" correspond à un dnf
    nombre_de_plus_deux = contenu.count("[[2000")  # [[2000 est mis à chaque début de résolution qui ont un +2



#todo améliorer l'interface de sélection (juste rendre clair, créer une zone tout en haut pour add expliquer et montrer, puis un input de sélection du fichier (optionnel))
fichier_papa_8_mars = 'D:\docs provisoires\Autre\coding\Python\cstimer statistiques résolutions\cstimer_papa.txt'
fichier_moi_9_mars = 'D:\docs provisoires\Autre\coding\Python\cstimer statistiques résolutions\cstimer_new.txt'
fichier_moi_11_mars = 'D:\docs provisoires\Autre\coding\Python\cstimer statistiques résolutions\cstimer_11_mars.txt'
fichier_moi_22_mars = 'D:\docs provisoires\Autre\coding\Python\cstimer statistiques résolutions\cstimer_end.txt'
fichier_papa_24_mars = 'D:\docs provisoires\Autre\coding\Python\cstimer statistiques résolutions\cstimer_papa_24_mars.txt'
fichier_papa_25_mars = 'D:\docs provisoires\Autre\coding\Python\cstimer statistiques résolutions\cstimer_papa_25_mars.txt'
fichier_moi_4_avril = 'D:\docs provisoires\Autre\coding\Python\cstimer statistiques résolutions\cstimer_4_avril.txt'  # je crois on est le 3 en fait
moi_21_avril = 'D:\docs provisoires\Autre\coding\Python\cstimer statistiques résolutions\cstimer_21_avril.txt'
moi_22_avril = 'D:\docs provisoires\Autre\coding\Python\cstimer statistiques résolutions\cstimer_22_avril.txt'  # je delete les sessions vides (peut être elles font buggé ?)
# le problème était dans le fichier texte : un numéro de session était "SE" (normalement c'est un nombre)
moi_24_avril = 'D:\docs provisoires\Autre\coding\Python\cstimer statistiques résolutions\cstimer_24_avril.txt'
papa_1_mai = 'D:\docs provisoires\Autre\coding\Python\cstimer statistiques résolutions\cstimer_papa_1_mai.txt'
faire_statistiques(moi_24_avril )
# faire_statistiques(fichier_papa_25_mars)

