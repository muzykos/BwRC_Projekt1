# BwRC_Projekt1
Biometria w rozpoznawaniu człowieka
Projekt numer #1 – analiza jakości danych
• Państwa celem jest skonstruowanie dwóch zbiorów danych. Pierwszego, który będzie składał
się z szybkości pisania na klawiaturze (przynajmniej 15 osób, z których każda musi przedłożyć
niemniej niż 5 próbek), a także drugiego, który będzie składał się ze zdjęć twarzy (analogicznie
15 osób, każda powinna zostać zaprezentowana z użyciem 5 zdjęć).
• W przypadku tego zadania, nie wolno korzystać ze zbiorów danych, które znajdują się w
bazach internetowych (np. Kaggle) – celem jest bowiem samodzielne zebranie danych.
• Następnie należy przygotować implementację procedur, które pozwolą na ocenę jakości
danych.

Projekt numer #1 – analiza jakości danych
• W przypadku szybkości pisania na klawiaturze, należy zbadać następujące informacje:
• Jak bardzo podobne są do siebie próbki różnych osób (tj. sprawdzić odległości pomiędzy próbkami
różnych osób, np. odległość Euklidesa oraz Czebyszewa)?
• Które litery są najbardziej istotne z punktu widzenia rozróżnialności poszczególnych osób (proszę
skorzystać na przykład z algorytmu PCA – Principal Component Analysis)?
• Korzystając z algorytmu k-Means proszę zweryfikować (przy założeniu k=15) czy utworzone podzbiory
będą jednolite (tj. czy ten algorytm sklasyfikuje próbki jednej osoby do tego samego zbioru czy też
zostaną one “rozrzucone” pomiędzy zbiorami).

Projekt numer #1 – analiza jakości danych
• W odniesieniu do zdjęć twarzy należy zweryfikować następujące elementy:
• Ilość szumu (proszę znaleźć algorytm, który pozwoli to ocenić), a następnie należy wyrazić tą wartość
procentowo (w stosunku do obrazu jako całości)
• Korzystając z metody BRISQUE (artykuł na platformie CEZ) należy ocenić jakość zdjęcia w sposób
zautomatyzowany
• Korzystając z gotowych metod segmentacji, proszę spróbować odseparować tło od obrazu twarzy, a
następnie porównać wyniki z oznaczeniami ręcznymi (proszę zbadać metryki IoU, a także Dice’a)
