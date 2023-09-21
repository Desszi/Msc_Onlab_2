# Msc_Onlab_2
Ez a könyvtár folytatása az Msc_Onlab_1 -nek. 

A Mondrián játékhoz készül egy generátor/szimulátor Python nyelven, amit egy már meglévő C++-ban megírt Mondrián játékgenerátor ihletett. 
Ehhez továbbiakban egy másik, Mondriánhoz hasonló játék fog tartozni, melynek játéklogikájához egy másikfajta AI megoldás fog tartozni, a Q tanulás módszere. 
Ennek a játéknek a célja hogy egymásra rakott lapokkal, ahol a színek fedik egymást egy adott pályát ki lehessen rakni, a játékelemek megfelelő sorrendben való lerakásával.

# Feladat: Mondrián szimulátor

Szabályok:
 - Az inputot a palyak nevű mappából véletlenszerűen választja, majd ehhez a pályához az elemek mappából választ egy pályához megfelelő elemkészletet.
 - Van egy elemkészletünk adott méretű pályához, nem kell az összesen felhasználni, hanem ezekből kell lerakni.
 - Stratégiát egy függvényként kell megírni, kezdetnek két stratégiát érdemes megírni, egyik ha a nagyobb elemmel kezdünk és haladunk a kisebb fele, az eggyel bonyolultabban pedig az egyszéles elemeket próbáljuk lerakni oda, ahol a legvalószínűbb hogy jó helye lesz.
 - Lépésszámnak számít ha egy elemet sikerült elhelyezni a pályán, azonban nem feltétlen egyből a jó helyére raktuk.
 - A pályát akkor raktuk ki ha teljesen sikerült lefedni a megadott elemekkel, ha nem akkor annak a pályának nincs megoldása, kikukázhatjuk.
 - Kimenetként szeretnénk látni a generált pályát és hogy azt hogy sikerült kirakni a megadott elemekből, illetve hogy ezt hány lépésből sikerült.
 - A kimenet egy csv fájl lesz, amiből a mesterséges intelligencia megtanulhatja, hogy egy pálya milyen nehézségi szintű.
