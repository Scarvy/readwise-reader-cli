"""The main CLI module of readercli"""
import click
from . import commands


@click.group(help="Interact with your Reader Library")
def cli():
    pass


# Commands
cli.add_command(commands.list)  # List command
cli.add_command(commands.add)  # Add command
cli.add_command(commands.upload)  # Upload command

if __name__ == "__main__":
    cli()
