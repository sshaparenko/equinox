# Equinox CLI

Equinox CLI is a tool that looks for SQL injection vulnerabilities

## Where to start?

1. Clone this project to your machine using `git clone`
2. Be sure to install poetry

Official installation:

```
curl -sSL https://install.python-poetry.org | python3 -
```

Brew installation:

```
brew install poetry
```

3. Navigate to the project directory
4. Run `poetry install` to install dependencies
5. Run `poetry shell` to activate virtual environment
6. Execute `equnox --help` and you should get instructions on how to use equinox

## Usage

For now it only works with only one GET parameter. Here's an example of command used:

```
equinox http://web.com/index.php?id=1 /path/to/worlist
```

This project goes with basic wordlist called `sqli.txt` that you can use.

## Example

For this example, I used a [PortSwigger Lab](https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data) that goes with a SQLi vulnerable website

```
equinox https://0a0800f4042420be82f76a5500cc00c4.web-security-academy.net/filter?category=Gifts ./sqli.txt
```

```

___________________    ____ ___ .___  _______   ________   ____  ___
\_   _____/\_____  \  |    |   \|   | \      \  \_____  \  \   \/  /
 |    __)_  /  / \  \ |    |   /|   | /   |   \  /   |   \  \     /
 |        \/   \_/.  \|    |  / |   |/    |    \/    |    \ /     \
/_______  /\_____\ \_/|______/  |___|\____|__  /\_______  //___/\  \
        \/        \__>                       \/         \/       \_/


[13:34:08] [INFO] checking connection to the target URL
[13:34:08] [INFO] trying to inject...
[13:34:13] [INFO] parameter 'category' appears to be vulnerable to SQL injection
```
