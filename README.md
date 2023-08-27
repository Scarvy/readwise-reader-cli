# Reader API Command-Line Interface

This repository provides a command-line interface (CLI) for interacting with [Readwise's Reader API](https://readwise.io/reader_api). This tool allows you to interact with the API directly from your command line, making it easy to `add` and `list` documents from your Reader library.

Also, You can even `upload` documents from your browser reading list, such as Chrome ReadingList.

Please note that future updates will include support for additional browsers.

## Installation

Set up a virtual environment and then run:

```bash
pip install readwise-reader-cli
```

## Usage

Before using the CLI, make sure to set the READER_API_TOKEN environment variable. You can obtain your API token [here](https://readwise.io/access_token).

```bash
export READER_API_TOKEN={your_api_token}
```

The CLI provides the following commands:

```bash
Usage: python -m readercli [OPTIONS] COMMAND [ARGS]...

  Interact with your Reader Library

Options:
  --help  Show this message and exit.

Commands:
  add     Add Document
  list    List Documents
  upload  Upload Reading List File
```

### List Documents

```bash
Usage: python -m readercli list [OPTIONS]

  List Documents

Options:
  -l, --location [later|feed|new|archive]
                                  Document(s) location  [default: archive]
  -c, --category [pdf|highlight|epub|rss|tweet|video|email|note|article]
                                  Document(s) category
  -a, --update-after [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  Updated after date in ISO format.
  -L, --layout [list|table]       Display documents either as a list or table
  --help                          Show this message and exit.
```

Example:

```bash
python -m readercli list --location archive
```

```bash
python -m readercli list --location archive --category article
```

```bash
python -m readercli list --location archive --category article --update-after 2023-01-01
```

```bash
python -m readercli list --location archive --category article --update-after 2023-01-01 --layout list
```

### Upload a Reading List (Google Chrome support only)

NOTE - There is no API to request ReadingList from Google, but it is being looked at [here](https://bugs.chromium.org/p/chromium/issues/detail?id=1238372).

To `upload` your Chrome Reading List, you first need to download your data from your account, then follow these steps:

1. Navigate to the [Data & Privacy](https://myaccount.google.com/data-and-privacy) section.
2. Find the "Download your data" option and click on it.
3. A list of data to export will appear. Click "Deselect all" and then locate the Chrome section.
4. Click "All Chrome data Included" and select ONLY "ReadingList".
5. Save the downloaded `.html` file to your preferred directory and take note of the file path.
6. Run the `import` command.

```bash
Usage: python -m readercli upload [OPTIONS] INPUT_FILE

  Upload Reading List File

Options:
  --file-type [html|csv]
  --help                  Show this message and exit.
```

Examples:

```bash
python -m readercli upload /path/to/ReadingList.html
```

```bash
python -m readercli upload --file-type csv /path/to/ReadingList.csv
```

### Add Document

```bash
Usage: python -m readercli add [OPTIONS] URL

  Add Document

Options:
  --help  Show this message and exit.
```

Examples:

```bash
python -m readercli add http://www.example.com
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
