## Telepítés
Visual Studio Code-ban lent Python mellett a verziónál (pl ```3.13.2```) create new virtual environment, majd ki kell választani a ```requirements.txt```-t és megvárni még elkészül a virtual env.
## Futtatás
Terminálban:

```fastapi dev```

## Adatbázis
A ```database.py``` fileban a ``DB_NAME`` felülírása szükséges az újonan elkészített/feltöltött adatbázis nevére

## Modellek

A ```models``` mappában lévő Python fileokban olyan Python osztályokat kell létrehozni, amik az adatbázis SQL tábláinak felelnek meg.

## Keresés és csere
Gyorsbillentyű Ctrl F aztán Ctrl H
Fontos hogy az Aa szimbólum ki legyen választva, hogy kis-nagy betűs pontossággal cserélje ki a beírt szövegeket.

A kicsi ``content`` és a nagy ``Content`` cserésje fontos az elkészített új osztály nevére kis és nagy betűs variánsban.

A ``routers`` mappában a Python file ``APIRouter`` egyedében a ``prefix="/contents"``-nél az idézőjel tartalmát kell kicserélni a feladatban meghatározottra (pl.: ``prefix="/api/ingatlan"``). 
