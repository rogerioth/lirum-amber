# String Operations TUI

A terminal UI and CLI for performing 200+ string operations — case transforms, encoding/decoding, hashing, regex, JSON formatting, text statistics, and more.

Built with [Textual](https://textual.textualize.io/).

## Quick Start

```bash
# Install
pip install -e .

# Launch TUI (no arguments)
string-ops

# CLI mode — run an operation directly
string-ops sha256 -t "hello"
echo "hello world" | string-ops reverse_words
```

## CLI Mode

All 200+ operations are available from the command line. Run `string-ops --help` for the full list.

### Basic usage

```bash
# By display name
string-ops lowercase -t "Hello World"          # → hello world
string-ops "SHA-256 Hash" -t "hello"           # → 2cf24dba...

# By function name (underscored)
string-ops to_uppercase -t "Hello World"       # → HELLO WORLD
string-ops base64_encode -t "hello"            # → aGVsbG8=

# From stdin (pipe)
echo "hello world" | string-ops reverse_words  # → world hello
cat file.txt | string-ops sha256               # hash file contents

# From file
string-ops lowercase -i file.txt
```

### Extra parameters

Operations that need parameters use `-p KEY=VALUE` (repeatable):

```bash
string-ops "Caesar Cipher Encode" -t "hello" -p shift=7    # → olssv
string-ops truncate -t "hello world" -p width=5              # → he...
string-ops "Pad Left" -t "42" -p width=5 -p char=0          # → 00042
string-ops center_align -t "hello" -p width=20               # →        hello
```

### Generators (no input needed)

```bash
string-ops generate_uuid                       # → 550e8400-e29b-...
string-ops generate_password -p length=24      # → xK9#mP2...
```

### Listing operations

```bash
string-ops --list                              # all operations
string-ops --help                              # operations with parameters
```

## Key Features

- **200+ string operations** across 13 categories
- **Real-time apply**: type text, see results instantly
- **Keyboard-driven**: full arrow key navigation, no mouse needed
- **Tab navigation**: `Tab` cycles focus through categories → operations → input → output
- **Search**: `Ctrl+/` to filter operations across categories
- **File I/O**: `Ctrl+O` open, `Ctrl+S` save
- **Categories**: Transform, Encode/Decode, Hash/Digest, Statistics, JSON, Regex, Extract, and more

## Architecture

```
main.py          # Entry point (TUI + CLI routing)
cli.py           # CLI argument parser and operation runner
tui/app.py       # Textual TUI (screens, widgets, bindings)
operations_mapping.py  # 200+ operations -> categories
string_ops/      # Pure-function operation implementations
  ├── transform.py      # Case transforms, reverse, rotate
  ├── encode.py         # Base64, URL, HTML, hex, binary, etc.
  ├── format_ops.py     # Trim, wrap, pad, align, normalize
  ├── hash_ops.py       # MD, SHA, BLAKE, HMAC, bcrypt, Argon2
  ├── statistics.py     # Counts, entropy, distance metrics
  ├── extract.py        # Extract emails, URLs, IPs, hashtags
  ├── find_replace.py   # Regex find/replace, count matches
  ├── json_ops.py       # JSON/XML/SQL/CSS format, JWT
  ├── escape.py         # JSON/XML/CSV/SQL/C/Java/Python/Bash escape
  ├── misc.py           # UUID, password, lorem, Pig Latin, Atbash
  ├── rearrange.py      # Shuffle, sort chars/words/lines
  ├── manipulate.py     # Split, join, chunk, prefix/suffix
  └── ciphers.py        # Vigenère, Morse code
tests/            # pytest test suite (17 modules: 15 unit + TUI + CLI)
```

## Docs

- [Architecture](docs/architecture.md) — high-level design and data flow
- [TUI Layer](docs/tui.md) — screens, widgets, keyboard shortcuts, event flow
- [Operations](docs/operations.md) — all 200+ operations, categories, module mapping

## Requirements

- Python 3.10+
- [Textual >= 0.48.0](https://textual.textualize.io/)

## Development

```bash
pip install -e ".[dev]"
pytest tests/
```

### CLI Tests

CLI behavior is tested via subprocess calls — covers display names, function names, extra params, generators, pipe input, file input, and error handling:

```bash
pytest tests/test_cli.py -v
```

### TUI Tests

The TUI is tested headlessly using Textual's `Pilot` API — no real terminal required:

```bash
pytest tests/test_tui.py -v
```

Tests cover initial focus, `Tab` cycling through panes, arrow key category navigation, Enter execution, and widget focus isolation.
