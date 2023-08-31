"""Provides code to print layouts to the command-line."""

from datetime import datetime
from dateutil import tz, parser

from rich.align import Align
from rich.console import Console, group
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

console = Console()

emoji_mapping_category = {
    "article": ":newspaper-emoji: article",
    "email": ":envelope-emoji: email",
    "rss": ":satellite_antenna-emoji: rss",
    "highlight": ":crayon-emoji: highlight",
    "note": ":memo-emoji: note",
    "pdf": ":page_facing_up-emoji: pdf",
    "epub": ":book-emoji: epub",
    "tweet": ":bird-emoji: tweet",
    "video": ":video_camera-emoji: video",
}

emoji_mapping_location = {
    "new": ":star-emoji: new",
    "later": ":clock2-emoji: later",
    "archive": ":file_cabinet-emoji: archive",
    "feed": ":inbox_tray-emoji: feed",
}

emoji_mapping = {
    "category": emoji_mapping_category,
    "location": emoji_mapping_location,
}


def format_reading_progress(reading_progress: float) -> str:
    """Format reading progress percentage"""

    percentage_str = f"{round(reading_progress * 100, 2)}%"
    return percentage_str


def format_published_date(timestamp_miliseconds: float) -> datetime:
    """Format published date of a document"""

    timestamp_seconds = timestamp_miliseconds / 1_000  # Convert microseconds to seconds

    datetime_obj = datetime.fromtimestamp(timestamp_seconds, tz=tz.tzlocal())

    return datetime_obj.strftime("%Y-%m-%d")


def format_updated_at_date(updated_at: str) -> str:
    """Format updated at date"""

    parsed_time = parser.isoparse(updated_at)

    local_time = parsed_time.astimezone(tz.tzlocal())

    return local_time.strftime("%Y-%m-%d")


def table_layout(documents, category=""):
    """Displays documents in a table format using rich"""

    table = Table(leading=1)

    if category in ("note", "highlight"):
        table.add_column(":link: Highlight Link")
        table.add_column(":file_folder: Category", justify="center")
        table.add_column(":clipboard: Content")
        table.add_column(":label: Tags")
        table.add_column(":world_map: Location", justify="center")
        table.add_column(":clock1: Last Update", justify="right")

        for document in documents:
            category = (
                emoji_mapping_category[document["category"]]
                if document["location"]
                else ":x: category"
            )
            content = Text(document["content"], style="#e4938e")

            title = Text("link", style="#FFE761")
            title.stylize(f"#FFE761 link {document['url']}")

            if document["tags"]:
                tags = list(document["tags"].keys())
                tags = ", ".join([tag for tag in tags])

                tags = Text(tags, style="#5278FE")
            else:
                tags = ":x: tags"

            location = (
                emoji_mapping_location[document["location"]]
                if document["location"]
                else ":x: None"
            )

            last_update = Text(
                format_updated_at_date(document["updated_at"]), no_wrap=True
            )

            table.add_row(
                title,
                category,
                content,
                tags,
                location,
                last_update,
            )

    else:
        # make the columns
        table.add_column(":bookmark: Title")
        table.add_column(":bust_in_silhouette: Author")
        table.add_column(":file_folder: Category", justify="center")
        table.add_column(":clipboard: Summary")
        table.add_column(":label: Tags")
        table.add_column(":world_map: Location", justify="center")
        table.add_column(":hourglass: Reading Progress", justify="right")
        table.add_column(":clock1: Last Update", justify="right")

        for document in documents:
            if (
                document["category"] == "highlight" or document["category"] == "note"
            ):  # skip highlights and notes
                continue
            author = (
                Text(document["author"])
                if document["author"]
                else Text("no author", style="italic #EF476F")
            )
            category = (
                emoji_mapping_category[document["category"]]
                if document["category"]
                else Text("no category", style="italic")
            )
            summary = (
                Text(document["summary"], style="#e4938e")
                if document["summary"]
                else ":x: no summary"
            )

            reading_progress = Text(
                format_reading_progress(document["reading_progress"]),
                style="bold #06D6A0",
            )

            title = (
                Text(document["title"], style="#FFE761")
                if document["title"]
                else Text("no title", style="italic #FFE761")
            )
            title.stylize(f"#FFE761 link {document['url']}")

            if document["tags"]:
                tags = list(document["tags"].keys())
                tags = ", ".join([tag for tag in tags])

                tags = Text(tags, style="#5278FE")
            else:
                tags = ":x: tags"

            location = (
                emoji_mapping_location[document["location"]]
                if document["location"]
                else ":x: None"
            )

            last_update = Text(
                format_updated_at_date(document["updated_at"]), no_wrap=True
            )

            table.add_row(
                title,
                author,
                category,
                summary,
                tags,
                location,
                reading_progress,
                last_update,
            )

    console.print(table)


