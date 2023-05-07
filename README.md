# Restaurant Manager

Aplikacja dla menadżera restauracji do zarządzania rezerwacjami i menu.

## Funkcjonalności

### Zarządzanie rezerwacjami

Dodawanie, modyfikacja, usuwanie rezerwacji. 

Do każdej rezerwacji można przypisać z góry ustalone menu, do wyboru z aktywnych menu istniejących w bazie danych. 

Rezerwację można przypisać do konkretnego stołu, o ile jest on w tym terminie wolny, aplikacja sprawdza czy stół jest zarezerwowany w podobnym czasie, domyślnie czas rezerwacji jest ustawiony na 3 godziny, jest to minimalny odstęp w jakim można przyjąć rezerwację na dany stół.

Każda rezerwacja posiada formularz, który można uzupełnić informacjami o alergiach, nietolerancjach gości lub szczególnych prośbach, np. potrzebnych krzesełek dla dzieci.

### Zarządzanie menu

Dodawanie, edycja, usuwanie dań z menu, Tworzenie ofert na ustalone menu, składających się z określonych dań, np. 3 przystawki, 3 zupy, 3 dania główne, 3 desery do wyboru przez gości. Takie menu może zostać przypisane do rezerwacji, ułatwiając organizację. 


## Wykorzystane technologie

Python, Django, Bootstrap, PostgreSQL


# Restaurant Manager

Application for a restaurant manager, helping with management of menu and reservations.

[Test the app](https://restaurantmanagementapp.herokuapp.com/)


## Functionalities

### Reservations management

Adding, modifying, removing reservations.

Each reservation can be assigned with a prepared menu, chosen from active menus in the database.

Reservation can be made for a specific table, provided said table is free at that time, the app checks for reservations around the time of the reservation. Default time is set to 3 hours, which is a minimal time difference between same table reservations.

Each reservation has a form, which can be filled with extra info, such as allergies, intolerancies or special requests, such as a baby chair needed.

### Menu management

Adding, modifying, removing dishes from a menu. Creating offers with a prepared menu, e.g. 3 starters, 3 soups, 3 main courses and 3 desserts for the guests to choose from. Such menu can be assigned to a reservation to help with the organizing.


## Technologies used

Python, Django, Bootstrap, PostgreSQL
