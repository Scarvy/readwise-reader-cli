"""The main CLI module of readercli"""
import click


from .api import fetch_documents
from .layout import table_layout


@click.command()
@click.option(
    "--location",
    "-l",
    type=str,
    default="archive",
    show_default=True,
    help="Document(s) location: `new`, `later`, `archive`, `feed`",
)
@click.option(
    "--days",
    "-d",
    default=1,
    show_default=True,
    help="Updated after in days.",
)
def cli(location, days):
    full_data = fetch_documents(updated_after=days, location=location)
    table_layout(full_data)


if __name__ == "__main__":
    cli()
