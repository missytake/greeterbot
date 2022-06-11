# Isolation Bot

This Delta Chat bot is the target of a recipient filter; the idea is to block
all outgoing mails in a mail server by directing it to this bot. It
auto-replies to all those mails with an error message.

## Setup

```
git clone https://github.com/missytake/isolationbot
cd isolationbot
python3 -m venv venv
. venv/bin/activate
pip install .
```

## Usage

```
isolationbot --email noreply@example.org --password p4$$w0rd /tmp/noreplydb
```

