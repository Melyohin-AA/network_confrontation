<div align="center">
  <h2 align="center">Network Confrontation</h2>
  <p align="center">Multiplayer turn-based strategy game</p>
</div>


### About the project

The product consists of a client-server application where the gameplay is implemented, and a website designed for interaction between players both during game sessions and in other time.

The project was developed by a small team of developers as part of the program development course.

#### Features:
Product features:
* The website:
  * player accounts;
  * player belongs to one of three different factions;
  * player's profile;
  * ranking players by their experience;
  * option to create new game session and set it up;
  * search of game sessions which are available for joining in;
  * option to join in a game session;
  * in-game store;
  * faction pages with faction's description and players' rating list;
* The gameplay:
  * 3 teams;
  * teams have their budget that is local for a game session;
  * players do their moves by turns;
  * time to do moves in each turn is limited;
  * hexagonal grid as the game field;
  * different types of grid tiles;
  * option to upgrade grid tiles and develop them in different ways;
  * accumulation of power points at a grid tile;
  * option to move power points between grid tiles;
  * capturing/defending of grid tiles with power points;
  * different effects that may be applied to grid tiles;
  * different "hack tools" which cause grid tile effects;
  * "hack tools" may be purchased at in-game store;
  * loss of all capital tiles causes the team's defeat;
  * the last remaining team wins;
  * players of the winning team gain experience;
* Target OS – Linux, Windows 10

#### Technology stack:
* `Python 3.10`
* `Django 3.1.4`
* `SQLite 3.22`
* `PyGame 2.1.2`
* `Sphinx 5.1.1`


### Usage

#### Project setting up:
1. Clone the repository
    ```sh
    git clone https://github.com/Melyohin-AA/network_confrontation.git
    ```
2. Change directory to `project`
3. Initialize the project by running `init.bat` script (for Windows) or `init.sh` script (for Linux)

#### Starting server:
1. Activate the virtual environment
2. Change directory to `src/web`
3. Run server
    ```sh
    manage.py runserver --insecure
    ```

#### Starting client:
1. Activate the virtual environment
2. Change directory to `src/desktop`
3. Run client
    ```sh
    python run.py
    ```

#### Compilation of developer documentation:
1. Activate the virtual environment
2. Change directory to `docs`
3. Compile documentation by running `make` script:
   * for Linux
   ```sh
   make html
   ```
   * for Windows
   ```sh
   make.bat html
   ```


### Documentation

User documentation: `docs/ДокументацияПользователя.pptx`.

Developer documentation: `docs/build/html/index.html`.


### Demo

Youtube video:<br>
[![Demo](https://img.youtube.com/vi/K3yNlMb3IwM/0.jpg)](https://youtu.be/K3yNlMb3IwM)
