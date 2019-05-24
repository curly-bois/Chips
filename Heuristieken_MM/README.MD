# Chips & Circuits
<img align="left" width="425" height="300" src="http://heuristieken.nl/wiki/images/7/77/Print1.gif">

<img align="right" width="425" height="400" src="http://heuristieken.nl/wiki/images/1/1d/Print2.gif">



Print #1 and Print #2 are arrangements of gates on a base, and all it takes is to wire the appropriate gates together. There are three net lists (in txt-format) for each print. Each net list needs to be implemented. Nets can only follow the grid, only one wire per segment, and one step costs 1 unit length. Nets that are aligned among the same grid line are said to be in collision. If there is one collision in one arrangement, the circuit cannot be used. Nets can also go up and down to lower and higher layers, also at the cost of 1 per level. The assignment is to implement all nets in all netlists at minimum cost.

## Aan de slag (Getting Started)

### Vereisten (Prerequisites)

Deze codebase is volledig geschreven in [Python3.6.3](https://www.python.org/downloads/). In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```
pip install -r requirements.txt
```

### Structuur (Structure)

alle scripts staan in de main folder. in de map Classes zitten alle scripts die classes aanmaken, de map options bevat scripts voor de te gebruiken input (de netlists en  de gridpoints).

De map data bevat alle code die waardes omzet naar data samen met de data zelf.


### Test (Testing)

Om de code te draaien met de standaardconfiguratie gebruik de instructie:

```
python main.py
```

## Auteurs (Authors)

* Floris Fok
* Max Frings
* Mels van Eck

## Dankwoord (Acknowledgments)

* StackOverflow
* minor programmeren van de UvA
