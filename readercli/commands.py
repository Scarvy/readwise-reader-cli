"""Subcommands of the main CLI module"""
import json
import os
from datetime import datetime, timedelta

import click
from click import secho
from xdg_base_dirs import xdg_data_home

from .api import add_document, list_documents, validate_token
from .constants import VALID_CATEGORY_OPTIONS, VALID_LOCATION_OPTIONS
from .data import fetch_full_library
from .layout import print_results, print_view_results
from .reading_list import build_reading_list
from .models import DocumentInfo
from .utils import (
    batch_add_documents,
    convert_date_range,
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
    type=click.Choice(tuple(VALID_LOCATION_OPTIONS), case_sensitive=True),
    help="Document(s) location",
)
@click.option(
    "--category",
    "-c",
    type=click.Choice(tuple(VALID_CATEGORY_OPTIONS), case_sensitive=True),
    help="Document(s) category",
)
@click.option(
    "--update-after",
    "-a",
    default=(datetime.now() - timedelta(days=1)),
    type=click.DateTime(),
    help="Updated after date in ISO format. Default: last 24hrs.",
)
@click.option(
    "--date-range",
    "-d",
    type=str,
    help="View documents updated after choosen time: day, week, month.",
)
@click.option(
    "--layout",
    "-L",
    type=click.Choice(["table", "list"], case_sensitive=True),
    help="Display documents either as a list or table. Default: table.",
)
@click.option(
    "--num-results",
    "-n",
    type=int,
    help="The number of documents to show.",
)
@click.option("--pager", "-P", is_flag=True, default=False, help="Use to page output.")
@click.option("--debug", is_flag=True, default=False, hidden=True)
@click.option(  # Don't hit Reader API
    "--no-api",
    is_flag=True,
    default=False,
    hidden=True,
)
def list(
    location,
    category,
    update_after,
    date_range,
    layout,
    num_results,
    pager=False,
    debug=False,
    no_api=False,
):
    if date_range:
        update_after = convert_date_range(date_range=date_range)

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
                    if debug:
                        print("Using cache")
                    tmp_docs = result

    if not tmp_docs:  # If cache expired or results not yet cached
        if no_api:
            return

        tmp_docs = list_documents(
            category=category,
            location=location,
            updated_after=update_after,
            debug=debug,
        )

        if len(tmp_docs) == 0:  # if list of documents is empty
            return

        else:  # Cache documents
            tmp_docs = [doc.model_dump(mode="json") for doc in tmp_docs]

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

    if num_results:
        docs = tmp_docs[
            0 : max(1, num_results)
        ]  # Prevent removing all documents from the list
    else:
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

    if full_data:
        if view == "location":
            stats = count_location_values(full_data)
        elif view == "tags":
            stats = count_tag_values(full_data)
        else:
            stats = count_category_values(full_data)

        print_view_results(stats=stats, view=view)
    else:
        raise print("Library is empty.")


@click.command(help="Add Document")
@click.argument("url")
@click.option("--debug", is_flag=True, default=False, hidden=True)
def add(url, debug=False):
    response = add_document(doc_info=DocumentInfo(url=url), debug=debug)
    if response.status_code == 200:
        secho(f"Already Exists.", fg="yellow")
    else:
        secho(f"Added!", fg="bright_green")


@click.command(help="Upload Reading List File")
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--file-type", type=click.Choice(["html", "csv"]), default="html")
@click.option("--debug", is_flag=True, default=False, hidden=True)
def upload(input_file, file_type, debug=False):
    click.echo(f"Adding Document(s) from: {input_file}")

    reading_list = build_reading_list(input_file=input_file, file_type=file_type)

    batch_add_documents(reading_list, debug=debug)


@click.command(help="Validate token")
@click.argument("token", type=str)
@click.option("--debug", is_flag=True, default=False, hidden=True)
def validate(token, debug=False):
    is_valid = validate_token(token=token, debug=debug)
    if is_valid:
        secho("Token is valid", fg="bright_green")
