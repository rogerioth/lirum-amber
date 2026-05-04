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
        variant: primary;
    }

    #btn-cancel {
        dock: right;
        variant: default;
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
        variant: primary;
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

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+o", "open_file", "Open File"),
        Binding("ctrl+s", "save_output", "Save Output"),
        Binding("ctrl+/", "toggle_search", "Search"),
        Binding("left", "prev_category", "Prev Category"),
        Binding("right", "next_category", "Next Category"),
        Binding("up", "move_up", "Up"),
        Binding("down", "move_down", "Down"),
        Binding("enter", "execute_operation", "Execute"),
    ]

    CSS = """
    Screen {
        layout: vertical;
    }

    #title {
        width: 1fr;
        height: 3;
        content-align: center middle;
        background: $accent;
        color: $text;
    }

    Container > #title {
        width: 1fr;
        height: 3;
    }

    #search-section {
        width: 1fr;
        height: 3;
        display: none;
        padding: 0 1;
    }

    #search-section.visible {
        display: block;
    }

    #search-input {
        width: 1fr;
    }

    #main-content {
        width: 1fr;
        height: 1fr;
    }

    #categories-pane {
        width: 35%;
        height: 1fr;
    }

    #categories-title {
        width: 1fr;
        height: 1;
        padding: 0 1;
        text-align: center;
        color: $text;
        background: $boost;
    }

    #category-label {
        width: 1fr;
        height: 1;
        padding: 0 1;
        text-align: center;
        color: $text;
        background: $accent;
    }

    DataTable#operations-table {
        width: 1fr;
        height: 1fr;
    }

    DataTable#operations-table > .datatable--cursor {
        background: $accent;
        color: $text;
    }

    #text-panes {
        width: 65%;
        height: 1fr;
    }

    #input-section {
        height: 50%;
        width: 1fr;
    }

    #output-section {
        height: 50%;
        width: 1fr;
    }

    #input-label, #output-label {
        width: 1fr;
        padding: 0 1;
        color: $text;
        background: $boost;
    }

    #input-label {
        content-align: left middle;
    }

    #output-label {
        content-align: left middle;
    }

    #text-input, #text-output {
        width: 1fr;
        height: 1fr;
        border: solid $accent;
        padding: 1;
    }

    #text-output {
        border: solid $success;
    }

    #status-bar {
        width: 1fr;
        height: 3;
        content-align: center middle;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_category = None
        self._current_operation = None
        self._search_visible = False
        self._search_query = ""
        self._operations = {}
        self._category_names = []
        self._operation_map = {}  # Maps operation name to function name
        self._load_operations()

    def _load_operations(self):
        """Load all operations from string_ops.utils."""
        from string_ops.utils import get_all_operations
        self._operations = get_all_operations()
        self._category_names = list(self._operations.keys())
        # Build operation name to function name mapping
        self._operation_map = {}
        for category, ops in self._operations.items():
            for name, func_name in ops:
                self._operation_map[name] = func_name

    def compose(self) -> ComposeResult:
        with Container():
            yield Static("String Operations TUI", id="title")

        with Container(id="search-section"):
            yield Input(placeholder="Search operations... (Ctrl+/ to toggle)", id="search-input")

        with Horizontal(id="main-content"):
            with Vertical(id="categories-pane"):
                yield Static("Categories", id="categories-title")
                yield Static("", id="category-label")
                yield DataTable(id="operations-table")

            with Vertical(id="text-panes"):
                with Vertical(id="input-section"):
                    yield Static("Input", id="input-label")
                    yield TextArea(id="text-input")

                with Vertical(id="output-section"):
                    yield Static("Output", id="output-label")
                    yield TextArea(id="text-output")

        yield Static("", id="status-bar")

    def on_mount(self) -> None:
        """Initialize the screen."""
        self._current_category = self._category_names[0] if self._category_names else None
        self._update_category_label()
        self._init_operations_table()
        self._populate_operations_table()
        self._update_status()
        title = self.query_one("#title", Static)
        cat_names = ", ".join(self._category_names) if self._category_names else "none"
        title.update(
            f"[bold]String Operations TUI[/bold]  "
            f"[dim]Categories: {cat_names}  |  Ctrl+/ Search  |  Ctrl+O Open  |  Ctrl+S Save  |  Q Quit[/dim]"
        )

    def _init_operations_table(self) -> None:
        """Initialize the operations table with columns (called once)."""
        table = self.query_one("#operations-table", DataTable)
        table.add_columns("Operation", "Description")

    def _update_category_label(self) -> None:
        """Update the category label display."""
        if self._current_category:
            count = len(self._operations.get(self._current_category, []))
            label = f"[bold]{self._current_category}[/bold]  [{count} operations]"
            cat_label = self.query_one("#category-label", Static)
            cat_label.update(label)

    def _populate_operations_table(self) -> None:
        """Populate the operations table."""
        table = self.query_one("#operations-table", DataTable)
        table.clear()

        operations = self._operations.get(self._current_category, [])
        for i, (name, func_name) in enumerate(operations):
            desc = self._get_operation_description(name)
            table.add_row(name, desc, key=str(i))

        if operations:
            table.move_cursor(row=0, column=0)

    def _get_operation_description(self, name: str) -> str:
        """Get a short description for an operation."""
        descriptions = {
            "To Uppercase": "Convert text to uppercase",
            "To Lowercase": "Convert text to lowercase",
            "To Title Case": "Capitalize first letter of each word",
            "To Sentence Case": "Capitalize first letter of each sentence",
            "Swap Case": "Swap uppercase and lowercase",
            "CamelCase": "Convert to camelCase",
            "PascalCase": "Convert to PascalCase",
            "snake_case": "Convert to snake_case",
            "kebab-case": "Convert to kebab-case",
            "CONSTANT_CASE": "Convert to CONSTANT_CASE",
            "Reverse": "Reverse the entire string",
            "Reverse Words": "Reverse word order",
            "Reverse Lines": "Reverse line order",
            "Rotate N Characters": "Caesar-style rotation",
            "Repeat N Times": "Repeat string N times",
            "Base64 Encode": "Encode to Base64",
            "Base64 Decode": "Decode from Base64",
            "URL Encode": "Percent-encode for URLs",
            "URL Decode": "Percent-decode from URLs",
            "HTML Entity Encode": "Convert to HTML entities",
            "HTML Entity Decode": "Convert from HTML entities",
            "Hex Encode": "Convert to hex string",
            "Hex Decode": "Convert from hex string",
            "ROT13": "Apply ROT13 cipher",
            "Unicode Escape": "Convert to unicode sequences",
            "Unicode Unescape": "Convert unicode to characters",
            "Binary Encode": "Convert to binary",
            "Binary Decode": "Convert from binary",
            "Octal Encode": "Convert to octal",
            "Octal Decode": "Convert from octal",
            "JSON Escape": "Escape for JSON string",
            "JSON Unescape": "Unescape JSON string",
            "JSON Pretty Print": "Format JSON with indentation",
            "JSON Minify": "Compact JSON",
            "JSON to String": "Parse JSON to string",
            "String to JSON": "Wrap text as JSON string",
            "JSON Diff": "Compare two JSON inputs",
            "JSON Path Extract": "Extract value by JSONPath",
            "Trim (both)": "Strip leading/trailing whitespace",
            "Trim Left": "Strip leading whitespace",
            "Trim Right": "Strip trailing whitespace",
            "Trim Newlines": "Strip leading/trailing newlines",
            "Collapse Whitespace": "Replace runs of whitespace",
            "Remove Empty Lines": "Remove blank lines",
            "Remove Duplicate Lines": "Remove duplicate lines",
            "Sort Lines": "Sort lines alphabetically",
            "Deduplicate Lines": "Remove consecutive duplicates",
            "Indent": "Add indentation",
            "Unindent": "Remove indentation",
            "Wrap Text": "Wrap to N columns",
            "Replace Line Endings": "CRLF <-> LF <-> CR",
            "Normalize Unicode": "NFC/NFD/NFKC/NFKD",
            "Strip Non-ASCII": "Remove non-ASCII characters",
            "Remove Diacritics": "Strip accents",
            "Slugify": "Convert to URL slug",
            "Truncate": "Truncate with suffix",
            "Pad Left": "Pad on the left",
            "Pad Right": "Pad on the right",
            "Add Line Numbers": "Prefix line numbers",
            "Remove Line Numbers": "Strip line numbers",
            "Extract Lines": "Extract lines in range",
            "Repeat Lines N Times": "Repeat each line N times",
            "Find and Replace": "Find and replace text",
            "Find and Replace All": "Replace all occurrences",
            "Regex Find": "Find all regex matches",
            "Regex Replace": "Replace regex matches",
            "Count Matches": "Count regex matches",
            "Extract Regex Groups": "Extract captured groups",
            "Extract Emails": "Find email addresses",
            "Extract URLs": "Find URLs",
            "Extract Phone Numbers": "Find phone numbers",
            "Extract IP Addresses": "Find IPv4/IPv6",
            "Extract Dates": "Find date patterns",
            "Extract Between Markers": "Extract between markers",
            "Extract by Regex": "Extract regex matches",
            "Extract First N Chars": "Get first N characters",
            "Extract Last N Chars": "Get last N characters",
            "Extract by Line Range": "Extract lines N-M",
            "MD5": "Compute MD5 hash",
            "SHA-1": "Compute SHA-1 hash",
            "SHA-256": "Compute SHA-256 hash",
            "SHA-512": "Compute SHA-512 hash",
            "CRC32": "Compute CRC32 checksum",
            "HMAC": "Compute HMAC",
            "Count Characters": "Total character count",
            "Count Characters (no space)": "Exclude whitespace",
            "Count Words": "Word count",
            "Count Lines": "Line count",
            "Count Bytes": "Byte count",
            "Character Frequency": "Frequency of each character",
            "Word Frequency": "Frequency of each word",
            "Shannon Entropy": "Calculate Shannon entropy",
            "Palindrome Check": "Check if palindrome",
            "Levenshtein Distance": "Edit distance",
            "Longest Word": "Find the longest word",
            "Shortest Word": "Find the shortest word",
            "Unique Words": "Count unique words",
            "Readability Score": "Flesch-Kincaid score",
            "Compare Two Texts": "Diff two inputs",
            "Generate UUID": "Generate random UUID",
            "Generate Password": "Generate random password",
            "Generate Lorem Ipsum": "Generate lorem ipsum text",
            "Generate Sequence": "Number/alphabet sequence",
            "Text to Morse Code": "Convert to Morse",
            "Morse to Text": "Convert from Morse",
            "Pig Latin": "Convert to Pig Latin",
            "Atbash Cipher": "Atbash substitution",
            "Vigenere Cipher": "Vigenere cipher",
            "Affine Cipher": "Affine cipher",
        }
        return descriptions.get(name, "")

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
            "  [dim]Up/Down Navigate | Enter Execute | Ctrl+/ Search | Ctrl+O Open | Ctrl+S Save | Q Quit[/dim]"
        )

    def action_move_up(self) -> None:
        """Move selection up."""
        table = self.query_one("#operations-table", DataTable)
        if table.row_count > 0 and table.cursor_row > 0:
            table.move_cursor(row=table.cursor_row - 1)
            self._update_status()

    def action_move_down(self) -> None:
        """Move selection down."""
        table = self.query_one("#operations-table", DataTable)
        if table.row_count > 0 and table.cursor_row < table.row_count - 1:
            table.move_cursor(row=table.cursor_row + 1)
            self._update_status()

    def action_prev_category(self) -> None:
        """Switch to previous category."""
        if not self._category_names:
            return
        idx = self._category_names.index(self._current_category)
        idx = (idx - 1) % len(self._category_names)
        self._current_category = self._category_names[idx]
        self._update_category_label()
        self._populate_operations_table()
        self._update_status()

    def action_next_category(self) -> None:
        """Switch to next category."""
        if not self._category_names:
            return
        idx = self._category_names.index(self._current_category)
        idx = (idx + 1) % len(self._category_names)
        self._current_category = self._category_names[idx]
        self._update_category_label()
        self._populate_operations_table()
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
        # Direct import approach - import all modules upfront
        from string_ops import (
            transform, encode, json_ops, format_ops,
            find_replace, extract, hash_ops, statistics, misc
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
            'reverse_string': transform,
            'reverse_words': transform,
            'reverse_lines': transform,
            'rotate_chars': transform,
            'repeat_string': transform,
            'base64_encode': encode,
            'base64_decode': encode,
            'url_encode': encode,
            'url_decode': encode,
            'html_encode': encode,
            'html_decode': encode,
            'hex_encode': encode,
            'hex_decode': encode,
            'rot13': encode,
            'unicode_escape': encode,
            'unicode_unescape': encode,
            'binary_encode': encode,
            'binary_decode': encode,
            'octal_encode': encode,
            'octal_decode': encode,
            'json_escape': json_ops,
            'json_unescape': json_ops,
            'json_pretty_print': json_ops,
            'json_minify': json_ops,
            'json_to_string': json_ops,
            'string_to_json': json_ops,
            'json_diff': json_ops,
            'json_path_extract': json_ops,
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
            'hash_md5': hash_ops,
            'hash_sha1': hash_ops,
            'hash_sha256': hash_ops,
            'hash_sha512': hash_ops,
            'hash_crc32': hash_ops,
            'hash_hmac': hash_ops,
            'count_characters': statistics,
            'count_characters_no_space': statistics,
            'count_words': statistics,
            'count_lines': statistics,
            'count_bytes': statistics,
            'character_frequency': statistics,
            'word_frequency': statistics,
            'shannon_entropy': statistics,
            'is_palindrome': statistics,
            'levenshtein_distance': statistics,
            'longest_word': statistics,
            'shortest_word': statistics,
            'count_unique_words': statistics,
            'readability_score': statistics,
            'diff_texts': misc,
            'generate_uuid': misc,
            'generate_password': misc,
            'generate_lorem_ipsum': misc,
            'generate_sequence': misc,
            'text_to_morse': misc,
            'morse_to_text': misc,
            'pig_latin': misc,
            'atbash': misc,
            'vigenere_cipher': misc,
            'affine_cipher': misc,
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

    TITLE = "String Operations"

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