def list_layout(documents, category=None):
    """Display documents in a list layout using rich"""

    width = 88

    @group()
    def render_document(document):
        """Yields renderables for a single document."""
        yield Rule(style="#FFE761")
        yield ""
        # Table with summary and reading progress
        title_table = Table.grid(padding=(0, 1))
        title_table.expand = True
        title = Text(document["title"], overflow="fold", style="#FFE761")
        title.stylize(f"#FFE761 link {document['url']}")

        reading_progress = format_reading_progress(document["reading_progress"])
        date_range_col = (
            format_published_date(document["published_date"])
            if document["published_date"]
            else "No Publish Date"
        )

        title_table.add_row(title, Text(reading_progress, style="italic #06D6A0"))
        title_table.columns[1].no_wrap = True
        title_table.columns[1].justify = "right"
        yield title_table
        yield ""
        summary_table = Table.grid(padding=(0, 1))
        summary_table.expand = True
        summary_col = (
            Text(document["summary"], style="#e4938e")
            if document["summary"]
            else Text("no summary")
        )
        summary_table.add_row(summary_col, date_range_col)
        summary_table.columns[1].justify = "right"
        yield summary_table
        yield ""
        # tags
        tags = list(document["tags"].keys())
        tags = ", ".join([tag for tag in tags])

        if tags:
            yield Text(tags, style="#5278FE")
        else:
            yield Text("No tags", style="italic")
        yield ""

    def column(renderable):
        """Constrain width and align to center to create a column."""
        return Align.center(renderable, width=width, pad=False)

    for document in documents:
        if (
            document["category"] == "highlight" or document["category"] == "note"
        ):  # skip highlights and notes
            continue
        console.print(column(render_document(document)))
    console.print(column(Rule(style="#FFE761")))


def print_view_results(stats: dict, view: str = ""):
    emojis = emoji_mapping[view]

    table = Table(title=f"{view.title()} Breakdown")

    sorted_tag_counts = dict(
        sorted(stats.items(), key=lambda item: item[1], reverse=True)
    )

    table.add_column("Name", justify="left", no_wrap=True)
    table.add_column("Count", justify="right", style="cyan", no_wrap=True)

    for name, value in sorted_tag_counts.items():
        table.add_row(emojis[name], str(value))

    console = Console()
    console.print(table)


def print_results(docuemnts, page=False, layout="", category=""):
    """Use a layout to print or page the fetched documents"""
    if page:
        with console.pager(styles=True):
            print_layout(docuemnts, layout=layout, category=category)
        return
    print_layout(docuemnts, layout=layout, category=category)


def print_layout(documents, category="", layout="table"):
    """Use listed layout"""
    if layout == "list":
        list_layout(documents, category=category)
    else:
        table_layout(documents, category=category)


if __name__ == "__main__":
    category_view = {
        "highlight": 728,
        "pdf": 68,
        "note": 161,
        "video": 8,
        "article": 329,
        "tweet": 24,
        "email": 320,
        "epub": 4,
        "rss": 358,
    }

    location_view = {"new": 2, "archive": 1095, "feed": 13, "later": 147}

    print_view_results(category_view, view="category")
    print_view_results(location_view, view="location")
