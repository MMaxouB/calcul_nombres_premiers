"""
But :
Trouver les n premiers nombres premiers

Ce fichier contient une version simple et directe pour générer
les premiers nombres premiers en testant la primalité d'un candidat
par division jusqu'à sa racine carrée.
"""

import time

# Début du chronométrage global
time_start = time.time()

# (option pour plus tard) demander n à l'utilisateur : pratique mais désactivée
"""n = int(input("Combien de nombres premuiers ?"))"""  # à réactiver si besoin

# Fichier de sortie où écrire la liste des premiers
OUTPUT_FILE = "premiers.txt"

# Nombre de nombres premiers que l'on veut obtenir
n = 1_000_000  # nombre de premiers à générer


# Fonction de test de primalité
def is_prime(v):
    """Retourne True si `v` est premier, False sinon.

    Méthode :
    - rejette les cas triviaux (nombres < 2)
    - traite 2 comme cas particulier
    - rejette les pairs (>2)
    - teste les diviseurs impairs jusqu'à sqrt(v)
    """

    # Cas triviaux : 0, 1 ne sont pas premiers
    if v < 2:
        return False

    # 2 est le seul nombre pair premier
    if v == 2:
        return True

    # Éliminer tous les autres pairs
    if v % 2 == 0:
        return False

    # On n'a besoin de tester des diviseurs que jusqu'à la racine carrée
    # r est la borne supérieure entière pour les diviseurs à tester
    r = int(v ** 0.5)

    # Tester seulement les diviseurs impairs : 3,5,7,...,r
    for d in range(3, r + 1, 2):
        # Si on trouve un diviseur, ce n'est pas premier
        if v % d == 0:
            return False

    # Aucun diviseur trouvé -> v est premier
    return True


# Génération des n premiers nombres premiers
primes = []            # liste pour stocker les premiers trouvés
candidate = 2          # premier candidat à tester (commence à 2)

"""

# Boucle principale : on itère jusqu'à trouver n nombres premiers
for i in range(n-1):
    # Tester le candidat courant
    if is_prime(candidate):
        # Si premier, l'ajouter à la liste résultat
        primes.append(candidate)
    # Passer au candidat suivant
    candidate += 1
"""
while len(primes) < n:   # boucle jusqu'à avoir exactement n nombres premiers
    if is_prime(candidate):
        primes.append(candidate)
    candidate += 1

# Écriture des résultats dans le fichier de sortie
with open(OUTPUT_FILE, "w") as f:
    for p in primes:
        f.write(f"{p}\n")

    # Chronométrage : écrire le temps total d'exécution
    time_end = time.time()
    f.write(f"Temps d'execution : {time_end - time_start:.2f} secondes")