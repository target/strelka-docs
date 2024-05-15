import os
import ast
from ruamel.yaml import YAML
from pathlib import Path
from utils.field_extraction import (
    parse_sample_event_dict,
    extract_sample_event_keys,
    extract_sample_event,
)


def load_configs():
    """
    Load configurations from 'config.yml' and 'descriptions.yml' files.

    Returns:
        tuple: A tuple containing two dictionaries: configs and descriptions.
    """

    yaml = YAML()
    with open("config.yml", "r") as file:
        configs = yaml.load(file)
    with open("descriptions.yml", "r") as file:
        descriptions = yaml.load(file)
    return configs, descriptions


configs, descriptions = load_configs()

# Use the loaded configs in the script
backend_config_path = configs["paths"]["backend_config_path"]
scanners_dir = configs["paths"]["scanners_dir"]
tests_dir = configs["paths"]["tests_dir"]
docs_dir = configs["paths"]["docs_dir"]
static_dir = configs["paths"]["static_dir"]

# Use the loaded descriptions in the script
scanner_details_features_description = descriptions["scanner_details_features"]
scanner_details_tastes_description = descriptions["scanner_details_tastes"]
scanner_details_fields_description = descriptions["scanner_details_fields"]
scanner_details_sample_event_description = descriptions["scanner_details_sample_event"]

scanner_overview_intro = descriptions["scanner_overview_intro"]

features_config = configs["features_config"]

# Material Icons
true_icon = "<div style='text-align: center; color: #66BB6A;'>:material-check: </div>"
false_icon = "<div style='text-align: center; color: #EE0F0F;'>:material-cancel: </div>"


def generate_scanner_overview(
        docs_dir, scanners_dir, tests_dir, features_config, backend_scanners
):
    """
    Generate an overview of all scanners, including their features, support for IOC, file emission, tests, malware scanners,
    and extended docs.

    Parameters:
    - docs_dir (str): The directory where the documentation will be saved.
    - scanners_dir (str): The directory containing the scanner files.
    - tests_dir (str): The directory containing the test files.
    - features_config (dict): A dictionary of feature names to search strings.
    - backend_scanners (set): A set of enabled scanner names.

    Returns:
    - None
    """
    scanner_filenames = sorted(
        [
            filename
            for filename in os.listdir(scanners_dir)
            if filename.endswith(".py") and filename != "__init__.py"
        ]
    )

    deployed_scanners_info = []
    not_deployed_scanners_info = []
    for filename in scanner_filenames:
        scanner_name = filename[:-3]
        scanner_name_camel = snake_to_camel(scanner_name)
        scanner_file_path = os.path.join(scanners_dir, filename)
        test_file_path = os.path.join(tests_dir, f"test_{scanner_name}.py")

        # Check the scanner's support for each feature using the check_features function
        feature_statuses = check_features(scanner_file_path, features_config)
        test_exists = os.path.isfile(test_file_path)

        scanner_info = {
            "Scanner Name": f"[{scanner_name_camel}]({scanner_name_camel}.md)",
            "IOC Support": (
                true_icon if feature_statuses.get("IOC Support", False) else false_icon
            ),
            "Image Thumbnails": (
                true_icon if feature_statuses.get("Image Thumbnails", False) else false_icon
            ),
            "File Emission": (
                true_icon if feature_statuses.get("Emit Files", False) else false_icon
            ),
            "Tests Created": true_icon if test_exists else false_icon,
            "Malware Scanner": (
                true_icon if feature_statuses.get("Malware", False) else false_icon
            ),
            "Extended Docs": (
                true_icon
                if feature_statuses.get("Extended Docs", False)
                else false_icon
            ),
        }

        if scanner_name_camel in backend_scanners:
            deployed_scanners_info.append(scanner_info)
        else:
            not_deployed_scanners_info.append(scanner_info)

    # Generate Markdown tables for deployed and not deployed scanners
    deployed_table = generate_scanner_table(deployed_scanners_info, "Deployed Scanners")
    not_deployed_table = generate_scanner_table(
        not_deployed_scanners_info, "Not Deployed Scanners"
    )

    overview_content = f"# Strelka Scanner Overview\n\n{scanner_overview_intro}\n\n{deployed_table}\n\n{not_deployed_table}\n"

    overview_filepath = os.path.join(docs_dir, "Scanners/ScannerOverview.md")
    with open(overview_filepath, "w") as overview_file:
        overview_file.write(overview_content)


