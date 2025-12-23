
**Project**: Génération des n premiers nombres premiers

- **But**: fournir trois approches pour générer les n premiers nombres premiers :
	- une version simple (tests de primalité par division),
	- une version multi-processus par découpage d'intervalles,
	- une version multi-processus utilisant un crible segmenté (Ératosthène).

**Fichiers importants**
- `premiers.py` : implémentation simple qui teste chaque candidat par division jusqu'à sa racine carrée et écrit le résultat dans `premiers.txt`.
- `premiers+mutli-processing.py` : découpe l'intervalle de recherche en plages et lance plusieurs processus pour tester la primalité dans chaque plage ; résultat écrit dans `premiers_complexe.txt`.
- `premiers+multi+crible.py` : implémentation du crible segmenté exécuté en parallèle par blocs ; résultat écrit dans `premiers_crible.txt`.

**Prérequis**
- Python 3.8+ (recommandé). Les modules utilisés sont dans la bibliothèque standard (`time`, `math`, `multiprocessing`).

**Paramètres**
- Dans chaque script, la variable `n` définit combien de nombres premiers au total on souhaite générer. Par défaut elle est fixée à `1_000_000`.
- Les scripts estiment une borne supérieure `MAX_N` pour la recherche du n-ième premier (approximation de Rosser & Schoenfeld). Vous pouvez réduire `n` pour des essais rapides.

**Usage**
- Exécuter la version simple :

```bash
python "premiers.py"
```

- Exécuter la version multiprocessing (simple) :

```bash
python "premiers+mutli-processing.py"
```

- Exécuter la version multiprocessing + crible segmenté :

```bash
python "premiers+multi+crible.py"
```

Remarques pour Windows : tous les scripts utilisent correctement la garde `if __name__ == "__main__"` lorsque nécessaire, ce qui est requis pour `multiprocessing` sous Windows.

**Fichiers de sortie**
- `premiers.txt` — sortie de la version simple.
- `premiers_complexe.txt` — sortie de la version multi-processus (découpage simple).
- `premiers_crible.txt` — sortie de la version multi-processus utilisant le crible.

Chaque fichier contient une liste de nombres premiers (un par ligne) suivie d'une ligne contenant le temps d'exécution global.

**Conseils de performance et mémoire**
- La méthode simple (`premiers.py`) est lente pour de grands `n` car elle teste chaque entier individuellement.
- La version multi-processus réduit le temps de calcul en utilisant plusieurs cœurs, mais la duplication de travail et des structures en mémoire peut augmenter l'usage mémoire.
- Le crible segmenté est généralement la meilleure option pour large `n` car il réduit les tests par division et permet un marquage efficace par blocs. Toutefois le crible nécessite d'allouer un tableau de booléens de taille ~`MAX_N`, donc surveillez la mémoire disponible.

**Modifier `n`**

- Pour tester rapidement, changez `n` à une valeur plus petite (par ex. `1000` ou `10000`) dans le script choisi avant de lancer.
