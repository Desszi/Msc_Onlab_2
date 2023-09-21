# Msc_Onlab_2
Ez a könyvtár folytatása az Msc_Onlab_1 -nek. 

A Mondrián játékhoz készül egy generátor/szimulátor Python nyelven, amit egy már meglévő C++-ban megírt Mondrián játékgenerátor ihletett. 
Ehhez továbbiakban egy másik, Mondriánhoz hasonló játék fog tartozni, melynek játéklogikájához egy másikfajta AI megoldás fog tartozni, a Q tanulás módszere. 
Ennek a játéknek a célja hogy egymásra rakott lapokkal, ahol a színek fedik egymást egy adott pályát ki lehessen rakni, a játékelemek megfelelő sorrendben való lerakásával.

# Feladat: Mondrián szimulátor

Szabályok:
 - Az inputot a palyak nevű mappából véletlenszerűen választja, majd ehhez a pályához az elemek mappából választ egy pályához megfelelő elemkészletet. Vagyis ha a pálya neve "board_7_7"-dal kezdődik, akkor a neki megfelelő elemkészlet "items_7_7".
 - Mostmár van egy elemkészletünk és egy adott méretű pályánk, ebből kell e lehető legtöbbet lerakni, amennyit csak lehet.
 - Egy lerakott elem 1 lépésnek felel meg, a lépésszámot növeljük. Lépésszámnak számít ha egy elemet sikerült elhelyezni a pályán, azonban nem feltétlen egyből a jó helyére raktuk.
 - Stratégiát egy függvényként kell megírni, kezdetnek egy stratégiát érdemes megírni, ahol sorbarakjuk az elemeket területnagyság szerint, és ilyen sorrendben rakosgatjuk le a pályára. Minden elemnek van egy betűneve a file-ban pl. d és ahova le lehet rakni a pályán ezt az elemet ott kitöltjük a betűnevével.
 - A pályát akkor raktuk ki ha teljesen sikerült lefedni a megadott elemekkel, ha nem akkor annak a pályának nincs megoldása ebben az esetben a lehető legjobb megoldást rajzoljuk ki.
 - Kimenetként szeretnénk látni a kiválasztott pályát, amivel kezdődik a játék, utána egy már kirakott pályát, illetve hogy ezt hány lépésből sikerült kirakni.
 - A kimenet egy csv fájl lesz, amiből a mesterséges intelligencia megtanulhatja, hogy egy pálya milyen nehézségi szintű.