def generate_scanner_table(scanner_info_list, table_title):
    """
    Generate a Markdown table for a list of scanner information.

    Parameters:
    - scanner_info_list (list): A list of dictionaries containing scanner information.
    - table_title (str): The title of the table.

    Returns:
    - str: The Markdown formatted table as a string.
    """
    # Generate Markdown table
    markdown_table = f"## {table_title}\n\n"
    markdown_table += "| " + " |  <div style='text-align: center';> ".join(scanner_info_list[0].keys()) + " </div> |\n"
    markdown_table += "|---" * len(scanner_info_list[0]) + "|\n"
    for scanner_info in scanner_info_list:
        markdown_table += "| " + " | ".join(scanner_info.values()) + " |\n"

    return markdown_table


def extract_fields_from_test(tests_dir, scanner_name):
    """
    Extract fields from a test file for a given scanner.

    Parameters:
    - tests_dir (str): The directory containing the test files.
    - scanner_name (str): The name of the scanner.

    Returns:
    - set: A set of tuples, each containing a field name and its type.
    """
    test_file_name = f"test_scan_{scanner_name}.py"
    test_file_path = Path(tests_dir) / test_file_name
    fields = set()

    try:
        with open(test_file_path, "r") as file:
            content = file.read()
            parsed_ast = ast.parse(content)
            for node in ast.walk(parsed_ast):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if (
                                isinstance(target, ast.Name)
                                and target.id == "test_scan_event"
                        ):
                            event_dict = parse_sample_event_dict(node.value)
                            fields.update(extract_sample_event_keys(event_dict))
                            break
    except FileNotFoundError:
        print(f"Test file not found for scanner {scanner_name}")
    except Exception as e:
        print(f"Error processing test file {test_file_name}: {e}")

    return fields

def snake_to_camel(word):
    """
    Convert snake_case to CamelCase.

    Parameters:
    - word (str): The snake_case string to convert.

    Returns:
    - str: The converted CamelCase string.
    """
    return "".join(x.capitalize() or "_" for x in word.split("_"))


def check_features(scanner_file_path, features_config):
    """
    Check for the presence of features in a scanner file based on the given features configuration.

    Parameters:
    - scanner_file_path (str): The path to the scanner file to check.
    - features_config (dict): A dictionary of feature names to search strings.

    Returns:
    - dict: A dictionary of feature presence, with feature names as keys and boolean values indicating presence.
    """
    feature_statuses = {}
    with open(scanner_file_path, "r") as file:
        content = file.read()
        for feature_name, search_string in features_config.items():
            feature_statuses[feature_name] = search_string in content
    return feature_statuses


def generate_features_table(feature_statuses):
    """
    Generate a Markdown table representing the support of various features.

    Parameters:
    - feature_statuses (dict): A dictionary of feature statuses to be included in the table.

    Returns:
    - str: The Markdown formatted table as a string.
    """
    table_header = "| Feature | <div style='text-align: center';> Support </div> |\n|---|---|\n"
    table_rows = [
        "| `{}` | {} |".format(
            feature,
            (
                "<div style='text-align: center; color: #66BB6A;'> :material-check: </div>"
                if status
                else "<div style='text-align: center; color: #EE0F0F;'>:material-cancel: </div>"
            ),
        )
        for feature, status in feature_statuses.items()
    ]
    return table_header + "\n".join(table_rows)


def generate_fields_table(fields_set):
    """
    Generate a Markdown table for the fields of a scanner.

    Parameters:
    - fields_set (set): A set of tuples, each containing a field name and its type.

    Returns:
    - str: The Markdown formatted table as a string.
    """
    # Updated the function to handle empty or error scenarios
    if not fields_set:
        return "!!! failure\r\n\tNo fields to display. The test file may not exist or could not be processed."
    table_header = "| Field Name | <div style='text-align: center';> Field Type </div> |\n|---|---|\n"
    # Sort the fields by their name before generating the table rows
    sorted_fields = sorted(fields_set, key=lambda x: x[0])
    table_rows = [
        f"| `{field}` | <div style='text-align: center''>`{field_type}`</div> |" for field, field_type in sorted_fields
    ]
    return table_header + "\n".join(table_rows)


