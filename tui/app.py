"""String Operations TUI application using textual framework."""

import sys
import os
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Static,
    Input,
    TextArea,
    DataTable,
    Button,
    DirectoryTree,
)
from textual.screen import Screen, ModalScreen
from textual import events


# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class OperationModal(ModalScreen):
    """Modal dialog for operations that need parameters."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
    ]

    def __init__(self, operation_name: str, **kwargs):
        super().__init__(**kwargs)
        self.operation_name = operation_name

    def compose(self) -> ComposeResult:
        yield Static(f"Parameter input not yet implemented for: {self.operation_name}", id="modal-message")
        yield Button("Close", id="modal-close", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "modal-close":
            self.dismiss(None)


class FileDialogScreen(ModalScreen):
    """Modal file dialog using DirectoryTree."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
    ]

    CSS = """
    FileDialogScreen {
        align: center middle;
        width: 80%;
        height: 80%;
        background: $surface;
    }

    #file-tree {
        width: 1fr;
        height: 1fr;
    }

    #dialog-title {
        width: 1fr;
        height: 1;
        content-align: center middle;
        background: $accent;
        color: $text;
    }

    #btn-open, #btn-cancel {
        width: 20%;
        height: 1;
        dock: bottom;
        margin: 1 0;
    }

    #btn-open {
        dock: left;
    }

    #btn-cancel {
        dock: right;
    }
    """

    def __init__(self, title: str = "File Dialog", on_select=None):
        super().__init__()
        self.title = title
        self.on_select = on_select

    def compose(self) -> ComposeResult:
        yield Static(self.title, id="dialog-title")
        yield DirectoryTree(".", id="file-tree")
        yield Button("Open", id="btn-open", variant="primary")
        yield Button("Cancel", id="btn-cancel", variant="default")

    def action_dismiss(self) -> None:
        self.dismiss(None)

    def on_tree_node_selected(self, event) -> None:
        data = event.node.data
        if data is not None:
            path = data.path
            if os.path.isfile(path):
                event.stop()
                self.dismiss(str(path))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancel":
            self.dismiss(None)
        elif event.button.id == "btn-open":
            tree = self.query_one("#file-tree", DirectoryTree)
            path = tree.focus_node.path if tree.focus_node else None
            if path and os.path.isfile(path):
                self.dismiss(str(path))
            elif path:
                tree.path = str(path)
            else:
                self.dismiss(None)


