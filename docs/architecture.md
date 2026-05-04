# Architecture

## High-Level Overview

```mermaid
graph TD
    A[main.py] --> B[StringOpsApp]
    B --> C[CategoryScreen]
    C --> D[FileDialogScreen]
    C --> E[OperationModal]
    C --> F[NotificationScreen]
    C --> G[operations_mapping.py]
    G --> H[string_ops/]
    H --> I[transform.py]
    H --> J[encode.py]
    H --> K[format_ops.py]
    H --> L[hash_ops.py]
    H --> M[statistics.py]
    H --> N[extract.py]
    H --> O[find_replace.py]
    H --> P[json_ops.py]
    H --> Q[misc.py]
    H --> R[rearrange.py]
    H --> S[manipulate.py]
    H --> T[ciphers.py]
    H --> U[escape.py]
```

## Layer Architecture

```mermaid
graph TB
    subgraph "Entry Point"
        main[main.py]
    end

    subgraph "UI Layer - tui/"
        app[tui/app.py]
        CategoryScreen[CategoryScreen]
        FileDialog[FileDialogScreen]
        Modal[OperationModal]
        Notify[NotificationScreen]
    end

    subgraph "Operation Registry"
        OpsMap[operations_mapping.py]
        Utils[string_ops/utils.py]
    end

    subgraph "Core Library - string_ops/"
        direction LR
        Transform[transform.py]
        Encode[encode.py]
        Format[format_ops.py]
        Hash[hash_ops.py]
        Stats[statistics.py]
        Extract[extract.py]
        Find[find_replace.py]
        JSON[json_ops.py]
        Misc[misc.py]
        Rearr[rearrange.py]
        Manip[manipulate.py]
        Ciph[ciphers.py]
        Esc[escape.py]
    end

    subgraph "Tests - tests/"
        TestDir[tests/]
    end

    main --> app
    app --> CategoryScreen
    CategoryScreen --> OpsMap
    CategoryScreen --> Transform
    CategoryScreen --> Encode
    CategoryScreen --> Format
    CategoryScreen --> Hash
    CategoryScreen --> Stats
    CategoryScreen --> Extract
    CategoryScreen --> Find
    CategoryScreen --> JSON
    CategoryScreen --> Misc
    CategoryScreen --> Rearr
    CategoryScreen --> Manip
    CategoryScreen --> Ciph
    CategoryScreen --> Esc

    Transform --> TestDir
    Encode --> TestDir
    Format --> TestDir
    Hash --> TestDir
    Stats --> TestDir
    Extract --> TestDir
    Find --> TestDir
    JSON --> TestDir
    Misc --> TestDir
```

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant CategoryScreen
    participant DataTable
    participant OpMap as operations_mapping
    participant Core as string_ops/

    User->>CategoryScreen: Types text in input area
    User->>DataTable: Arrow keys select category
    DataTable->>CategoryScreen: on_data_table_cell_highlighted
    CategoryScreen->>OpMap: Look up operations for category
    OpMap->>CategoryScreen: Return [(name, func), ...]
    CategoryScreen->>DataTable: Populate operations table
    User->>DataTable: Arrow keys + Enter select operation
    DataTable->>CategoryScreen: on_data_table_cell_selected
    CategoryScreen->>CategoryScreen: action_execute_operation()
    CategoryScreen->>Core: _run_operation(func_name, input)
    Core->>CategoryScreen: Return result string
    CategoryScreen->>User: Display result in output area
```

## Module Dependency Graph

```mermaid
graph LR
    main.py --> tui_app[tui/app.py]
    tui_app --> op_map[operations_mapping.py]
    tui_app --> transform
    tui_app --> encode
    tui_app --> format_ops
    tui_app --> hash_ops
    tui_app --> statistics
    tui_app --> extract
    tui_app --> find_replace
    tui_app --> json_ops
    tui_app --> misc
    tui_app --> rearrange
    tui_app --> manipulate
    tui_app --> ciphers
    tui_app --> escape

    op_map --> string_ops[All string_ops modules]
```

## Key Design Decisions

- **Single-file TUI**: The entire TUI lives in `tui/app.py` (4 classes: `CategoryScreen`, `StringOpsApp`, `FileDialogScreen`, `NotificationScreen`, `OperationModal`).
- **Operation registry**: `operations_mapping.py` maps 200+ operations to 12 categories. Each entry is `(display_name, function_name)`.
- **Late import**: Core modules are imported inside `_run_operation()` to avoid circular dependencies and speed up startup.
- **Module dispatch**: A large `module_map` dictionary routes function names to their implementing modules.
- **Real-time apply**: Text input changes trigger immediate operation execution via `on_text_area_changed`.
- **Reactive UI**: Built on Textual, a modern async TUI framework for Python.
