"""CLI mode for string-ops — run operations directly from the command line."""

import argparse
import importlib
import inspect
import sys
import os

from operations_mapping import OPERATIONS


_MODULES = [
    "transform",
    "encode",
    "format_ops",
    "hash_ops",
    "statistics",
    "extract",
    "find_replace",
    "json_ops",
    "escape",
    "misc",
    "rearrange",
    "manipulate",
    "ciphers",
]


def _build_index():
    name_map = {}
    func_map = {}
    for category, ops in OPERATIONS.items():
        for display_name, func_name in ops:
            name_map[display_name.lower()] = (display_name, func_name, category)
            func_map[func_name.lower()] = (display_name, func_name, category)
    return name_map, func_map


def _resolve_operation(query, name_map, func_map):
    key = query.lower().replace(" ", "_")
    if key in func_map:
        return func_map[key]
    plain = query.lower()
    if plain in name_map:
        return name_map[plain]
    combined = {**func_map, **name_map}
    for k, v in combined.items():
        if key in k or plain in k:
            return v
    return None


def _find_function(func_name):
    for mod_name in _MODULES:
        try:
            module = importlib.import_module(f"string_ops.{mod_name}")
            func = getattr(module, func_name, None)
            if func:
                return func
        except ImportError:
            continue
    return None


def _get_params(func):
    sig = inspect.signature(func)
    params = []
    for name, param in list(sig.parameters.items())[1:]:
        default = None
        if param.default is not param.empty:
            default = param.default
        params.append((name, default))
    return params


def _convert_value(value, target_type=None):
    if target_type is str:
        return value
    if target_type is bool or (target_type is None and value.lower() in ("true", "false")):
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
    if target_type is float:
        return float(value)
    if target_type is int or (target_type is None and value.isdigit()):
        return int(value)
    if target_type is None:
        try:
            return float(value)
        except ValueError:
            pass
    return value


def _format_op_list(filter_query=None):
    name_map, func_map = _build_index()
    lines = []
    f = (filter_query or "").lower()
    for category, ops in OPERATIONS.items():
        visible = [
            (name, fn) for name, fn in ops
            if not f or f in name.lower() or f in fn.lower()
        ]
        if not visible:
            continue
        lines.append(f"\n{category}:")
        for display_name, func_name in visible:
            func = _find_function(func_name)
            params = _get_params(func) if func else []
            param_str = ""
            if params:
                parts = []
                for pname, pdefault in params:
                    if pdefault is not None:
                        parts.append(f"[{pname}={pdefault}]")
                    else:
                        parts.append(f"<{pname}>")
                param_str = " " + " ".join(parts)
            lines.append(f"  {display_name}")
            lines.append(f"    {func_name}{param_str}")
    return "\n".join(lines)


def build_parser():
    name_map, func_map = _build_index()

    parser = argparse.ArgumentParser(
        prog="amber",
        description="Run 200+ string operations from the command line. "
                    "Without arguments, launches the interactive TUI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_format_op_list(),
    )

    parser.add_argument(
        "operation",
        nargs="?",
        help="Operation name (display name or function name). "
             "If omitted, launches the interactive TUI.",
    )
    parser.add_argument(
        "-t", "--text",
        help="Input text (inline string).",
    )
    parser.add_argument(
        "-i", "--input",
        metavar="FILE",
        help="Read input from file.",
    )
    parser.add_argument(
        "-p", "--param",
        action="append",
        metavar="KEY=VALUE",
        dest="params",
        help="Extra parameter (repeatable, e.g. -p shift=5 -p width=80).",
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all available operations and exit.",
    )

    return parser, name_map, func_map


def run_cli(args=None):
    parser, name_map, func_map = build_parser()

    if args is None:
        args = sys.argv[1:]

    if not args:
        # No args → launch TUI
        from tui.app import StringOpsApp
        StringOpsApp().run()
        return

    parsed = parser.parse_args(args)

    if parsed.list:
        print(_format_op_list())
        return

    if not parsed.operation:
        parser.print_help()
        return

    resolved = _resolve_operation(parsed.operation, name_map, func_map)
    if not resolved:
        print(f"Unknown operation: {parsed.operation}", file=sys.stderr)
        print("Use --list to see all available operations.", file=sys.stderr)
        sys.exit(1)

    display_name, func_name, category = resolved

    func = _find_function(func_name)
    if not func:
        print(f"Error: function '{func_name}' not found", file=sys.stderr)
        sys.exit(1)

    input_text = ""
    if parsed.text is not None:
        input_text = parsed.text
    elif parsed.input:
        try:
            with open(parsed.input, "r", encoding="utf-8") as f:
                input_text = f.read()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read()

    no_input_funcs = {
        "generate_uuid", "generate_password", "generate_lorem_ipsum",
        "generate_sequence", "generate_ulid", "generate_nanoid",
    }

    if not input_text and func_name not in no_input_funcs and parsed.text is None and not parsed.input:
        # stdin was read but empty (e.g., subprocess without piped input)
        print("Error: No input provided. Use -t TEXT, -i FILE, or pipe input.", file=sys.stderr)
        sys.exit(1)

    kwargs = {}
    func_params = _get_params(func)
    param_types = {}
    sig = inspect.signature(func)
    for name, param in sig.parameters.items():
        if param.annotation is not param.empty:
            param_types[name] = param.annotation

    for kv in (parsed.params or []):
        if "=" not in kv:
            print(f"Error: Parameter '{kv}' must be in KEY=VALUE format", file=sys.stderr)
            sys.exit(1)
        key, _, value = kv.partition("=")
        kwargs[key] = _convert_value(value, param_types.get(key))

    try:
        if func_name in no_input_funcs:
            result = func(**kwargs)
        else:
            result = func(input_text, **kwargs)
        if result is not None:
            sys.stdout.write(str(result))
            if not str(result).endswith("\n"):
                sys.stdout.write("\n")
    except TypeError as e:
        func_params = _get_params(func)
        param_desc = ", ".join(
            f"{n}={d}" if d is not None else n
            for n, d in func_params
        )
        print(
            f"Error: {e}\n"
            f"Usage: {func_name} TEXT [{param_desc}]",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