class NotificationScreen(ModalScreen):
    """Simple notification screen."""

    CSS = """
    NotificationScreen {
        align: center middle;
        width: 50%;
        height: auto;
        background: $surface;
    }

    #notification-text {
        width: 1fr;
        height: auto;
        padding: 1 2;
        content-align: center middle;
    }

    #notification-btn {
        width: 30%;
        height: 1;
        dock: bottom;
        margin: 1 0;
    }
    """

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Static(self.message, id="notification-text")
        yield Button("OK", id="notification-btn", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "notification-btn":
            self.dismiss()


class CategoryScreen(Screen):
    """Main screen with categories, search, input/output textviews."""

    CSS = """
    #main-container {
        layout: grid;
        grid-size: 2 1;
        grid-gutter: 1 2;
        height: 1fr;
    }

    #categories-pane {
        width: 32;
        height: 100%;
        border: solid $primary;
        padding: 0 1;
    }

    #categories-table {
        width: 100%;
        height: 100%;
    }

    #operations-pane {
        width: 1fr;
        height: 100%;
        border: solid $primary;
        padding: 0 1;
    }

    #operations-table {
        width: 100%;
        height: 100%;
    }

    #input-output-container {
        height: 10;
    }

    #text-input {
        width: 1fr;
        height: 100%;
        border: solid $primary;
    }

    #text-output {
        width: 1fr;
        height: 100%;
        border: solid $primary;
    }

    #status-bar {
        height: 1;
        width: 100%;
        background: $primary;
        color: $text;
        padding: 0 1;
    }

    #search-section {
        height: 3;
        display: none;
    }

    #search-section.visible {
        display: block;
    }

    #search-input {
        width: 100%;
    }

    #category-label, #operations-label {
        width: 100%;
        height: 1;
        background: $accent;
        color: $text;
        text-align: center;
    }

    DataTable > .datatable--cursor {
        background: #6d28d9;
    }

    DataTable > .datatable--cursor:hover {
        background: #7c3aed;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+o", "open_file", "Open File"),
        Binding("ctrl+s", "save_output", "Save Output"),
        Binding("ctrl+/", "toggle_search", "Search"),
        Binding("tab", "focus_next", "Switch Pane"),
        Binding("enter", "execute_operation", "Execute", show=False),
    ]

    _current_category = None
    _current_operation = None
    _search_visible = False
    _search_query = ""

    def compose(self) -> ComposeResult:
        with Container(id="search-section"):
            yield Input(placeholder="Search operations...", id="search-input")
        with Container(id="main-container"):
            with Vertical(id="categories-pane"):
                yield Static("CATEGORIES", id="category-label")
                yield DataTable(id="categories-table")
            with Vertical(id="operations-pane"):
                yield Static("OPERATIONS", id="operations-label")
                yield DataTable(id="operations-table")
        with Horizontal(id="input-output-container"):
            yield TextArea(id="text-input")
            yield TextArea(id="text-output")
        yield Static("", id="status-bar")

    def on_mount(self) -> None:
        from operations_mapping import OPERATIONS
        self._operations = OPERATIONS
        self._operation_map = {}
        for ops in OPERATIONS.values():
            for display_name, func_name in ops:
                self._operation_map[display_name] = func_name

        cat_table = self.query_one("#categories-table", DataTable)
        cat_table.add_columns("Category")
        cat_table.cursor_type = "row"
        for category in self._operations.keys():
            cat_table.add_row(category)
        cat_table.move_cursor(row=0)

        op_table = self.query_one("#operations-table", DataTable)
        op_table.add_columns("Operation", "Description")
        op_table.cursor_type = "row"

        self._current_category = cat_table.get_row_at(0)[0]
        self._populate_operations_table()
        self._update_status()

        cat_table.focus()

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.data_table.id == "categories-table":
            self._set_category_from_table(event.data_table)
        elif event.data_table.id == "operations-table":
            if event.data_table.row_count > 0 and event.data_table.cursor_row < event.data_table.row_count:
                row_data = event.data_table.get_row_at(event.data_table.cursor_row)
                self._current_operation = row_data[0]
                self._update_status()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id == "operations-table":
            self.action_execute_operation()

    def _set_category_from_table(self, table: DataTable) -> None:
        """Set current category from table selection."""
        if table.row_count > 0:
            row_data = table.get_row_at(table.cursor_row)
            selected_category = row_data[0]
            if selected_category != self._current_category:
                self._current_category = selected_category
                self._update_category_label()
                self._populate_operations_table()
                self._update_status()

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle real-time text input changes."""
        if event.text_area.id != "text-input":
            return
        if not self._current_operation:
            return
        func_name = self._operation_map.get(self._current_operation)
        if not func_name:
            return
        input_text = event.text_area.text
        result = self._run_operation(func_name, input_text)
        if result is not None:
            output_area = self.query_one("#text-output", TextArea)
            # Avoid cursor jump by only updating if different
            if output_area.text != str(result):
                output_area.text = str(result)
            self._update_status()

    def _update_category_label(self) -> None:
        label = self.query_one("#operations-label", Static)
        if self._current_category:
            label.update(f"[bold]{self._current_category}[/bold] OPERATIONS")
        else:
            label.update("OPERATIONS")

    def _get_operation_description(self, name: str) -> str:
        descriptions = {
            "Lowercase": "Convert all chars to lowercase",
            "Uppercase": "Convert all chars to uppercase",
            "Title Case": "Capitalize first letter of each word",
            "Camel Case": "Convert to camelCase",
            "Pascal Case": "Convert to PascalCase",
            "Snake Case": "Convert to snake_case",
            "Kebab Case": "Convert to kebab-case",
            "Constant Case": "Convert to CONSTANT_CASE",
            "Dot Case": "Convert to dot.case",
            "Path Case": "Convert to path/case",
            "Sentence Case": "Capitalize first letter of each sentence",
            "Swap Case": "Swap uppercase <-> lowercase",
            "Alternating Case": "aLtErNaTiNg CaSe",
            "Sponge Case": "sPoNgE cAsE",
            "Capitalize First Letter": "Capitalize first letter only",
            "Decapitalize First Letter": "Lowercase first letter only",
            "Reverse String": "Reverse the entire string",
            "Reverse Words": "Reverse word order",
            "Reverse Lines": "Reverse line order",
            "Shuffle Characters": "Randomly shuffle characters",
            "Shuffle Words": "Randomly shuffle words",
            "Shuffle Lines": "Randomly shuffle lines",
            "Sort Characters (Ascending)": "Sort chars A-Z",
            "Sort Characters (Descending)": "Sort chars Z-A",
            "Sort Words (Ascending)": "Sort words A-Z",
            "Sort Words (Descending)": "Sort words Z-A",
            "Sort Lines (Ascending)": "Sort lines A-Z",
            "Sort Lines (Descending)": "Sort lines Z-A",
            "Sort Lines by Length": "Sort lines shortest to longest",
            "Trim": "Strip leading/trailing whitespace",
            "Trim Left (Ltrim)": "Strip leading whitespace",
            "Trim Right (Rtrim)": "Strip trailing whitespace",
            "Remove Extra Spaces": "Collapse multiple spaces to one",
            "Remove All Whitespace": "Strip all whitespace chars",
            "Remove Empty Lines": "Remove blank lines",
            "Remove Duplicate Lines": "Remove duplicate lines",
            "Remove Duplicate Words": "Remove duplicate words",
            "Pad Left": "Pad string to length on left",
            "Pad Right": "Pad string to length on right",
            "Center Align": "Center-align text",
            "Left Align": "Left-align text",
            "Right Align": "Right-align text",
            "Justify": "Justify paragraph text",
            "Spaces to Tabs": "Convert spaces to tabs",
            "Tabs to Spaces": "Convert tabs to spaces",
            "Expand Tabs": "Expand tab characters",
            "Wrap Text": "Wrap text to specified width",
            "Normalize Newlines (CRLF to LF)": "Convert CRLF to LF",
            "Normalize Newlines (LF to CRLF)": "Convert LF to CRLF",
            "Normalize Newlines (CR to LF)": "Convert CR to LF",
            "Base64 Encode": "Encode to Base64",
            "Base64 Decode": "Decode from Base64",
            "Base64url Encode": "Encode to URL-safe Base64",
            "Base64url Decode": "Decode from URL-safe Base64",
            "URL Encode": "Percent-encode for URLs",
            "URL Decode": "Percent-decode from URLs",
            "HTML Entity Encode": "Encode to HTML entities",
            "HTML Entity Decode": "Decode from HTML entities",
            "Hex Encode": "Encode to hex string",
            "Hex Decode": "Decode from hex string",
            "Binary Encode": "Encode to binary",
            "Binary Decode": "Decode from binary",
            "Octal Encode": "Encode to octal",
            "Octal Decode": "Decode from octal",
            "Base32 Encode": "Encode to Base32",
            "Base32 Decode": "Decode from Base32",
            "Base58 Encode": "Encode to Base58",
            "Base58 Decode": "Decode from Base58",
            "Base85/Ascii85 Encode": "Encode to Base85/Ascii85",
            "Base85/Ascii85 Decode": "Decode from Base85/Ascii85",
            "Punycode Encode": "Encode to Punycode",
            "Punycode Decode": "Decode from Punycode",
            "Quoted-Printable Encode": "Encode to Quoted-Printable",
            "Quoted-Printable Decode": "Decode from Quoted-Printable",
            "ROT13": "Apply ROT13 cipher",
            "ROT47": "Apply ROT47 cipher",
            "Atbash Cipher": "Apply Atbash cipher",
            "Caesar Cipher Encode": "Apply Caesar cipher",
            "Caesar Cipher Decode": "Decode Caesar cipher",
            "Vigenère Cipher Encode": "Apply Vigenère cipher",
            "Vigenère Cipher Decode": "Decode Vigenère cipher",
            "Morse Code Encode": "Encode to Morse code",
            "Morse Code Decode": "Decode from Morse code",
            "MD2 Hash": "MD2 hash digest",
            "MD4 Hash": "MD4 hash digest",
            "MD5 Hash": "MD5 hash digest",
            "SHA-1 Hash": "SHA-1 hash digest",
            "SHA-224 Hash": "SHA-224 hash digest",
            "SHA-256 Hash": "SHA-256 hash digest",
            "SHA-384 Hash": "SHA-384 hash digest",
            "SHA-512 Hash": "SHA-512 hash digest",
            "SHA-512/224 Hash": "SHA-512/224 hash digest",
            "SHA-512/256 Hash": "SHA-512/256 hash digest",
            "SHA-3-224 Hash": "SHA-3-224 hash digest",
            "SHA-3-256 Hash": "SHA-3-256 hash digest",
            "SHA-3-384 Hash": "SHA-3-384 hash digest",
            "SHA-3-512 Hash": "SHA-3-512 hash digest",
            "Keccak-224 Hash": "Keccak-224 hash digest",
            "Keccak-256 Hash": "Keccak-256 hash digest",
            "Keccak-384 Hash": "Keccak-384 hash digest",
            "Keccak-512 Hash": "Keccak-512 hash digest",
            "Shake-128 Hash": "Shake-128 hash digest",
            "Shake-256 Hash": "Shake-256 hash digest",
            "BLAKE2b Hash": "BLAKE2b hash digest",
            "BLAKE2s Hash": "BLAKE2s hash digest",
            "BLAKE3 Hash": "BLAKE3 hash digest",
            "RIPEMD-160 Hash": "RIPEMD-160 hash digest",
            "Whirlpool Hash": "Whirlpool hash digest",
            "Tiger Hash": "Tiger hash digest",
            "CRC16": "CRC16 checksum",
            "CRC32": "CRC32 checksum",
            "Adler-32": "Adler-32 checksum",
            "FNV-1a Hash": "FNV-1a hash",
            "MurmurHash": "MurmurHash hash",
            "xxHash": "xxHash hash",
            "HMAC-MD5": "HMAC-MD5 keyed hash",
            "HMAC-SHA1": "HMAC-SHA1 keyed hash",
            "HMAC-SHA256": "HMAC-SHA256 keyed hash",
            "HMAC-SHA512": "HMAC-SHA512 keyed hash",
            "Bcrypt Hash": "Bcrypt password hash",
            "Scrypt Hash": "Scrypt password hash",
            "Argon2 Hash": "Argon2 password hash",
            "PBKDF2 Hash": "PBKDF2 key derivation",
            "JSON Escape": "Escape for JSON string",
            "JSON Unescape": "Unescape JSON string",
            "XML Escape": "Escape for XML",
            "XML Unescape": "Unescape XML",
            "CSV Escape": "Escape for CSV",
            "CSV Unescape": "Unescape CSV",
            "SQL Escape": "Escape for SQL string",
            "Regex Escape": "Escape for regex pattern",
            "C String Escape": "Escape for C string",
            "C String Unescape": "Unescape C string",
            "Java String Escape": "Escape for Java string",
            "Java String Unescape": "Unescape Java string",
            "Python String Escape": "Escape for Python string",
            "Python String Unescape": "Unescape Python string",
            "Bash Escape": "Escape for Bash string",
            "Prettify JSON": "Format JSON with indentation",
            "Minify JSON": "Compact JSON",
            "Prettify XML": "Format XML with indentation",
            "Minify XML": "Compact XML",
            "Prettify SQL": "Format SQL with indentation",
            "Minify SQL": "Compact SQL",
            "Prettify CSS": "Format CSS with indentation",
            "Minify CSS": "Compact CSS",
            "Parse Query String": "Parse URL query string",
            "Stringify Query String": "Build URL query string",
            "JWT Decode": "Decode JWT payload",
            "Character Count": "Count total characters",
            "Character Count (No Spaces)": "Count chars excluding spaces",
            "Word Count": "Count total words",
            "Line Count": "Count total lines",
            "Byte Size (UTF-8)": "Count UTF-8 byte size",
            "Vowel Count": "Count vowel characters",
            "Consonant Count": "Count consonant characters",
            "Entropy Calculation": "Shannon entropy",
            "Levenshtein Distance": "Edit distance",
            "Jaro-Winkler Distance": "String similarity metric",
            "Hamming Distance": "Character difference count",
            "Soundex": "Soundex phonetic code",
            "Metaphone": "Metaphone phonetic code",
            "Double Metaphone": "Double Metaphone phonetic code",
            "Is Palindrome": "Check if string is palindrome",
            "Is Anagram": "Check if two strings are anagrams",
            "Find Most Frequent Word": "Most common word",
            "Find Most Frequent Character": "Most common character",
            "Extract Emails": "Find email addresses",
            "Extract URLs": "Find URLs",
            "Extract Domains": "Extract domain names",
            "Extract IPv4 Addresses": "Find IPv4 addresses",
            "Extract IPv6 Addresses": "Find IPv6 addresses",
            "Extract MAC Addresses": "Find MAC addresses",
            "Extract Numbers": "Extract numeric values",
            "Extract Hashtags": "Extract #hashtags",
            "Extract Mentions": "Extract @mentions",
            "Strip HTML Tags": "Remove HTML tags",
            "Strip Markdown Tags": "Remove Markdown tags",
            "Strip Punctuation": "Remove punctuation",
            "Strip ANSI Escape Codes": "Remove ANSI codes",
            "Split by Comma": "Split text by comma",
            "Split by Space": "Split text by space",
            "Split by Newline": "Split text by newline",
            "Join Lines by Comma": "Join lines with comma",
            "Join Lines by Space": "Join lines with space",
            "Chunk Text": "Split into fixed-size chunks",
            "Truncate Text": "Truncate to N characters",
            "Add Prefix to Lines": "Add prefix to each line",
            "Add Suffix to Lines": "Add suffix to each line",
            "String to ASCII Array": "Convert to ASCII codes",
            "ASCII Array to String": "Convert ASCII codes to string",
            "Zalgo Text Generator": "Generate Zalgo text",
            "Leetspeak Generator": "Convert to leetspeak",
            "Upside Down Text": "Flip text upside down",
            "Vaporwave / Fullwidth Text": "Fullwidth characters",
            "Braille Translation": "Convert to Braille",
            "UUIDv4 Generator": "Generate random UUIDv4",
            "ULID Generator": "Generate random ULID",
            "NanoID Generator": "Generate random NanoID",
            "Random Password Generator": "Generate random password",
            "Lorem Ipsum Generator": "Generate Lorem Ipsum text",
            "Slugify": "Convert to URL-friendly slug",
            "Unslugify": "Restore from slug",
        }
        return descriptions.get(name, str(name))

    def _populate_operations_table(self) -> None:
        table = self.query_one("#operations-table", DataTable)
        table.clear()
        if not self._current_category:
            return
        ops = self._operations.get(self._current_category, [])
        for name, func_name in ops:
            desc = self._get_operation_description(name)
            table.add_row(name, desc)
        if table.row_count > 0:
            table.move_cursor(row=0)
            self._current_operation = table.get_row_at(0)[0]

    def _update_status(self) -> None:
        """Update the status bar."""
        status = self.query_one("#status-bar", Static)
        input_text = self.query_one("#text-input", TextArea).text
        chars = len(input_text)
        words = len(input_text.split()) if input_text.strip() else 0
        lines = len(input_text.split('\n')) if input_text else 0
        category = f"[bold]{self._current_category}[/bold]" if self._current_category else "[dim]No category[/dim]"
        operation = f" | [bold]{self._current_operation}[/bold]" if self._current_operation else ""
        status.update(
            f"[dim]Chars: {chars} | Words: {words} | Lines: {lines} | Category: {category}{operation}[/dim]"
            "  [dim]Up/Down Navigate | Real-time Apply | Ctrl+/ Search | Ctrl+O Open | Ctrl+S Save | Q Quit[/dim]"
        )

    def _on_input_text_changed(self, text: str) -> None:
        """Handle real-time text input changes."""
        if not self._current_operation:
            return
        func_name = self._operation_map.get(self._current_operation)
        if not func_name:
            return
        input_text = text
        result = self._run_operation(func_name, input_text)
        if result is not None:
            self.query_one("#text-output", TextArea).text = str(result)
            self._update_status()

    def action_execute_operation(self) -> None:
        """Execute the selected operation."""
        table = self.query_one("#operations-table", DataTable)
        if table.row_count == 0 or table.cursor_row >= table.row_count:
            return

        row_data = table.get_row_at(table.cursor_row)
        operation_name = row_data[0]
        self._current_operation = operation_name

        # Get the operation function from the map
        func_name = self._operation_map.get(operation_name)

        if not func_name:
            self.app.push_screen(OperationModal(operation_name))
            return

        # Execute the operation
        input_text = self.query_one("#text-input", TextArea).text
        result = self._run_operation(func_name, input_text)

        if result is not None:
            self.query_one("#text-output", TextArea).text = str(result)
            self._update_status()
        else:
            self.app.push_screen(NotificationScreen("Operation returned no output."))

    def _run_operation(self, func_name: str, input_text: str):
        """Run a string operation by name."""
        from string_ops import (
            transform, encode, json_ops, format_ops,
            find_replace, extract, hash_ops, statistics, misc,
            rearrange, manipulate, ciphers, escape
        )

        module_map = {
            'to_uppercase': transform,
            'to_lowercase': transform,
            'to_title_case': transform,
            'to_sentence_case': transform,
            'swap_case': transform,
            'to_camel_case': transform,
            'to_pascal_case': transform,
            'to_snake_case': transform,
            'to_kebab_case': transform,
            'to_constant_case': transform,
            'to_dot_case': transform,
            'to_path_case': transform,
            'to_alternating_case': transform,
            'to_sponge_case': transform,
            'capitalize_first_letter': transform,
            'decapitalize_first_letter': transform,
            'reverse_string': transform,
            'reverse_words': transform,
            'reverse_lines': transform,
            'rotate_chars': transform,
            'repeat_string': transform,
            'base64_encode': encode,
            'base64_decode': encode,
            'base64url_encode': encode,
            'base64url_decode': encode,
            'url_encode': encode,
            'url_decode': encode,
            'html_encode': encode,
            'html_decode': encode,
            'hex_encode': encode,
            'hex_decode': encode,
            'rot13': encode,
            'rot47': encode,
            'atbash': encode,
            'caesar_cipher_encode': encode,
            'caesar_cipher_decode': encode,
            'vigenere_cipher_encode': ciphers,
            'vigenere_cipher_decode': ciphers,
            'morse_encode': ciphers,
            'morse_decode': ciphers,
            'unicode_escape': encode,
            'unicode_unescape': encode,
            'binary_encode': encode,
            'binary_decode': encode,
            'octal_encode': encode,
            'octal_decode': encode,
            'base32_encode': encode,
            'base32_decode': encode,
            'base58_encode': encode,
            'base58_decode': encode,
            'base85_encode': encode,
            'base85_decode': encode,
            'punycode_encode': encode,
            'punycode_decode': encode,
            'quoted_printable_encode': encode,
            'quoted_printable_decode': encode,
            'json_escape': escape,
            'json_unescape': escape,
            'json_pretty_print': json_ops,
            'json_minify': json_ops,
            'json_to_string': json_ops,
            'string_to_json': json_ops,
            'json_diff': json_ops,
            'json_path_extract': json_ops,
            'xml_pretty_print': json_ops,
            'xml_minify': json_ops,
            'sql_pretty_print': json_ops,
            'sql_minify': json_ops,
            'css_pretty_print': json_ops,
            'css_minify': json_ops,
            'parse_query_string': json_ops,
            'stringify_query_string': json_ops,
            'jwt_decode': json_ops,
            'trim': format_ops,
            'trim_left': format_ops,
            'trim_right': format_ops,
            'trim_newlines': format_ops,
            'collapse_whitespace': format_ops,
            'remove_empty_lines': format_ops,
            'remove_duplicate_lines': format_ops,
            'sort_lines': format_ops,
            'deduplicate_lines': format_ops,
            'indent_text': format_ops,
            'unindent_text': format_ops,
            'wrap_text': format_ops,
            'replace_line_endings': format_ops,
            'normalize_unicode': format_ops,
            'strip_non_ascii': format_ops,
            'remove_diacritics': format_ops,
            'slugify': format_ops,
            'truncate': format_ops,
            'pad_left': format_ops,
            'pad_right': format_ops,
            'add_line_numbers': format_ops,
            'remove_line_numbers': format_ops,
            'extract_lines': format_ops,
            'repeat_lines': format_ops,
            'remove_all_whitespace': format_ops,
            'remove_duplicate_words': format_ops,
            'center_align': format_ops,
            'left_align': format_ops,
            'right_align': format_ops,
            'justify': format_ops,
            'spaces_to_tabs': format_ops,
            'tabs_to_spaces': format_ops,
            'expand_tabs': format_ops,
            'normalize_newlines_crlf_lf': format_ops,
            'normalize_newlines_lf_crlf': format_ops,
            'normalize_newlines_cr_lf': format_ops,
            'find_and_replace': find_replace,
            'find_and_replace_all': find_replace,
            'regex_find': find_replace,
            'regex_replace': find_replace,
            'count_matches': find_replace,
            'extract_regex_groups': find_replace,
            'extract_emails': extract,
            'extract_urls': extract,
            'extract_phone_numbers': extract,
            'extract_ip_addresses': extract,
            'extract_dates': extract,
            'extract_between_markers': extract,
            'extract_regex': extract,
            'extract_first_n': extract,
            'extract_last_n': extract,
            'extract_by_line_range': extract,
            'extract_domains': extract,
            'extract_ipv4': extract,
            'extract_ipv6': extract,
            'extract_mac': extract,
            'extract_numbers': extract,
            'extract_hashtags': extract,
            'extract_mentions': extract,
            'strip_html_tags': extract,
            'strip_markdown_tags': extract,
            'strip_punctuation': extract,
            'strip_ansi_codes': extract,
            'hash_md5': hash_ops,
            'hash_md2': hash_ops,
            'hash_md4': hash_ops,
            'hash_sha1': hash_ops,
            'hash_sha224': hash_ops,
            'hash_sha256': hash_ops,
            'hash_sha384': hash_ops,
            'hash_sha512': hash_ops,
            'hash_sha512_224': hash_ops,
            'hash_sha512_256': hash_ops,
            'hash_sha3_224': hash_ops,
            'hash_sha3_256': hash_ops,
            'hash_sha3_384': hash_ops,
            'hash_sha3_512': hash_ops,
            'hash_keccak_224': hash_ops,
            'hash_keccak_256': hash_ops,
            'hash_keccak_384': hash_ops,
            'hash_keccak_512': hash_ops,
            'hash_shake128': hash_ops,
            'hash_shake256': hash_ops,
            'hash_blake2b': hash_ops,
            'hash_blake2s': hash_ops,
            'hash_blake3': hash_ops,
            'hash_ripemd160': hash_ops,
            'hash_whirlpool': hash_ops,
            'hash_tiger': hash_ops,
            'hash_crc16': hash_ops,
            'hash_crc32': hash_ops,
            'hash_adler32': hash_ops,
            'hash_fnv1a': hash_ops,
            'hash_murmurhash': hash_ops,
            'hash_xxhash': hash_ops,
            'hash_hmac_md5': hash_ops,
            'hash_hmac_sha1': hash_ops,
            'hash_hmac_sha256': hash_ops,
            'hash_hmac_sha512': hash_ops,
            'hash_bcrypt': hash_ops,
            'hash_scrypt': hash_ops,
            'hash_argon2': hash_ops,
            'hash_pbkdf2': hash_ops,
            'count_characters': statistics,
            'count_characters_no_space': statistics,
            'count_words': statistics,
            'count_lines': statistics,
            'count_bytes': statistics,
            'count_vowels': statistics,
            'count_consonants': statistics,
            'character_frequency': statistics,
            'word_frequency': statistics,
            'shannon_entropy': statistics,
            'is_palindrome': statistics,
            'is_anagram': statistics,
            'levenshtein_distance': statistics,
            'jaro_winkler_distance': statistics,
            'hamming_distance': statistics,
            'soundex': statistics,
            'metaphone': statistics,
            'double_metaphone': statistics,
            'longest_word': statistics,
            'shortest_word': statistics,
            'count_unique_words': statistics,
            'readability_score': statistics,
            'find_most_frequent_word': statistics,
            'find_most_frequent_char': statistics,
            'diff_texts': misc,
            'generate_uuid': misc,
            'generate_password': misc,
            'generate_lorem_ipsum': misc,
            'generate_sequence': misc,
            'text_to_morse': misc,
            'morse_to_text': misc,
            'pig_latin': misc,
            'affine_cipher': misc,
            'generate_zalgo': misc,
            'generate_leetspeak': misc,
            'generate_upside_down': misc,
            'generate_vaporwave': misc,
            'generate_braille': misc,
            'generate_ulid': misc,
            'generate_nanoid': misc,
            'unslugify': misc,
            'shuffle_characters': rearrange,
            'shuffle_words': rearrange,
            'shuffle_lines': rearrange,
            'sort_characters_asc': rearrange,
            'sort_characters_desc': rearrange,
            'sort_words_asc': rearrange,
            'sort_words_desc': rearrange,
            'sort_lines_asc': rearrange,
            'sort_lines_desc': rearrange,
            'sort_lines_by_length': rearrange,
            'split_by_comma': manipulate,
            'split_by_space': manipulate,
            'split_by_newline': manipulate,
            'join_by_comma': manipulate,
            'join_by_space': manipulate,
            'chunk_text': manipulate,
            'add_prefix_lines': manipulate,
            'add_suffix_lines': manipulate,
            'string_to_ascii_array': manipulate,
            'ascii_array_to_string': manipulate,
            'xml_escape': escape,
            'xml_unescape': escape,
            'csv_escape': escape,
            'csv_unescape': escape,
            'sql_escape': escape,
            'sql_unescape': escape,
            'regex_escape': escape,
            'c_string_escape': escape,
            'c_string_unescape': escape,
            'java_string_escape': escape,
            'java_string_unescape': escape,
            'python_string_escape': escape,
            'python_string_unescape': escape,
            'bash_escape': escape,
        }

        module = module_map.get(func_name)
        if not module:
            return None

        func = getattr(module, func_name, None)
        if not func:
            return None

        try:
            return func(input_text)
        except TypeError as e:
            # Handle functions that require additional parameters
            return f"Error: This operation requires additional parameters.\n{e}"
        except Exception as e:
            return f"Error executing operation: {e}"

    def action_focus_next(self) -> None:
        focus_order = [
            "#categories-table",
            "#operations-table",
            "#text-input",
            "#text-output",
        ]

        for i, widget_id in enumerate(focus_order):
            if self.query_one(widget_id).has_focus:
                next_idx = (i + 1) % len(focus_order)
                self.query_one(focus_order[next_idx]).focus()
                return

        self.query_one(focus_order[0]).focus()

    def action_toggle_search(self) -> None:
        """Toggle search visibility."""
        self._search_visible = not self._search_visible
        search_section = self.query_one("#search-section", Container)
        search_input = self.query_one("#search-input", Input)
        if self._search_visible:
            search_section.add_class("visible")
            search_input.clear()
            search_input.focus()
        else:
            search_section.remove_class("visible")
            search_input.value = ""
            self._search_query = ""
            self._populate_operations_table()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        if event.input.id == "search-input":
            self._search_query = event.value.lower()
            self._filter_operations()

    def _filter_operations(self) -> None:
        """Filter operations based on search query."""
        table = self.query_one("#operations-table", DataTable)
        table.clear()

        if not self._search_query:
            self._populate_operations_table()
            return

        operations = self._operations.get(self._current_category, [])
        query = self._search_query.lower()
        for i, (name, func_name) in enumerate(operations):
            if query in name.lower() or query in func_name.lower():
                desc = self._get_operation_description(name)
                table.add_row(name, desc, key=str(i))

        if table.row_count > 0:
            table.move_cursor(row=0, column=0)

    def action_open_file(self) -> None:
        """Open a file dialog."""
        self.app.push_screen(FileDialogScreen("Open File", self._on_file_opened))

    def _on_file_opened(self, filepath: str | None) -> None:
        """Handle file open result."""
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.query_one("#text-input", TextArea).text = content
                self._update_status()
            except Exception as e:
                self.query_one("#text-input", TextArea).text = f"[error]Error opening file: {e}[/error]"

    def action_save_output(self) -> None:
        """Save output to file."""
        output_text = self.query_one("#text-output", TextArea).text
        if not output_text or output_text.startswith("[dim]"):
            self.app.push_screen(NotificationScreen("Nothing to save. Output is empty."))
            return

        self.app.push_screen(FileDialogScreen("Save Output", self._on_file_saved))

    def _on_file_saved(self, filepath: str | None) -> None:
        """Handle file save result."""
        if filepath:
            try:
                output_text = self.query_one("#text-output", TextArea).text
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(output_text)
                self.app.push_screen(NotificationScreen(f"Saved to {filepath}"))
            except Exception as e:
                self.app.push_screen(NotificationScreen(f"Error saving file: {e}"))


class StringOpsApp(App):
    """Main application class for String Operations TUI."""

    TITLE = "Lirum Amber"

    CSS = """
    Screen {
        background: #1a1228;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        """Initialize the app."""
        self.push_screen(CategoryScreen())

    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()


if __name__ == "__main__":
    app = StringOpsApp()
    app.run()