def generate_tastes_table(positive, negative):
    """
    Generate a Markdown table for the tastes (positive and negative) of a scanner.

    Parameters:
    - positive (list): List of positive tastes (file types the scanner can process).
    - negative (list): List of negative tastes (scanners that should not process the file after this scanner).

    Returns:
    - str: The Markdown formatted table as a string.
    """
    positive_icon = "<div style='text-align: center; color: #66BB6A;'> :material-check: </div>"
    negative_icon = "<div style='text-align: center; color: #EE0F0F;'>:material-cancel: </div>"

    # Sort the filetypes
    positive_sorted = sorted(positive)
    negative_sorted = sorted(negative)

    rows = []
    for flavor in positive_sorted:
        rows.append(f"| `{flavor}` | {positive_icon} |")
    for source in negative_sorted:
        rows.append(f"| `{source}` | {negative_icon} |")

    # Construct the table
    table_header = "| Source Filetype | <div style='text-align: center';> Include / Exclude </div> |\n|---|---|\n"
    table = table_header + "\n".join(sorted(rows))

    return table


def update_mkdocs_config(
        mkdocs_config_path,
        enabled_nav_entries,
        disabled_nav_entries,
):
    """
    Update the MkDocs configuration file with the generated navigation entries.

    Parameters:
    - mkdocs_config_path (str): The path to the MkDocs configuration file.
    - enabled_nav_entries (list): A list of dictionaries for enabled scanner navigation entries.
    - disabled_nav_entries (list): A list of dictionaries for disabled scanner navigation entries.

    Returns:
    - None
    """
    with open(mkdocs_config_path, "r") as mkdocs_file:
        yaml = YAML()
        mkdocs_config = yaml.load(mkdocs_file)

    mkdocs_config["nav"] = [
        {
            "Strelka": [
                {"Overview": "index.md"},
                {"Use Cases": "Strelka/StrelkaUseCases.md"},
                {"FAQ": "Strelka/StrelkaFaq.md"},
            ]
        },
        {
            "Getting Started": [
                {"Quickstart": "GettingStarted/GettingStartedQuickstart.md"},
                {"Installation": "GettingStarted/GettingStartedInstallation.md"},
            ],
        },
        {
            "Scanners": [
                {"Overview": "Scanners/ScannerOverview.md"},
                {"Deployed": enabled_nav_entries},
                {"Not Deployed": disabled_nav_entries},
            ]
        },
        {
            "Strelka UI": [
                {"Overview": "StrelkaUi/StrelkaUiOverview.md"},
            ]
        },
        {
            "Community": [
                {"Overview": "Community/CommunityOverview.md"},
                {"Opensource": "Community/CommunityOpensource.md"},
            ],
        },
    ]

    with open(mkdocs_config_path, "w") as mkdocs_file:
        yaml.dump(mkdocs_config, mkdocs_file)


