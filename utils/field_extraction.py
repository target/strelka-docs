import ast
import os
import re


def parse_sample_event_dict(node):
    """
    Recursively parse an AST node representing a dictionary to extract its keys and values.
    Only handles simple literals and nested dictionaries.

    Parameters:
    - node (ast.Dict): The AST node to parse.

    Returns:
    - dict: A dictionary of keys and values extracted from the AST node.
    """
    if isinstance(node, ast.Dict):
        result = {}
        for key, value in zip(node.keys, node.values):
            key_str = parse_sample_event_ast_node(key) if key else None
            value_str = parse_sample_event_ast_node(value)
            result[key_str] = value_str
        return result
    raise ValueError("Node is not a dictionary")


def parse_sample_event_ast_node(node):
    """
    Parse an AST node and return its value as a Python object.
    Handles basic literals and dictionaries.

    Parameters:
    - node (ast.AST): The AST node to parse.

    Returns:
    - object: The value of the AST node as a Python object.
    """
    if isinstance(node, (ast.Str, ast.Constant)):  # ast.Constant for Python 3.8+
        return node.s if hasattr(node, "s") else node.value
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Dict):
        return parse_sample_event_dict(node)
    elif isinstance(node, ast.List):
        return [parse_sample_event_ast_node(elem) for elem in node.elts]
    elif isinstance(node, ast.Tuple):
        return tuple(parse_sample_event_ast_node(elem) for elem in node.elts)
    elif isinstance(node, ast.NameConstant):
        return node.value
    else:
        return repr(node)  # Fallback to a safe representation of the node


def extract_sample_event_keys(data, prefix=""):
    """
    Recursively extract keys from a nested dictionary or list.

    Parameters:
    - data (dict or list): The data structure to extract keys from.
    - prefix (str, optional): A prefix to prepend to the keys. Defaults to "".

    Returns:
    - set: A set of tuples, each containing a key and its type.
    """
    keys = set()
    if isinstance(data, dict):
        for k, v in data.items():
            full_key = f"{prefix}.{k}" if prefix else k
            keys.add((full_key, type(v).__name__))
            keys.update(extract_sample_event_keys(v, full_key))
    elif isinstance(data, list):
        for item in data:
            keys.update(extract_sample_event_keys(item, prefix))
    return keys


def extract_sample_event(tests_dir, scanner_name):
    """
    Extract a sample event from a test file for a given scanner.

    Parameters:
    - tests_dir (str): The directory containing the test files.
    - scanner_name (str): The name of the scanner.

    Returns:
    - str: The sample event code as a Markdown-formatted string.
    """
    test_file_name = f"test_scan_{scanner_name}.py"
    test_file_path = os.path.join(tests_dir, test_file_name)
    sample_event_code = ""
    inside_event = False

    try:
        with open(test_file_path, "r") as file:
            for line in file:
                if "test_scan_event" in line:
                    inside_event = True
                if inside_event:
                    # Replace mock.ANY with a fake value, e.g., 0.001 for 'elapsed' field
                    line = re.sub(r"mock\.ANY", "0.001", line)
                    sample_event_code += line
                if inside_event and line.strip().endswith("}"):
                    break
    except FileNotFoundError:
        return f"!!! failure\r\n\tTest file not found for scanner {scanner_name}"
    sample_event_code = f"```json\r\n{sample_event_code}```"
    return sample_event_code
