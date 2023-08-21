"""The main CLI module of readercli"""
import click


from .api import fetch_documents
from .layout import table_layout


@click.command()
@click.option(
    "--location",
    "-l",
    type=str,
    default=["archive"],
    help="Document(s) location: `new`, `later`, `archive`, `feed`",
)
def cli(location):
    full_data = fetch_documents(location=location)
    table_layout(full_data)


if __name__ == "__main__":
    cli()
