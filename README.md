
# Strelka Documentation

Welcome to the official documentation for Strelka, an advanced tool for automated malware analysis. This documentation aims to provide comprehensive insights into the functionality and usage of Strelka, facilitating ease of use and development.

## Table of Contents
- [Overview](#overview)
- [How Docs Work](#how-docs-work)
- [Running Docs Locally](#running-docs-locally)
- [Automated Pipeline](#automated-pipeline)
- [Documentation Format](#documentation-format)
  - [Scanners](#scanners)
  - [Scanner Class](#scanner-class)
  - [Scanner Functions](#scanner-functions)
  - [Features and Fields](#features-and-fields)
- [Backend Configuration](#backend-configuration)

## Overview

Strelka is designed for detailed malware analysis, providing robust scanning capabilities across various file types. 
The project's documentation is automatically generated and updated through GitHub Actions the latest changes in the `strelka` repository.

## How Docs Work

Documentation for Strelka is automatically generated to ensure up-to-date information. Key sections include:

- **Strelka Scanners**: Discusses the core analysis components.

## Running Docs Locally

To set up and view the documentation locally, follow these steps:

1. **Install Poetry**

   Download and install Poetry, a tool for handling Python package dependencies.

   ```bash
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
   ```

2. **Clone the Strelka Repository**

   Obtain the latest version of the `strelka` code from its repository.

   ```bash
   git clone https://github.com/target/strelka
   ```
3. **Install Dependencies**

   Use Poetry to install the necessary dependencies for running the documentation locally.

   ```bash
   poetry install
   ```

4. **(Optional) Replace Scanners**

   If you need to develop or test documentation for specific scanners, modify the scanner in the `strelka/scanner` folder.

5. **Build the Documentation**

   Generate the latest version of the documentation by running the build script. This will create new `.md` files based on all of the scanner code.

   ```bash
   python ./build_docs.py
   ```

6. **Start the Local Mkdocs Server**

   Use Poetry to run the Mkdocs server and view the documentation locally.

   ```bash
   poetry run mkdocs serve
   ```

7. **Access the Documentation**

   Open your web browser and go to `http://127.0.0.1:8000/target/strelka/` to view the local documentation.

## Automated Pipeline

`strelka-docs` builds and publishes new documents to the `gh-pages` branch. This branch is hosted on [GitHub](https://target.github.io/strelka-docs/).

## Strelka Documentation Update Process

1. **Pull Request** (`strelka` repo)
   - A user submits a PR which is then reviewed for integration.

2. **Merge** (`strelka` repo)
   - The PR is approved and merged into the main branch.

3. **Build Trigger** (`strelka` repo)
   - The merge triggers the Vela pipeline, which builds Strelka and commits to the `strelka-docs` repo.

4. **Doc Build** (`strelka-docs` repo)
   - The `strelka-docs` pipeline generates documentation using the latest `strelka` repos.

5. **Publish** (`strelka-docs` repo)
   - Newly generated documentation is published and made available to users.

## Documentation Format

### Scanners

#### Scanner Class

Documented based on Google docstrings guidelines, including:

- **Description**: A concise overview of the scanner's purpose and functionality. 
    - Includes **Scanner Type**: Collection or Malware
- **Attributes**: Details about the scanner's attributes that define its behavior. Usually found outside functions or inside init. (Can be None)
- **Other Parameters**: Details about the scanner's options. Can usually be found defined at the top of the `scan` class or inside the `backend.yml`.
- **Detection Use Cases**: Examples of potential use cases for the scanner, highlighting its detection capabilities.
- **Known Limitations**: Acknowledgment of any limitations or areas for improvement in the scanner's functionality. (Can be None)
- **Todo**: List of potential script improvements / future implementations (Can be None)
- **References**: List of references used to develop / describe the scanner (Can be None)
- **Contributors**: List of users that have assisted in the development of the scanner.

##### Example of a Class-based Docstring

```
class ScanEmail(strelka.Scanner):
    """
    Extracts and analyzes metadata, attachments, and optionally generates thumbnails from email messages.

    This scanner processes email files to extract and analyze metadata, attachments, and optionally generates
    thumbnail images of the email content for a visual overview. It supports both plain text and HTML emails,
    including inline images.

    Scanner Type: Collection

    ## Options

    Attributes:
      None
        
    Other Parameters:
        create_thumbnail (bool): Indicates whether a thumbnail should be generated for the email content.
        thumbnail_header (bool): Indicates whether email header information should be included in the thumbnail.
        thumbnail_size (int): Specifies the dimensions for the generated thumbnail images.

    ## Detection Use Cases
    !!! info "Detection Use Cases"
        - **Document Extraction**
            - Extracts and analyzes documents, including attachments, from email messages for content review.
        - **Thumbnail Generation**
            - Optionally generates thumbnail images of email content for visual analysis, which can be useful for
            quickly identifying the content of emails.
        - **Email Header Analysis**
            - Analyzes email headers for potential indicators of malicious activity, such as suspicious sender addresses
            or subject lines.

    ## Known Limitations
    !!! warning "Known Limitations"
        - **Email Encoding and Complex Structures**
            - Limited support for certain email encodings or complex email structures.
        - **Thumbnail Accuracy**
            - Thumbnail generation may not accurately represent the email content in all cases,
            especially for emails with complex layouts or embedded content.
        - **Limited Output**
            - Content is limited to a set amount of characters to prevent excessive output.

    ## To Do
    !!! question "To Do"
        - **Improve Error Handling**:
            - Enhance error handling for edge cases and complex email structures.
        - **Enhance Support for Additional Email Encodings and Content Types**:
            - Expand support for various email encodings and content types to improve scanning accuracy.

    ## References
    !!! quote "References"
        - [Python Email Parsing Documentation](https://docs.python.org/3/library/email.html)
        - [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/stable/)
        - [PyMuPDF (fitz) Documentation](https://pymupdf.readthedocs.io/en/latest/)

    ## Contributors
    !!! example "Contributors"
        - [Josh Liburdi](https://github.com/jshlbrd)
        - [Paul Hutelmyer](https://github.com/phutelmyer)
        - [Ryan O'Horo](https://github.com/ryanohoro)

    """
```


#### Example of a Function-based Docstring

Outlines function purposes, arguments, and return values, promoting clarity and ease of use.

```
        """
        Performs the scan operation on batch file data, extracting and categorizing different types of tokens.

        Args:
            data (bytes): The batch file data as a byte string.
            file (strelka.File): The file object to be scanned.
            options (dict): Options for customizing the scan. These options can dictate specific behaviors
                            like which tokens to prioritize or ignore.
            expire_at (datetime): Expiration timestamp for the scan result. This is used to determine when
                                  the scan result should be considered stale or outdated.
        """
```

