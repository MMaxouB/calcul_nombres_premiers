"""
But :
Trouver les n premiers nombres premiers
en utilisant plusieurs cœurs CPU (multiprocessing) et le crible d'Ératosthène

Cette version découpe l'espace en blocs et utilise un crible segmenté
pour marquer les composites dans chaque bloc en parallèle.
"""

"""
APPROXIMATION DU N-IÈME NOMBRE PREMIER

Approximation du n-ième nombre premier.
Formule issue des raffinements du théorème des nombres premiers :
p_n ≈ n (ln n + ln ln n)
Voir Rosser & Schoenfeld (1962) pour les bornes précises.

"""

import time
import math
from multiprocessing import Pool, cpu_count

# -----------------------------
# Début du chronométrage
# -----------------------------
time_start = time.time()

OUTPUT_FILE = "premiers_crible.txt"

# Nombre de nombres premiers que l'on veut AU FINAL
n = 1_000_000  # nombre de premiers à générer

# -----------------------------
# Calculer MAX_N avec marge adaptative
# -----------------------------
def estimate_max_n(n):
    """Estime une borne supérieure suffisante pour contenir au moins n premiers."""
    if n < 6:
        return 15  # cas très petits
    else:
        approx = n * (math.log(n) + math.log(math.log(n)))  # voir explications ci-dessus
        return int(approx + max(10, approx * 0.1))

MAX_N = estimate_max_n(n)

# -----------------------------
# Crible d'Ératosthène classique pour les nombres jusqu'à √MAX_N
# On calcule d'abord tous les petits premiers nécessaires pour criber
# les blocs plus grands (crible segmenté)
# -----------------------------
sqrt_max = int(MAX_N ** 0.5) + 1
crible_small = [True] * sqrt_max
crible_small[0:2] = [False, False]  # 0 et 1 ne sont pas premiers

primes_up_to_sqrt = []
for i in range(2, sqrt_max):
    if crible_small[i]:
        # i est premier, on l'ajoute à la liste
        primes_up_to_sqrt.append(i)
        # marquer les multiples de i comme non-premiers dans le petit crible
        for multiple in range(i * i, sqrt_max, i):
            crible_small[multiple] = False

# -------------------------------------------------
# Fonction pour marquer les multiples dans un bloc (pour le crible segmenté)
# -------------------------------------------------
def mark_block(args):
    """Marque les nombres composés dans l'intervalle [start, end) en utilisant
    la liste `primes_small` (tous les premiers ≤ sqrt(MAX_N)).

    Retourne une liste booléenne `block` où True signifie "potentiellement premier".
    """
    start, end, primes_small = args
    block = [True] * (end - start)

    # Pour chaque petit premier p, marquer ses multiples dans le bloc
    for p in primes_small:
        # Le premier multiple de p >= start. On prend au moins p*p.
        first = max(p * p, ((start + p - 1) // p) * p)
        for multiple in range(first, end, p):
            block[multiple - start] = False
    return block

# -------------------------------------------------
# Programme principal
# -------------------------------------------------
if __name__ == "__main__":

    # Nombre de cœurs à utiliser
    cores = cpu_count()
    # Taille d'un bloc pour chaque process (division simple)
    chunk_size = MAX_N // cores
    ranges = []

    # Préparer les plages ; le dernier bloc va jusqu'à MAX_N inclus
    for i in range(cores):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != cores - 1 else MAX_N + 1
        ranges.append((start, end, primes_up_to_sqrt))

    # Exécuter le marquage en parallèle pour chaque bloc
    with Pool(cores) as pool:
        results = pool.map(mark_block, ranges)

    # Fusionner tous les blocs marqués pour reconstruire le crible complet
    full_crible = []
    for block in results:
        full_crible.extend(block)

    # Extraire exactement n nombres premiers depuis l'indexation du crible
    primes = [i for i, is_p in enumerate(full_crible) if is_p]
    primes = primes[:n]

    # -----------------------------
    # Écriture dans le fichier
    # -----------------------------
    with open(OUTPUT_FILE, "w") as f:
        for p in primes:
            f.write(f"{p}\n")

        time_end = time.time()
        f.write(f"\nTemps d'execution : {time_end - time_start:.2f} secondes")
