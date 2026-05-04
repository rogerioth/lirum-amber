# TUI Layer

## Overview

The TUI (Terminal User Interface) is built on [Textual](https://textual.textualize.io/), a modern Python framework for building rich terminal applications.

All TUI code lives in `tui/app.py`.

## Class Hierarchy

```mermaid
classDiagram
    class StringOpsApp {
        +TITLE = "String Operations"
        +on_mount()
        +action_quit()
    }

    class CategoryScreen {
        -_current_category: str
        -_current_operation: str
        -_search_visible: bool
        -_search_query: str
        -_operations: dict
        -_operation_map: dict
        +compose()
        +on_mount()
        +on_data_table_cell_highlighted()
        +on_data_table_cell_selected()
        +on_text_area_changed()
        +on_input_changed()
        +action_execute_operation()
        +action_toggle_search()
        +action_open_file()
        +action_save_output()
        -_run_operation()
        -_populate_operations_table()
        -_filter_operations()
        -_set_category_from_table()
        -_update_status()
        -_update_category_label()
        -_get_operation_description()
    }

    class FileDialogScreen {
        +title: str
        +on_select: Callable
        +compose()
        +on_button_pressed()
    }

    class NotificationScreen {
        +message: str
        +compose()
        +on_button_pressed()
    }

    class OperationModal {
        +operation_name: str
        +compose()
        +on_button_pressed()
    }

    StringOpsApp --> CategoryScreen : pushes on mount
    CategoryScreen --> FileDialogScreen : pushes for open/save
    CategoryScreen --> NotificationScreen : pushes for errors
    CategoryScreen --> OperationModal : pushes for param needed
```

## Screen Layout

```mermaid
graph TB
    subgraph "CategoryScreen Layout"
        direction TB
        SearchBar["[Search Section - hidden by default]"]
        MainGrid["Main Grid (2 columns)"]
        CatCol["Left Column - Categories"]
        OpCol["Right Column - Operations"]
        IOArea["Input/Output Area"]
        StatusBar["Status Bar"]

        SearchBar --> MainGrid
        MainGrid --> CatCol
        MainGrid --> OpCol
        MainGrid --> IOArea
        IOArea --> StatusBar
    end

    subgraph "Left Column"
        CatLabel["CATEGORIES label"]
        CatTable["DataTable of categories"]
    end

    subgraph "Right Column"
        OpLabel["CATEGORY_NAME OPERATIONS label"]
        OpTable["DataTable of operations"]
    end

    subgraph "Input/Output"
        InputArea["TextArea - Input"]
        OutputArea["TextArea - Output"]
    end

    CatCol --> CatLabel
    CatCol --> CatTable
    OpCol --> OpLabel
    OpCol --> OpTable
    IOArea --> InputArea
    IOArea --> OutputArea
```

## Keyboard Shortcuts

| Key | Action | Description |
|-----|--------|-------------|
| `Up` / `Down` | Navigate | Move cursor in categories or operations table |
| `Enter` | Execute | Run the highlighted operation |
| `Tab` | Focus Next | Cycle through panes (categories -> operations -> input -> output) |
| `Ctrl+/` | Toggle Search | Show/hide the search bar |
| `Ctrl+O` | Open File | Open file dialog to load text into input |
| `Ctrl+S` | Save Output | Save output area content to file |
| `Q` | Quit | Exit the application |

## Event Flow

```mermaid
sequenceDiagram
    participant DT as DataTable
    participant CS as CategoryScreen
    participant Core as string_ops/
    participant TA as TextArea

    Note over DT,TA: Category Navigation
    DT->>CS: on_data_table_cell_highlighted (categories-table)
    CS->>CS: _set_category_from_table()
    CS->>CS: _update_category_label()
    CS->>CS: _populate_operations_table()

    Note over DT,TA: Operation Selection
    DT->>CS: on_data_table_cell_highlighted (operations-table)
    CS->>CS: Track _current_operation
    DT->>CS: on_data_table_cell_selected (Enter key)
    CS->>CS: action_execute_operation()
    CS->>Core: _run_operation(func_name, input)
    Core->>CS: Return result
    CS->>TA: Update text-output area

    Note over DT,TA: Real-time Apply
    TA->>CS: on_text_area_changed (text-input)
    CS->>CS: Check _current_operation
    CS->>Core: _run_operation(func_name, input)
    Core->>CS: Return result
    CS->>TA: Update text-output area
```

## CSS Styling

The UI uses Textual's CSS-like styling defined in `CategoryScreen.CSS`:

- **Grid layout**: 2-column main grid (categories + operations)
- **Borders**: `$primary` colored borders on panes
- **Search visibility**: Controlled via `.visible` class toggling `display: block/none`
- **Status bar**: `$primary` background at the bottom
- **Category label**: `$accent` background header for each pane

## Key Bindings

Two levels of bindings exist:

1. **StringOpsApp**: Only `q` for quit (global).
2. **CategoryScreen**: `q`, `ctrl+o`, `ctrl+s`, `ctrl+/`, `tab`, `enter`.

The `show=False` on the `enter` binding prevents it from appearing in the footer, since Enter behavior is implicit in DataTable usage.
