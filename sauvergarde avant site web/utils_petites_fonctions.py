
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