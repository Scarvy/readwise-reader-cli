# Reader API Command-Line Interface

This repository provides a command-line interface (CLI) for interacting with [Readwise's Reader API](https://readwise.io/reader_api). This tool allows you to interact with the API directly from your command line, making it easy to `add`, `list`, and `import` documents into your Reader library. You can even import documents from your browser reading list, such as Chrome ReadingList.

Please note that future updates will include support for additional browsers.

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

## Usage

Before using the CLI, make sure to set the READER_API_TOKEN environment variable. You can obtain your API token [here](https://readwise.io/access_token).

```bash
export READER_API_TOKEN={your_api_token}
```

The CLI provides the following commands:

### List Documents

List documents from your Readwise account. You can specify the location to filter documents by using the `-l` or `--location` flag. Valid location options are: `new`, `later`, `archive`, and `feed`.

Example:

```bash
python -m readercli list -l archive
```

### Import Chrome Reading List

NOTE - There is no API to request ReadingList from Google, but It is being looked at [here](https://bugs.chromium.org/p/chromium/issues/detail?id=1238372).

To import your Chrome Reading List, you first need to download your data from your account, then follow these steps:

1. Navigate to the [Data & Privacy](https://myaccount.google.com/data-and-privacy) section in your account.
2. Find the "Download your data" option and click on it.
3. A list of data to export will appear. Click "Deselect all" and then locate the Chrome section.
4. Click "All Chrome data Included" and select ONLY "ReadingList".
5. Save the downloaded `.html` file to your preferred directory and take note of the file path.
6. Run the `import` command.


```bash
python -m readercli import -f ReadingList
python -m readercli import -f /path/to/CustomReadingList
```

### Add Document(s)

Add a document to your Readwise account. You can either provide a file path or name for the HTML file using the `-f` or `--file` flag, or a URL string using the `-u` or `--url` flag.

Examples:

```bash
python -m readercli add -f ReadingList.html
python -m readercli add -u https://example.com/document
```

## Command-Line Arguments

- `-h, --help`: Show the help message and exit.
- `-l, --location`: Document location for listing (`new`, `later`, `archive`, `feed`).
- `-f, --file`: File path or name for HTML file.
- `-u, --url`: URL string for the document.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.