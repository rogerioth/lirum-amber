import json


def json_escape(s: str) -> str:
    return json.dumps(s)


def json_unescape(s: str) -> str:
    return json.loads(s)


def json_pretty_print(s: str) -> str:
    obj = json.loads(s)
    return json.dumps(obj, indent=2, ensure_ascii=False)


def json_minify(s: str) -> str:
    obj = json.loads(s)
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=False)


def json_to_string(s: str) -> str:
    obj = json.loads(s)
    return str(obj)


def string_to_json(s: str) -> str:
    return json.dumps(s)


def json_diff(json1: str, json2: str) -> dict:
    obj1 = json.loads(json1)
    obj2 = json.loads(json2)
    return {
        'identical': obj1 == obj2,
        'json1': obj1,
        'json2': obj2,
    }


def json_path_extract(json_str: str, path: str) -> any:
    obj = json.loads(json_str)
    keys = path.strip('.').split('.')
    current = obj
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list):
            try:
                current = current[int(key)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return current
