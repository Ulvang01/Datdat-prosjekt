# Datdat-prosjekt
Prosjekt i TDT4145 Datamodellering og databasesysteme

## How to run program:
If you have python installed and th requirements defined in requirements.txt
 - Run proggrom with `python3 main.py`
 - Then type `help` to get avabile commands

Else this projects comes with a devcontainer that can be deployed to run the program without a issue

## Commands for each userstory
 - Userstory 1:
    - use command: `verify`, this creates and verifies that the database has the information given
 - Userstory 2:
    - use command: 
 - Userstory 3:
    - use command: 
 - Userstory 4:
    - use command: 
 - Userstory 5:
    - use command: `getBestsellingScreening`, this gets the screening with most sold ticekts
    and displays the plays name with the screenings date and number of sold tickets
 - Userstory 6:
    - use command: 
 - Userstory 7:
    - use command: 

## Outputs for each userstory:


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