def process_scanner(
        filename, backend_scanners, docs_dir, features_config, backend_config, tests_dir
):
    """
    Process a scanner file, generate its documentation, and return information for navigation.

    Parameters:
    - filename (str): The name of the scanner file.
    - backend_scanners (set): A set of enabled scanner names.
    - docs_dir (str): The directory where the documentation will be saved.
    - features_config (dict): A dictionary of feature names to search strings.
    - backend_config (dict): The loaded YAML configuration for the backend.
    - tests_dir (str): The directory containing the test files.

    Returns:
    - dict: A dictionary containing the scanner name, whether it's enabled, and its filepath.
    """
    scanner_file_path = os.path.join(scanners_dir, filename)
    scanner_name_snake = filename[:-3]
    scanner_name_camel = snake_to_camel(scanner_name_snake)

    feature_statuses = check_features(scanner_file_path, features_config)
    features_table = generate_features_table(feature_statuses)

    # Get the scanner configuration to generate the tastes table
    scanner_config = backend_config.get("scanners", {}).get(scanner_name_camel, [])

    # Extract the Sample Event code from the test file
    scanner_test_name = filename.replace("scan_", "").replace(".py", "")
    sample_event_code = extract_sample_event(tests_dir, scanner_test_name)

    positive_flavors = []
    negative_sources = []

    if scanner_config:
        for config in scanner_config:
            if "positive" in config:
                positive_flavors.extend(config["positive"].get("flavors", []))
            if "negative" in config:
                negative_sources.extend(config["negative"].get("source", []))

    tastes_table = generate_tastes_table(positive_flavors, negative_sources)

    # Extract the Sample Event fields and types from the test file
    scanner_test_name = filename.replace("scan_", "").replace(".py", "")
    event_fields = extract_fields_from_test(tests_dir, scanner_test_name)
    event_fields_table = generate_fields_table(event_fields)

    md_content = (
        f"# {scanner_name_camel}\n\n"
        f"::: strelka.src.python.strelka.scanners.{scanner_name_snake}.{scanner_name_camel}\n"
        f"## Features\n\n{scanner_details_features_description}\n\n{features_table}\n\n"
        f"## Tastes\n\n{scanner_details_tastes_description}\n\n{tastes_table}\n\n"
        f"## Scanner Fields\n\n{scanner_details_fields_description}\n\n{event_fields_table}\n\n"
        f"## Sample Event\n\n{scanner_details_sample_event_description}\n\n\n{sample_event_code}\n\n"
    )
    md_filepath = os.path.join(docs_dir, f"Scanners/{scanner_name_camel}.md")
    with open(md_filepath, "w") as md_file:
        md_file.write(md_content)

    return {
        "name": scanner_name_camel,
        "enabled": scanner_name_camel in backend_scanners,
        "filepath": f"{scanner_name_camel}.md",
    }


def main():
    """
    The main function orchestrates the generation of documentation for scanners configurations.

    This script performs the following steps:
    1. Loads backend configuration to determine which scanners are enabled.
    2. Processes each scanner file to generate detailed documentation, including features, tastes, fields, and sample events.
    3. Generates an overview of all scanners, including their support for various features and tests.
    4. Updates the mkdocs.yml configuration file to include navigation entries for the generated documentation.

    The script expects the following directory structure and files:
    - A 'static_dir' containing static Markdown files to be included in the documentation.
    - A 'scanners_dir' containing Python files for each scanner, excluding '__init__.py'.
    - A 'tests_dir' containing test files for each scanner.
    - A 'backend_config_path' pointing to a YAML file with backend configuration details.
    - A 'docs_dir' where the generated documentation will be stored.

    The script generates Markdown files for each scanner configuration, including an overview file. It also updates the mkdocs.yml file to include navigation entries for the generated documentation.

    After running this script, the 'docs_dir' will be populated with detailed documentation for each scanner configuration, ready for use with a documentation generator like MkDocs.

    Usage:
    - Ensure all required directories and files are in place.
    - Run the script to generate documentation.
    - Use the generated documentation with a documentation generator to create a browsable documentation site.
    """
    yaml = YAML()

    with open(backend_config_path, "r") as backend_file:
        backend_config = yaml.load(backend_file)

    backend_scanners = set(backend_config.get("scanners", {}).keys())
    enabled_nav_entries = []
    disabled_nav_entries = []

    # Get all scanner filenames, excluding '__init__.py', and sort them alphabetically
    scanner_filenames = sorted(
        [
            filename
            for filename in os.listdir(scanners_dir)
            if filename.endswith(".py") and filename != "__init__.py"
        ]
    )

    for filename in scanner_filenames:
        scanner_info = process_scanner(
            filename,
            backend_scanners,
            docs_dir,
            features_config,
            backend_config,
            tests_dir,
        )
        nav_entry = {scanner_info["name"]: f"Scanners/{scanner_info['filepath']}"}
        if scanner_info["enabled"]:
            enabled_nav_entries.append(nav_entry)
        else:
            disabled_nav_entries.append(nav_entry)

    # Sort the enabled and disabled scanner entries alphabetically by name
    enabled_nav_entries.sort(key=lambda x: list(x.keys())[0])
    disabled_nav_entries.sort(key=lambda x: list(x.keys())[0])

    # Update mkdocs.yml navigation
    update_mkdocs_config(
        "mkdocs.yml",
        enabled_nav_entries,
        disabled_nav_entries,
    )

    generate_scanner_overview(
        docs_dir, scanners_dir, tests_dir, features_config, backend_scanners
    )

    print("Documentation generation completed.")


if __name__ == "__main__":
    main()
