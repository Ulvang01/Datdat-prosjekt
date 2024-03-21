# Datdat-prosjekt

Prosjekt i TDT4145 Datamodellering og databasesysteme

## How to run program

If you have python installed and th requirements defined in requirements.txt

- Run proggrom with `python3 main.py`
- Then type `help` to get avabile commands

Else this projects comes with a devcontainer that can be deployed to run the program without a issue

## Commands for each userstory

- Userstory 1: - use command:
  - `verify`, this creates and verifies that the database has the information given
- Userstory 2: - use command:
  - `verify`, this will also create and verify the tickets in the database
- Userstory 3: - use command:
  - `makeCustomerProfile <name>, <phone number>, <address>`, this will create a new customerprofile
  - `getFreeSeats <name of play>, <yyyy-mm-dd>`, this will provide the a list of all rows, and available seats on the given row
  - `purchaseTickets <name of play>, <yyyy-mm-dd>, <row>, <area>, <amount>, <customer name>, <ticket type>`, this will purchase x amount of tickets on a given row
- Userstory 4: - use command:
  - `getPlaysByDate <yyyy-mm-dd>`, this will provide all the plays on a given day, and the amount of sold tickets
- Userstory 5: - use command:
  - `getActorsByPlay <name>`, this will provide all the actors and their roles for a given play
- Userstory 6: - use command:
  - `getBestsellingScreening`, this gets the screening with most sold ticekts
    and displays the plays name with the screenings date and number of sold tickets
- Userstory 7: - use command:
  - `getActorConnections <name>`, this will provide all connections an actor has played with, and in what play it happend

## Outputs for each userstory

- Userstory 1 and 2:
  - `verify` will output all the operations its on when verifying
- Userstory 3:

  - `makeCustomerProfile Simon, 44444444, apegata 2` will output

    ```md
    Customer by name Ola Nordmann added to database
    ```

  - `getFreeSeats Kongsemnene, 2024-02-03` will output:

    ```md
    Galleri
    Row: 4 Free Seats: 5
    Row: 3 Free Seats: 5
    Row: 2 Free Seats: 5
    Row: 1 Free Seats: 5
    Parkett
    Row: 18 Free Seats: 24
    Row: 17 Free Seats: 24
    Row: 16 Free Seats: 27
    Row: 15 Free Seats: 24
    Row: 14 Free Seats: 27
    Row: 13 Free Seats: 24
    Row: 12 Free Seats: 28
    Row: 11 Free Seats: 28
    Row: 10 Free Seats: 28
    Row: 9 Free Seats: 28
    Row: 8 Free Seats: 28
    Row: 7 Free Seats: 26
    Row: 6 Free Seats: 26
    Row: 5 Free Seats: 26
    Row: 4 Free Seats: 26
    Row: 3 Free Seats: 18
    Row: 2 Free Seats: 9
    Row: 1 Free Seats: 10
    ```

  - `purchaseTickets Kongsemnene, <yyyy-mm-dd>, <row>, <area>, <amount>, <customer name>, <ticket type>` will output:

    ```md
    Price: 4050
    ```

  - `getPlaysByDate 2024-02-03` will output:

    ```md
    Dato: 2024-02-03, Kongsemnene, Solgte billetter=74
    ```

  - `getActorsByPlay Kongsemnene` will output:

    ```md
    Output her
    ```

  - `getBestsellingScreening` will output:

    ```md

    ```

## Database Changes

Description of the changed done with the database from DB delivery 1

- The `stilling` (position) field has been removed as it was found to overlap significantly with `oppgaver` (tasks).
- The description field for tasks has been removed, as we were unable to gather sufficient information about each task to create meaningful descriptions.

Sure, here's the translation ready for your Markdown (.md) file:

## Assumptions

Assumptions made when creating functions and data for the database

- If there is a discrepancy between the list of roles in the task description and the website, the roles from the website are used. Additionally, if there are roles on the website that are not mentioned in the task description, they are included only in the first act.
- The responsible director of the theater is stored as a `<fine solution>`.
- All participants are assumed to be full-time employees, as there is no information stating otherwise.
- The database only contains tasks listed on the website, and these are standardized. For example, "Music release from the subjects" is changed to follow "Musical Responsibility."

## Creators

Christoffer Ulvang Thorvaldsen
Simon Bjerkås
Idar Buer
