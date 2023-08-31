"""Subcommands of the main CLI module"""
import json
import os
from datetime import datetime, timedelta

import click
from xdg_base_dirs import xdg_data_home

from .api import APIHandler
from .constants import VALID_CATEGORY_OPTIONS, VALID_LOCATION_OPTIONS
from .data import fetch_full_library
from .layout import print_results, print_view_results
from .utils import (
    batch_add_documents,
    build_reading_list,
    count_category_values,
    count_location_values,
    count_tag_values,
)

DEFAULT_CATEGORY_NAME = "all"

CACHE_DIR = xdg_data_home() / "reader"
CACHED_RESULT_PATH = CACHE_DIR / "library.json"
CACHE_EXPIRATION = 1  # Minutes


@click.command(help="List Documents")
@click.option(
    "--location",
    "-l",
    type=click.Choice(VALID_LOCATION_OPTIONS, case_sensitive=True),
    help="Document(s) location",
)
@click.option(
    "--category",
    "-c",
    type=click.Choice(VALID_CATEGORY_OPTIONS, case_sensitive=True),
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
    type=click.Choice(["table", "list"], case_sensitive=True),
    help="Display documents either as a list or table. Default is table.",
)
@click.option("--pager", "-P", is_flag=True, default=False, help="Use to page output.")
@click.option(  # Don't hit Reader API
    "--no-api",
    is_flag=True,
    default=False,
    hidden=True,
)
def list(location, category, update_after, layout, pager=False, no_api=False):
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

        api = APIHandler()
        tmp_docs = api.fetch_documents(
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

    docs = tmp_docs[:-1]  # Slice off the time key before passing to layout

    print_results(docs, page=pager, layout=layout, category=category)


@click.command(help="Library breakdown")
@click.option(
    "--view",
    "-V",
    default="category",
    type=click.Choice(["category", "location", "tags"], case_sensitive=True),
)
def lib(view):
    full_data = fetch_full_library()

    if view == "location":
        stats = count_location_values(full_data)
    elif view == "tags":
        stats = count_tag_values(full_data)
    else:
        stats = count_category_values(full_data)

    print_view_results(stats=stats, view=view)


@click.command(help="Add Document")
@click.argument("url")
def add(url):
    data = {"url": url}  # plan to add more option like title, tags etc.

    api = APIHandler()
    api.add_document(data=data)


@click.command(help="Upload Reading List File")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--file-type", type=click.Choice(["html", "csv"]), default="html")
def upload(input_file, file_type):
    click.echo(f"Adding Document(s) from: {input_file}")

    reading_list = build_reading_list(input_file=input_file, file_type=file_type)

    batch_add_documents(reading_list)
