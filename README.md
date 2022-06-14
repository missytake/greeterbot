# Greeter Bot

This Delta Chat bot listens for new users on a mailcow instance and writes to
them when they are created. It greets them and sends them a draw.xdc to try out
on their devices.

## Setup

```
git clone https://github.com/missytake/greeterbot
cd greeterbot
python3 -m venv venv
. venv/bin/activate
pip install .
```

## Usage

```
greeterbot --email noreply@example.org --password p4$$w0rd /tmp/noreplydb
```

