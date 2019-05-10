# Chips & Circuits

![alt text](http://heuristieken.nl/wiki/images/7/77/Print1.gif)

Print #1 and Print #2 are arrangements of gates on a base, and all it takes is to wire the appropriate gates together. There are three net lists (in txt-format) for each print. Each net list needs to be implemented. Nets can only follow the grid, only one wire per segment, and one step costs 1 unit length. Nets that are aligned among the same grid line are said to be in collision. If there is one collision in one arrangement, the circuit cannot be used. Nets can also go up and down to lower and higher layers, also at the cost of 1 per level. The assignment is to implement all nets in all netlists at minimum cost.

## Aan de slag (Getting Started)

### Vereisten (Prerequisites)

Deze codebase is volledig geschreven in [Python3.6.3](https://www.python.org/downloads/). In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```
pip install -r requirements.txt
```

### Structuur (Structure)

In de map MM staat een werkende versie van A-algoritme samengevoegd met andere heuristieken,deze staan beschreven in de readme van deze map.


## Auteurs (Authors)

* Floris Fok
* Max Frings
* Mels van Eck

## Dankwoord (Acknowledgments)

* StackOverflow
* minor programmeren van de UvA
