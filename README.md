# Datdat-prosjekt

Prosjekt i TDT4145 Datamodellering og databasesysteme

## How to run program

If you have python installed and the requirements defined in [requirements.txt](./requirements.txt)

- Run program with `python3 main.py`
- Then type `help` to get avabile commands

Else this projects comes with a devcontainer that can be deployed to run the program without an issue
Make sure to open a terminal and move to this directory.

- run `npm install -g @devcontainers/cli`
- then run `devcontainer up --workspace-folder .`
- then run `devcontainer exec --workspace-folder . python3 main.py`

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

  - `verify` will output all the operations its on when verifying:

    ```md
    Creating table Scene...
    Creating table Area...
    Creating table Row...
    Creating table Chair...
    Creating table Play...
    Creating table Screening...
    Creating table CustomerProfile...
    Creating table TicketPurchase...
    Creating table TicketPrice...
    Creating table Ticket...
    Creating table Actor...
    Creating table Role...
    Creating table ActorRoleJunction...
    Creating table Act...
    Creating table RoleActJunction...
    Creating table Contributor...
    Creating table EmployeeStatus...
    Creating table Task...
    Creating table TaskContributorJunction...
    Added tables: Scene, Area, Row, Chair, Play, Screening, CustomerProfile, TicketPurchase, TicketPrice, Ticket, Actor, Role, ActorRoleJunction, Act, RoleActJunction, Contributor, EmployeeStatus, Task, TaskContributorJunction
    Reading Scene(name=Hovedscene)...
    Scene(name=Hovedscene) verified.
    Reading Scene(name=Gamle-scene)...
    Scene(name=Gamle-scene) verified.
    Verifying Kongsemnene...
    Scene(name=Hovedscene) 'Hovedscene'
    Verifying screenings...
    Verifying ticketprices...
    Verifying actors...
    Verifying acts...
    Verifying Størst av alt er kjærligheten...
    Scene(name=Gamle-scene) 'Gamle-scene'
    Verifying screenings...
    Verifying ticketprices...
    Verifying actors...
    Verifying acts...
    Reading contributors...
    Done verifying employee statuses...
    Reading contributors...
    Verifying contributors...
    Størst av alt er kjærligheten
    Verifying contributors...
    Størst av alt er kjærligheten
    Størst av alt er kjærligheten
    Verifying contributors...
    Størst av alt er kjærligheten
    Verifying contributors...
    Størst av alt er kjærligheten
    Verifying contributors...
    Størst av alt er kjærligheten
    Verifying contributors...
    Kongsemnene
    Kongsemnene
    Verifying contributors...
    Kongsemnene
    Kongsemnene
    Verifying contributors...
    Kongsemnene
    Verifying contributors...
    Kongsemnene
    Done verifying contributors...
    Adding dummy user...
    Verifying tickets...
    ```

- Userstory 3:

  - `makeCustomerProfile Ola Nordmann, 44444444, Munkegata 28` will output

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

  - `purchaseTickets Kongsemnene, 2024-02-03, 9, Parkett, 9, Ola Nordmann, Ordinær` will output:

    ```md
    2024-02-03
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
    Best selling screening is: Kongsemnene at 2024-02-03 .
    And it has sold: 74 tickets.
    ```

  - `getActorConnections Sunniva Du Mond Nordal` will output:

    ```md
    Skuespiller Sunniva Du Mond Nordal har spilt sammen med Jo Saberniak i stykket Størst av alt er kjærligheten
    Skuespiller Sunniva Du Mond Nordal har spilt sammen med Marte M. Steinholt i stykket Størst av alt er kjærligheten
    Skuespiller Sunniva Du Mond Nordal har spilt sammen med Tor Ivar Hagen i stykket Størst av alt er kjærligheten
    Skuespiller Sunniva Du Mond Nordal har spilt sammen med Trond-Ove Skrødal i stykket Størst av alt er kjærligheten
    Skuespiller Sunniva Du Mond Nordal har spilt sammen med Natalie Grøndahl Tangen i stykket Størst av alt er kjærligheten
    Skuespiller Sunniva Du Mond Nordal har spilt sammen med Åsmund Flaten i stykket Størst av alt er kjærligheten
    ```

## Database Changes

Description of the changes done with the database from DB delivery 1

- The `stilling` (position) field has been removed as it was found to overlap significantly with `oppgaver` (tasks).
- The description field for tasks has been removed, as we were unable to gather sufficient information about each task to create meaningful descriptions.

## Assumptions

Assumptions made when creating functions and data for the database

- If there is a discrepancy between the list of roles in the task description and the website, the roles from the website are used. Additionally, if there are roles on the website that are not mentioned in the task description, they are included only in the first act.
- All participants are assumed to be full-time employees, as there is no information stating otherwise.
- The database only contains tasks listed on the website, and these are standardized. For example, "Music release from the subjects" is changed to follow "Musical Responsibility."

## Creators

Christoffer Ulvang Thorvaldsen
Simon Bjerkås
Idar Buer
