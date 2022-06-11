# Isolation Bot

This Delta Chat bot is the target of a recipient filter; the idea is to block
all outgoing mails in a mail server by directing it to this bot. It
auto-replies to all those mails with an error message.

## Usage

```
isolationbot --email noreply@example.org --password p4$$w0rd /tmp/noreplydb
```

