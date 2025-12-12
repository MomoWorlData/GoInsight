# GoInsight

[![Partner Tenuki](https://img.shields.io/badge/Partner-Tenuki-orange)](https://tenuki-brest.jeudego.org)
[![Partner IMT Atlantique](https://img.shields.io/badge/Partner-IMT_Atlantique-blue)](https://www.imt-atlantique.fr/en)
[![Website KataGo](https://img.shields.io/badge/Website-KataGo-green)](https://katagotraining.org)
[![GitHub KataGo](https://img.shields.io/badge/Github-KataGo-black)](https://github.com/lightvector/KataGo)
[![License MIT](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/license/MIT)

<table>
  <tr>
    <td width="150">
      <img src="assets/GoInsight_logo.png" alt="Logo" width="250"/>
    </td>
    <td>
      <p>GoInsight is a tool to help Go player analyse their games. It uses a fine-tuned version of <b>KataGo</b>, alongside various pre and post-processings steps to provide a user-friendly feedbacks on Go games. This project is the result of the collaboration between <b>Tenuki</b> and <b>IMT Atlantique</b>.</p>
    </td>
  </tr>
</table>

## Features

- `Better move highlights`.
- `Blunder and mistake highlights`.
- `Important square highlight` to help the player understand the engine choice.
- `Ignorable area` to be able to study a specific area of the game.

## Installation

This project requires Python `3.7` or higher. Please ensure Python `3.7+` is installed and available on your `PATH` before running the setup.

### Unix (Linux/MacOS)

First, open a terminal in the directory you'd like to clone the project in.

```bash
# Clone the repo
git clone https://github.com/leobeaumont/GoInsight.git
cd GoInsight
```
```bash
# Setup the environement
make setup
```
```bash
# Activate the virtual environment
source .venv/bin/activate
```
```bash
# Download KataGo model
make get-model
```

You're all setup !

### Windows

First, open PowerShell in the directory where you'd like to clone the project.

```powershell
# Clone the repo
git clone https://github.com/leobeaumont/GoInsight.git
cd ./GoInsight/
```
```powershell
# Allow PowerShell scripts to run (first time only)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
```powershell
# Setup the environment
.\make.ps1 setup
```
```powershell
# Activate the virtual environment
.\.venv\Scripts\Activate.ps1
```
```Powershell
# Download KataGo model
.\make.ps1 get-model
```

## Commands

### Run KataGo in terminal

This start an instance of KataGo, type gtp commands to interact with it.
- Use `quit` command to close the instance
- Use `list_commands` to get a list of all the commands

#### Unix (Linux/MacOs)

```bash
make run-model
```
#### Windows

```Powershell
.\make.ps1 run-model
```

### Optimise KataGo for your device (optional)

Start a batch of tests to find the best parameters (This will take a few minutes)

#### Unix (Linux/MacOS)

```bash
make opt-model
```
#### Windows

```Powershell
.\make.ps1 opt-model
```

### Tests

This will run all tests declared in the tests directory

#### Unix (Linux/MacOS)

```bash
make tests
```

#### Windows

```powershell
.\make.ps1 tests
```

### Documentation

This will open the project's documentation on your default web browser

#### Unix (Linux/MacOS)

```bash
make docs
```

#### Windows

```powershell
.\make.ps1 docs
```

### Clean project

Remove setup files and the virtual environment from the project

#### Unix (Linux/MacOS)

```bash
make clean
```

#### Windows

```powershell
.\make.ps1 clean
```

## Using GoInsight as an API

TO DO

### Setup

TO DO

### Usage

TO DO

## Contributing

Contributions are not welcome yet, as this project is part of students cursus a `IMT Atltantique`. The project will be opened to contributors after the course ended.

## Acknowledgements

### Structures

- `Tenuki` Brest Go association.
- `IMT Atlantique` engineering school.
- `KataGo` open ource Go engine.

### Supervisors and clients

- Coppin Gilles
- Le Hir Mathieu
- Peillard Étienne

### Project members

- Beaumont Léo (leo.beaumont@imt-atlantique.net)
- Chambriard Léopold (leopold.chambriard@imt-atlantique.net)
- Chouki Mouad (mouad.chouki@imt-atlantique.net)
- Disdier Jordan (jordan.disdier@imt-atlantique.net)
- Garrana Simon (simon.garrana@imt-atlantique.net)
- Miranda-Gonzales Marcelo (marcelo.miranda-gonzales@imt-atlantique.net)
- Roubertou Amaury (amaury.roubertou@imt-atlantique.net)

## Contacts

For any questions or supports, please contact leo.beaumont@imt-atlantique.net.