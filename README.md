# String Operations TUI

A terminal UI for performing 200+ string operations — case transforms, encoding/decoding, hashing, regex, JSON formatting, text statistics, and more.

Built with [Textual](https://textual.textualize.io/).

## Quick Start

```bash
# Install
pip install -e .

# Run
string-ops
# or
python main.py
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
main.py          # Entry point
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
tests/            # pytest test suite (15 modules, including TUI tests)
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

### TUI Tests

The TUI is tested headlessly using Textual's `Pilot` API — no real terminal required:

```bash
pytest tests/test_tui.py -v
```

Tests cover initial focus, `Tab` cycling through panes, arrow key category navigation, Enter execution, and widget focus isolation.
