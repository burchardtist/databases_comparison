# Porównanie wydajności wybranych baz danych

## Cel

Celem jest porównanie wybranych baz danych wykorzystując podstawowe operacje:
insert, select, update na kolumnach z i bez indeksu.

Wybanymi systemami baz danych są: **MySql**, **PostgreSQL**, **SQLite**

Każda baza zbudowana jest z takich kolumn jak:
```Python
# MySql
'id': 'int PRIMARY KEY NOT NULL AUTO_INCREMENT',
'city': 'varchar(255)',
'lat': 'float(13,10)',
'lon': 'float(13,10)',
'date': 'datetime'
```

Dane są generowane losowo, lecz każda z baz posiada identyczny zestaw. Do
pomiarów wykorzystałem 3 rozmiary zestawów: 10E3, 10E4 i 10E5. Każdy pomiar
wykonałem 5 razy i wyciągnąłem z nich średnią.

## Wyniki pomiarów
[insert10e3]: src/charts/insert_1000.png
[insert10e4]: src/charts/insert_10000.png
[insert10e5]: src/charts/insert_100000.png
[insert_i10e3]: src/charts/insert_indexed_1000.png
[insert_i10e4]: src/charts/insert_indexed_10000.png
[insert_i10e5]: src/charts/insert_indexed_100000.png

[select10e3]: src/charts/select_1000.png
[select10e4]: src/charts/select_10000.png
[select10e5]: src/charts/select_100000.png
[select_i10e3]: src/charts/select_indexed_1000.png
[select_i10e4]: src/charts/select_indexed_10000.png
[select_i10e5]: src/charts/select_indexed_100000.png

[update10e3]: src/charts/update_1000.png
[update10e4]: src/charts/update_10000.png
[update10e5]: src/charts/update_100000.png
[update_i10e3]: src/charts/update_indexed_1000.png
[update_i10e4]: src/charts/update_indexed_10000.png
[update_i10e5]: src/charts/update_indexed_100000.png

#### insert
![alt text][insert10e3]
![alt text][insert_i10e3]

![alt text][insert10e4]
![alt text][insert_i10e4]

![alt text][insert10e5]
![alt text][insert_i10e5]

#### select
![alt text][select10e3]
![alt text][select_i10e3]

![alt text][select10e4]
![alt text][select_i10e4]

![alt text][select10e5]
![alt text][select_i10e5]

#### update
![alt text][update10e3]
![alt text][update_i10e3]

![alt text][update10e4]
![alt text][update_i10e4]

![alt text][update10e5]
![alt text][update_i10e5]

## Podsumowanie

### insert:

| System         | 10E3   | 10E4   | 10E5   |
| ---------------|--------|--------|--------|
| **MySQL**      | 0.01s  | 0.01s  | 0.009s |
| **PostgreSQL** | 0.005s | 0.006s | 0.006s |
| **SQLite**     | 0.02s  | 0.016s | 0.016s |

ilość danych i brak indeksów nie wpływa na szybkość dodawania danych.
Stanowczo najszybszy jest PostgreSQL, a najwolniejszy SQLite.

### select:

| System         | 10E3               | 10E4               | 10E5             |
| ---------------|--------------------|--------------------|------------------|
| **MySQL**      | 0.0065s / 0.00155s | 0.030s  / 0.00255s | 0.065s / 0.0040s |
| **PostgreSQL** | 0.0075s / 0.0025s  | 0.015s  / 0.0040s  | 0.05s  / 0.0020s |
| **SQLite**     | 0.0035s / 0.0015s  | 0.0005s / 0.0025s  | 0.002s / 0.0040s |

Wybieranie danych po indeksie jest porównywalnie dobre dla każdego systemu
i jest ono natychmiastowe.

Z kolumnami bez indeksu najlepiej radzi sobie SQLite, MySQL i PostgreSQL mają
bardzo porównywalne wyniki i są one 2x gorsze od SQLite.

### update:

| System         | 10E3        | 10E4       | 10E5        |
| ---------------|-------------|------------|-------------|
| **MySQL**      | 1.6s / 0.4s | 90s / 5.5s | 8000s / 50s |
| **PostgreSQL** | 0.8s / 0.4s | 40s / 5.5s | 2500s / 50s |
| **SQLite**     | 0.8s / 0.4s | 40s / 5s   | 2500s / 45s |

Podobnie jak przy operacji select, indeksy bardzo wyrównują wyniki wszystkich
testowanych baz danych, ale także można zauważyć że ilość danych nie zmienia
szybkości aktualizacji rekordów.

Aktualizacja dla kolumn bez indeksu najszybciej działa w przypadku dwóch
systemów: PostgreSQL i SQLite. 2x słabsze wyniki uzyskuje MySQL. Dla dużej
liczby danych MySQL jest skrajnie niewydajny.

### Konkluzje

Według przeprowadzonych testów wynika, że:
  - indeksy ekstremalnie przyspieszają pracę
  - do zapisu danych najlepszy jest PostgreSQL
  - do aktualizacji PostgreSQL i SQLite
  - do wybierania danych  SQLite
  - MySQL jest zauważalnie słabszy od pozostałych
