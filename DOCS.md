# `Spellbook Commands`

**Usage**:

```console
$ Spellbook Commands [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `update-db`: Update the local MTG card database.
* `search`: Search the collection for a card by name.
* `log`: List the log files for the collection.
* `backups`: List backup files.
* `restore`: Restore your collection from a backup file.
* `add`: Add cards to a collection.
* `remove`: Remove cards from a collection.

## `Spellbook Commands update-db`

Update the local MTG card database. This is used for spellchecking your cards among other things.
It is automatically updated if the current database file is older than 30 days.

**Usage**:

```console
$ Spellbook Commands update-db [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `Spellbook Commands search`

Search the collection for a card by name.

**Usage**:

```console
$ Spellbook Commands search [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--collection TEXT`: [default: default]
* `--help`: Show this message and exit.

## `Spellbook Commands log`

List the log files for the collection.
These files track cards you&#x27;ve added or removed.

**Usage**:

```console
$ Spellbook Commands log [OPTIONS]
```

**Options**:

* `--collection TEXT`: [default: default]
* `--help`: Show this message and exit.

## `Spellbook Commands backups`

List backup files.
These files are created right before you add or remove cards.

**Usage**:

```console
$ Spellbook Commands backups [OPTIONS]
```

**Options**:

* `--collection TEXT`: [default: default]
* `--help`: Show this message and exit.

## `Spellbook Commands restore`

Restore your collection from a backup file.

**Usage**:

```console
$ Spellbook Commands restore [OPTIONS] BACKUP
```

**Arguments**:

* `BACKUP`: [required]

**Options**:

* `--collection TEXT`: [default: default]
* `--help`: Show this message and exit.

## `Spellbook Commands add`

Add cards to a collection.
You can specify a single card by name, or a path to a text file containing a list of cards.

**Usage**:

```console
$ Spellbook Commands add [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--collection TEXT`: [default: default]
* `--help`: Show this message and exit.

## `Spellbook Commands remove`

Remove cards from a collection.
You can specify a single card by name, or a path to a text file containing a list of cards.

**Usage**:

```console
$ Spellbook Commands remove [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--collection TEXT`: [default: default]
* `--help`: Show this message and exit.
