## Telepítés
Visual Studio Code-ban lent Python mellett a verziónál (pl ```3.13.2```) create new virtual environment, majd ki kell választani a ```requirements.txt```-t és megvárni még elkészül a virtual env.
## Futtatás
Terminálban:

```fastapi dev```

## Adatbázis
A ```database.py``` fileban a ``DB_NAME`` felülírása szükséges az újonan elkészített/feltöltött adatbázis nevére

## Modellek

A ```models``` mappában lévő Python fileokban olyan Python osztályokat kell létrehozni, amik az adatbázis SQL tábláinak felelnek meg.

### Kapcsolatok

A modellek (táblák) közti kapcsolatokat speciális változókkal tudunk reprezentálni, amik a következő képpen hozhatóak létre:

1. Előfeltételek

    Az a modell, aminek a kapcsolatának eredményét egy végpontban szeretnénk látni, annak fel kell lennie osztva legalább 3 örökölt osztályra:
- OsztalyBase(SqlModel)

    összes mező kivéve kapcsolati

- Osztaly(OsztalyBase, table=True)

    kapcsolati mezők = Relationship()-el
- OszalyPublic(OsztalyBase)

    kapcsolati mezők = Relationship() NÉLKÜL
2. Létrehozás
```python
from .kapcsoltosztaly import KapcsoltOsztaly # a .kapcsoltosztaly előtt a . nagyon fontos

class Osztaly(OsztalyBase, table=True):
    kapcsolat_mezo: KapcsoltOszaly = Relationship(back_populates="osztaly_link") # fontos: a kettőspont után a másik osztály neve, a back_populates után a másik osztályban a kapcsoló változó neve  
class OsztalyPublic(OsztalyBase):
    kapcsolat_mezo: KapcsoltOsztaly
```

```python
class KapcsoltOsztaly(SqlModel, table=True):
    osztaly: "Osztaly" = Relationship(back_populates="kapcsolat_mezo") # fontos: a másik osztály neve IDÉZŐJELBEN, a back_populates a másik osztály kapcsolati mező neve
```

## Keresés és csere
Gyorsbillentyű Ctrl F aztán Ctrl H
Fontos hogy az Aa szimbólum ki legyen választva, hogy kis-nagy betűs pontossággal cserélje ki a beírt szövegeket.

A kicsi ``ingatlan`` és a nagy ``Ingatlan`` cserésje fontos az elkészített új osztály nevére kis és nagy betűs variánsban.

A ``routers`` mappában a Python file ``APIRouter`` egyedében a ``prefix="/api/ingatlan"``-nél az idézőjel tartalmát kell kicserélni a feladatban meghatározottra (pl.: ``prefix="/orszagok"``). 
