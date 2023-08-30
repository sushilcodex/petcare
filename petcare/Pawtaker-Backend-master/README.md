
# Petcare

Backend APIs for Petcare


## Installation

Install dependencies

```bash  
  sudo apt install python3.10-dev python3.10-venv python3.10-pip
```
## Run Locally

Clone the project

```bash
  git clone https://github.com/sparkbrains/SparkPet-Backend.git
```

Go to the project directory

```bash
  cd SparkPet-Backend
```

Edit Environment file

```
   Create new .env file and include the variables which are in petcarte-env.sample file
```

Create Virtual Environment

```bash
  source env/bin/activate
```

Start the server (Make sure your 8000 port is open)

```bash
  make runserver
```


## Before Making Commit

Reformating the Code:

```bash
  make reformat
```