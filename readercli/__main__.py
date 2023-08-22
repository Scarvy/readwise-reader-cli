"""The main CLI module of readercli"""
import click

from .api import fetch_documents
from .layout import table_layout
from .constants import VALID_CATEGORY_OPTIONS, VALID_LOCATION_OPTIONS

DEFAULT_CATEGORY_NAME = "all"


@click.command()
@click.option(
    "--location",
    "-l",
    default="archive",
    show_default=True,
    type=click.Choice(VALID_LOCATION_OPTIONS, case_sensitive=False),
    help="Document(s) location: `new`, `later`, `archive`, `feed`",
)
@click.option(
    "--days",
    "-d",
    default=1,
    show_default=True,
    help="Updated after in days.",
)
@click.option(
    "--category",
    "-c",
    type=click.Choice(VALID_CATEGORY_OPTIONS, case_sensitive=False),
    help="Document(s) category: `article`, `email`, `rss`, `highlight`, `note`, `pdf`, `epub`, `tweet`, `video`",
)
def cli(location, category, days):
    option_key = f"{location}_{(category := category if category else DEFAULT_CATEGORY_NAME)}_{days}"
    click.echo(option_key)

    full_data = fetch_documents(
        updated_after=days, location=location, category=category
    )
    table_layout(full_data)


if __name__ == "__main__":
    cli()
