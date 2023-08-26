"""Subcommands of the main CLI module"""
import os
import json
from datetime import datetime, timedelta

import click
from xdg_base_dirs import xdg_data_home

from .api import fetch_documents, add_document
from .layout import print_layout
from .constants import VALID_CATEGORY_OPTIONS, VALID_LOCATION_OPTIONS
from .utils import add_document_batch, build_reading_list

DEFAULT_CATEGORY_NAME = "all"

CACHE_DIR = xdg_data_home() / "reader"
CACHED_RESULT_PATH = CACHE_DIR / "library.json"
CACHE_EXPIRATION = 1  # Minutes


@click.command(help="List Documents")
@click.option(
    "--location",
    "-l",
    default="archive",
    show_default=True,
    type=click.Choice(VALID_LOCATION_OPTIONS, case_sensitive=False),
    help="Document(s) location",
)
@click.option(
    "--category",
    "-c",
    type=click.Choice(VALID_CATEGORY_OPTIONS, case_sensitive=False),
    help="Document(s) category",
)
@click.option(
    "--update-after",
    "-a",
    default=(datetime.now() - timedelta(days=1)),
    type=click.DateTime(),
    help="Updated after date in ISO format.",
)
@click.option(
    "--layout",
    "-L",
    type=click.Choice(["list", "table"], case_sensitive=True),
    help="Display documents either as a list or table",
)
@click.option(  # Don't hit Reader API
    "--no-api",
    is_flag=True,
    default=False,
    hidden=True,
)
def list(location, category, update_after, layout, no_api=False):
    update_after_str = update_after.strftime("%Y-%m-%d")

    options_key = f"{location}_{(DEFAULT_CATEGORY_NAME if not category else category)}_{update_after_str}"

    if no_api:  # check options_key
        click.echo(options_key)

    tmp_docs = None

    if os.path.exists(CACHED_RESULT_PATH):
        with open(CACHED_RESULT_PATH, "r") as f:
            json_file = json.load(f)
            result = json_file.get(options_key)
            if result:
                t = result[-1].get("time")
                time = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
                diff = datetime.now() - time
                if diff < timedelta(minutes=CACHE_EXPIRATION):
                    print("Using cache instead!")
                    tmp_docs = result

    if not tmp_docs:  # If cache expired or results not yet cached
        if no_api:
            return

        tmp_docs = fetch_documents(
            updated_after=update_after, location=location, category=category
        )

        if len(tmp_docs) == 0:  # if list of documents is empty
            return

        else:  # Cache documents
            tmp_docs.append({"time": str(datetime.now())})
            os.makedirs(CACHE_DIR, exist_ok=True)

            with open(CACHED_RESULT_PATH, "a+") as f:
                if os.path.getsize(CACHED_RESULT_PATH) == 0:  # file is empty
                    result_dict = {options_key: tmp_docs}
                    f.write(json.dumps(result_dict, indent=4))
                else:
                    f.seek(0)
                    result_dict = json.load(f)
                    result_dict[options_key] = tmp_docs
                    f.truncate(0)
                    f.write(json.dumps(result_dict, indent=4))

    docs = tmp_docs

    print_layout(
        docs[:-1], layout=layout
    )  # Slice off the time key before passing to layout


@click.command(help="Add Document")
@click.argument("url")
def add(url):
    add_document(data={"url": url})


@click.command(help="Upload Reading List File")
@click.argument("filename", type=click.File("rb"))
def upload(filename):
    click.echo(f"Adding Document(s) from file: {filename}")

    reading_list = build_reading_list(filename)

    add_document_batch(reading_list)
