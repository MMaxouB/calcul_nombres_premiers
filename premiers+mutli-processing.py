"""
But :
Trouver les n premiers nombres premiers
en utilisant plusieurs cœurs CPU (multiprocessing)

Ce fichier montre une approche simple parallèle :
on découpe l'intervalle de recherche en plages et on teste
la primalité de chaque entier dans chaque plage via plusieurs processus.
"""

import time
import math
from multiprocessing import Pool, cpu_count


# -----------------------------
# Début du chronométrage global
# -----------------------------
time_start = time.time()

# Fichier de sortie
OUTPUT_FILE = "premiers_complexe.txt"

# Nombre de nombres premiers que l'on veut AU FINAL
n = 1_000_000  # nombre de premiers à générer en tout 


def estimate_max_n(n):
    """Estime une borne supérieure suffisante pour le n-ième premier.

    Pour n >= 6 on utilise l'approximation p_n ≈ n (ln n + ln ln n)
    et on ajoute une marge de sécurité (10% ou +10).
    Pour les très petites valeurs, on retourne une petite borne sûre.
    """
    if n < 6:
        # cas très petits : on prend une borne fixe sûre
        return 15
    else:
        # approximation classique issue du théorème des nombres premiers
        approx = n * (math.log(n) + math.log(math.log(n)))
        # marge de sécurité : 10 % ou +10 minimum
        return int(approx + max(10, approx * 0.1))


# Limite maximale de recherche (nombre de nombres qu'on devra tester)
MAX_N = estimate_max_n(n)


# -----------------------------
# Test de primalité (même logique que dans main.py)
# -----------------------------
def is_prime(v):
    """Test basique de primalité par essais de divisions.

    - rejette les cas triviaux
    - gère 2 séparément
    - élimine les pairs
    - teste les diviseurs impairs jusqu'à sqrt(v)
    """
    # Cas triviaux
    if v < 2:
        return False

    # 2 est premier
    if v == 2:
        return True

    # Les nombres pairs > 2 ne sont pas premiers
    if v % 2 == 0:
        return False

    # On teste jusqu'à la racine carrée
    r = int(v ** 0.5)

    # On teste seulement les diviseurs impairs
    for d in range(3, r + 1, 2):
        if v % d == 0:
            return False

    return True


# -------------------------------------------------
# Fonction exécutée par CHAQUE PROCESS
# -------------------------------------------------
def find_primes_in_range(args):
    """Chaque process reçoit une plage (start, end)
    et renvoie la liste des nombres premiers trouvés dans cette plage.
    """
    start, end = args
    primes_local = []

    # Parcourir chaque entier de la plage et tester la primalité
    for candidate in range(start, end):
        if is_prime(candidate):
            primes_local.append(candidate)

    return primes_local


# -------------------------------------------------
# Programme principal (obligatoire sous Windows)
# -------------------------------------------------
if __name__ == "__main__":

    # Détecter le nombre de cœurs physiques/logiques disponibles
    cores = cpu_count()

    # Taille d'une plage de calcul par cœur (division simple du travail)
    chunk_size = MAX_N // cores

    ranges = []

    # Découpage de [0 → MAX_N] en plages pour chaque process
    for i in range(cores):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        ranges.append((start, end))

    # Création du pool de processus
    with Pool(cores) as pool:
        # Chaque process travaille sur sa plage via find_primes_in_range
        results = pool.map(find_primes_in_range, ranges)

    # Fusion de toutes les listes de nombres premiers renvoyées par les processus
    primes = []
    for part in results:
        primes.extend(part)

    # Tri nécessaire car chaque process a travaillé sur sa plage indépendamment
    primes.sort()

    # On ne garde que les n premiers (au cas où MAX_N était une sur-approximation)
    primes = primes[:n]

    # -----------------------------
    # Écriture dans le fichier
    # -----------------------------
    with open(OUTPUT_FILE, "w") as f:
        for p in primes:
            f.write(f"{p}\n")

        time_end = time.time()
        f.write(f"\nTemps d'execution : {time_end - time_start:.2f} secondes")
