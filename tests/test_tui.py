"""Tests for the TUI application's interactive behavior (focus, tab, navigation)."""

import pytest
from tui.app import StringOpsApp


@pytest.mark.asyncio
async def test_initial_focus_on_categories():
    """On startup, focus should be on the categories table."""
    app = StringOpsApp()
    async with app.run_test() as pilot:
        screen = app.screen
        from textual.widgets import DataTable
        cat_table = screen.query_one("#categories-table", DataTable)
        assert cat_table.has_focus, "Categories table should have initial focus"


@pytest.mark.asyncio
async def test_tab_cycles_focus():
    """Tab should cycle focus: categories -> operations -> text-input -> text-output -> categories."""
    app = StringOpsApp()
    async with app.run_test() as pilot:
        screen = app.screen
        from textual.widgets import DataTable, TextArea

        # Initial focus: categories
        cat_table = screen.query_one("#categories-table", DataTable)
        assert cat_table.has_focus

        # Tab 1: operations
        await pilot.press("tab")
        op_table = screen.query_one("#operations-table", DataTable)
        assert op_table.has_focus, f"Expected operations table to have focus after 1st tab, got {screen.focused}"

        # Tab 2: text-input
        await pilot.press("tab")
        text_input = screen.query_one("#text-input", TextArea)
        assert text_input.has_focus, f"Expected text-input to have focus after 2nd tab, got {screen.focused}"

        # Tab 3: text-output
        await pilot.press("tab")
        text_output = screen.query_one("#text-output", TextArea)
        assert text_output.has_focus, f"Expected text-output to have focus after 3rd tab, got {screen.focused}"

        # Tab 4: back to categories
        await pilot.press("tab")
        assert cat_table.has_focus, f"Expected categories table to have focus after 4th tab, got {screen.focused}"


@pytest.mark.asyncio
async def test_arrow_keys_navigate_categories():
    """Up/Down arrow keys should change the selected category and update operations list."""
    app = StringOpsApp()
    async with app.run_test() as pilot:
        screen = app.screen
        from textual.widgets import DataTable

        cat_table = screen.query_one("#categories-table", DataTable)
        assert cat_table.has_focus, "Categories table should have focus"

        initial_category = screen._current_category

        # Press down to move to next category
        await pilot.press("down")
        new_category = screen._current_category
        assert new_category != initial_category, "Down arrow should change category"
        assert cat_table.has_focus, "Categories table should retain focus after arrow key"


@pytest.mark.asyncio
async def test_enter_executes_operation():
    """Pressing Enter on an operation should populate the output text area."""
    app = StringOpsApp()
    async with app.run_test() as pilot:
        screen = app.screen
        from textual.widgets import DataTable, TextArea

        # Type some text into the input
        await pilot.press("tab", "tab")  # nav to text-input
        text_input = screen.query_one("#text-input", TextArea)
        assert text_input.has_focus
        text_input.text = "hello world"

        # Navigate back to ops to select an operation
        await pilot.press("tab", "tab")  # to text-output then categories
        await pilot.press("tab")  # to operations

        op_table = screen.query_one("#operations-table", DataTable)
        assert op_table.has_focus, "Should be on operations table"

        # Press Enter to execute the selected operation
        await pilot.press("enter")
        text_output = screen.query_one("#text-output", TextArea)
        assert text_output.text, "Output should not be empty after executing operation"


@pytest.mark.asyncio
async def test_arrow_keys_only_navigate_when_table_focused():
    """Arrow keys on text-input should NOT change category."""
    app = StringOpsApp()
    async with app.run_test() as pilot:
        screen = app.screen
        from textual.widgets import TextArea

        # Tab to text-input
        await pilot.press("tab", "tab")

        text_input = screen.query_one("#text-input", TextArea)
        assert text_input.has_focus

        initial_category = screen._current_category

        # Press down arrow - should NOT change category (it should move text cursor)
        await pilot.press("down")
        assert screen._current_category == initial_category, (
            "Arrow keys in text-input should not change category"
        )
