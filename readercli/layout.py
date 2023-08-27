"""Provides code to print layouts to the command-line."""

from datetime import datetime

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
    "feed": ":newspaper2-emoji: feed",
}


def format_reading_progress(reading_progress: float) -> str:
    """Format reading progress percentage"""

    percentage_str = f"{round(reading_progress * 100, 2)}%"
    return percentage_str


def format_published_date(timestamp_miliseconds: float) -> datetime:
    """Format published date of a document"""

    timestamp_seconds = timestamp_miliseconds / 1_000  # Convert microseconds to seconds

    datetime_obj = datetime.fromtimestamp(timestamp_seconds)

    return datetime_obj.strftime("%Y-%m-%d")


def table_layout(documents, category):
    """Displays documents in a table format using rich"""

    table = Table(leading=1)

    if category in ["note", "highlight"]:
        table.add_column(":link: Highlight Link")
        table.add_column(":file_folder: Category", justify="center")
        table.add_column(":clipboard: Content")
        table.add_column(":label: Tags")
        table.add_column(":world_map: Location", justify="center")
        table.add_column(":clock1: Last Update", justify="right")

        for document in documents:
            category = (
                emoji_mapping_category[document["category"]]
                if document["category"]
                else Text("no category", style="italic")
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

            last_update = Text(document["updated_at"][:10], no_wrap=True)

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

            last_update = Text(document["updated_at"][:10], no_wrap=True)

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


def print_layout(*args, layout="table", category=None):
    """Use specified layout"""
    if layout == "list":
        list_layout(*args, category=category)
    elif layout == "table":
        table_layout(*args, category=category)
    else:
        table_layout(*args, category=category)


if __name__ == "__main__":
    documents = [
        {
            "id": "01h8707jqgjsfzznh281xxashb",
            "url": "https://read.readwise.io/read/01h8707jqgjsfzznh281xxashb",
            "title": "Large language models, explained with a minimum of math and jargon",
            "author": "Timothy B Lee",
            "source": None,
            "category": "article",
            "location": "new",
            "tags": {
                "shortlist": {
                    "name": "shortlist",
                    "type": "manual",
                    "created": 1692640034398,
                }
            },
            "site_name": "understandingai.org",
            "word_count": 6117,
            "created_at": "2023-08-19T13:37:24.567027+00:00",
            "updated_at": "2023-08-21T18:34:24.731100+00:00",
            "published_date": 1690416000000,
            "summary": "Want to really understand how large language models work? Here’s a gentle primer.",
            "image_url": "https://substackcdn.com/image/fetch/w_1200,h_600,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc3e159bd-1228-4205-b1eb-5898ab9172d3_1600x856.png",
            "content": None,
            "source_url": "https://link.sbstck.com/redirect/08f86d22-19a6-4cc1-b449-0eebe03603dd?j=eyJ1IjoiY2gzcTgifQ.mfKJkm1MFmHg0LGeKdRGUAyRwWsVKwDUCVREGN0XyUw",
            "notes": "A model so vast,\nWords flow like a river wide,\nIntelligence reigns.",
            "parent_id": None,
            "reading_progress": 0.035575772085228635,
        },
        {
            "id": "01h7jnwdem0v454jfz6jt3999z",
            "url": "https://read.readwise.io/read/01h7jnwdem0v454jfz6jt3999z",
            "title": "Python Design Patterns¶",
            "author": "python-patterns.guide",
            "source": "Readwise web highlighter",
            "category": "article",
            "location": "new",
            "tags": {
                "python": {
                    "name": "Python",
                    "type": "manual",
                    "created": 1691770320268,
                },
                "resources": {
                    "name": "resources",
                    "type": "manual",
                    "created": 1691770341678,
                },
                "shortlist": {
                    "name": "shortlist",
                    "type": "manual",
                    "created": 1691771937889,
                },
                "programming": {
                    "name": "programming",
                    "type": "manual",
                    "created": 1691770334734,
                },
                "design-patterns": {
                    "name": "design-patterns",
                    "type": "manual",
                    "created": 1691770329111,
                },
            },
            "site_name": "python-patterns.guide",
            "word_count": 118,
            "created_at": "2023-08-11T16:11:45.191410+00:00",
            "updated_at": "2023-08-16T23:29:30.819847+00:00",
            "published_date": None,
            "summary": "I’m Brandon Rhodes (website, Twitter) and this is my evolving guide to design patterns in the Python programming language.",
            "image_url": "",
            "content": None,
            "source_url": "https://python-patterns.guide/",
            "notes": "",
            "parent_id": None,
            "reading_progress": 1,
        },
        {
            "id": "01h7gwmcthew5qn35wvdkpv8aj",
            "url": "https://read.readwise.io/read/01h7gwmcthew5qn35wvdkpv8aj",
            "title": "Python Command-Line Arguments",
            "author": "Real Python",
            "source": "Readwise web highlighter",
            "category": "article",
            "location": "new",
            "tags": {
                "shortlist": {
                    "name": "shortlist",
                    "type": "manual",
                    "created": 1691725386688,
                }
            },
            "site_name": "realpython.com",
            "word_count": 12352,
            "created_at": "2023-08-10T23:31:12.964479+00:00",
            "updated_at": "2023-08-21T17:48:55.708477+00:00",
            "published_date": 1580860800000,
            "summary": "Python command-line arguments are the key to converting your programs into useful and enticing tools that are ready to be used in the terminal of your operating system. In this step-by-step tutorial, you'll learn their origins, standards, and basics, and how to implement them in your program.",
            "image_url": "https://files.realpython.com/media/Python-Command-Line-Arguments_Watermarked.33cee612a4ae.jpg",
            "content": None,
            "source_url": "https://realpython.com/python-command-line-arguments/",
            "notes": "",
            "parent_id": None,
            "reading_progress": 0.9019759274910384,
        },
        {
            "id": "01h65f74nbcywcc37v29rkymrj",
            "url": "https://read.readwise.io/read/01h65f74nbcywcc37v29rkymrj",
            "title": "RESTful Web Services",
            "author": "Leonard Richardson",
            "source": "File Upload",
            "category": "pdf",
            "location": "new",
            "tags": {
                "url": {"name": "URL", "type": "manual", "created": 1690397218500},
                "xml": {"name": "XML", "type": "manual", "created": 1690397222773},
                "http": {"name": "HTTP", "type": "manual", "created": 1690397212606},
                "reading": {
                    "name": "reading",
                    "type": "manual",
                    "created": 1691725499900,
                },
                "shortlist": {
                    "name": "shortlist",
                    "type": "manual",
                    "created": 1691725489429,
                },
                "restful-api": {
                    "name": "RESTful-API",
                    "type": "manual",
                    "created": 1690397205219,
                },
            },
            "site_name": "readwise.io",
            "word_count": 152889,
            "created_at": "2023-07-25T02:49:27.806466+00:00",
            "updated_at": "2023-08-21T18:34:54.375418+00:00",
            "published_date": 1297900800000,
            "summary": "",
            "image_url": "",
            "content": None,
            "source_url": "https://readwise.io/reader/document_raw_content/68888514",
            "notes": "",
            "parent_id": None,
            "reading_progress": 0.033482142857142856,
        },
        {
            "id": "01h65f6zw9y1b0kx4png80mmv1",
            "url": "https://read.readwise.io/read/01h65f6zw9y1b0kx4png80mmv1",
            "title": "Web API Design",
            "author": "Helen Whelan",
            "source": "File Upload",
            "category": "pdf",
            "location": "new",
            "tags": {
                "api": {"name": "API", "type": "manual", "created": 1690397106792},
                "web": {"name": "Web", "type": "manual", "created": 1690397114367},
                "ebook": {"name": "ebook", "type": "manual", "created": 1690397149271},
                "shortlist": {
                    "name": "shortlist",
                    "type": "manual",
                    "created": 1691725432090,
                },
            },
            "site_name": "readwise.io",
            "word_count": 7661,
            "created_at": "2023-07-25T02:49:21.239292+00:00",
            "updated_at": "2023-08-21T18:34:50.675757+00:00",
            "published_date": 1332288000000,
            "summary": "",
            "image_url": "",
            "content": None,
            "source_url": "https://readwise.io/reader/document_raw_content/74070770",
            "notes": "",
            "parent_id": None,
            "reading_progress": 0.6842105263157895,
        },
        {
            "id": "01h8ajwcytqbhv627ag9cg2a01",
            "url": "https://read.readwise.io/read/01h8ajwcytqbhv627ag9cg2a01",
            "title": None,
            "author": None,
            "source": None,
            "category": "highlight",
            "location": "later",
            "tags": None,
            "site_name": None,
            "word_count": 0,
            "created_at": "2023-08-20T23:01:04.928012+00:00",
            "updated_at": "2023-08-20T23:01:04.928026+00:00",
            "published_date": None,
            "summary": None,
            "image_url": None,
            "content": "Almost two-thirds of respondents said their APIs generate revenue. Of those respondents, 43% said APIs generate over a quarter of company revenue. In the financial services and advertising, API revenue was closely measured. It was judged the second-most important metric of public API success, just after usage.",
            "source_url": None,
            "notes": "",
            "parent_id": "01h8ajqppjyrwfa8gvw1gg3x8a",
            "reading_progress": 0,
        },
    ]

    notes = [
        {
            "id": "01h7mzsn5tbe0bjqnr3gmj2bv9",
            "url": "https://read.readwise.io/read/01h7mzsn5tbe0bjqnr3gmj2bv9",
            "title": None,
            "author": None,
            "source": "reader-mobile-app",
            "category": "note",
            "location": None,
            "tags": None,
            "site_name": None,
            "word_count": None,
            "created_at": "2023-08-12T13:43:28.919967+00:00",
            "updated_at": "2023-08-12T13:43:28.919980+00:00",
            "published_date": None,
            "summary": None,
            "image_url": None,
            "content": "Pragmatism is a philosophical approach that emphasizes practicality and usefulness over abstract theories or principles. It originated in the United States in the late 19th century and was developed by philosophers such as William James and John Dewey. Pragmatists believe that the value of an idea or belief lies in its ability to solve problems and improve people's lives. They emphasize experimentation, observation, and experience as the basis for knowledge and reject the idea of absolute truth or certainty. Pragmatism has had a significant influence on American culture and has been applied in fields such as education, politics, and business.",
            "source_url": None,
            "notes": "",
            "parent_id": "01h7mzsdxnr5jhkk9phq4e7r6f",
            "reading_progress": 0,
        },
        {
            "id": "01h5fkadcpf5ea8srh9y1b9ws6",
            "url": "https://read.readwise.io/read/01h5fkadcpf5ea8srh9y1b9ws6",
            "title": None,
            "author": None,
            "source": "reader-web-app",
            "category": "note",
            "location": None,
            "tags": None,
            "site_name": None,
            "word_count": None,
            "created_at": "2023-07-16T14:58:36.391838+00:00",
            "updated_at": "2023-07-16T14:58:36.391851+00:00",
            "published_date": None,
            "summary": None,
            "image_url": None,
            "content": "Write for a particular person in mind",
            "source_url": None,
            "notes": "",
            "parent_id": "01h5fk9y1shfjvvvtr7z0hvc9n",
            "reading_progress": 0,
        },
        {
            "id": "01h8m0et3vf7f3a0c7nbmhkxjg",
            "url": "https://read.readwise.io/read/01h8m0et3vf7f3a0c7nbmhkxjg",
            "title": None,
            "author": None,
            "source": "reader-web-app",
            "category": "note",
            "location": "later",
            "tags": None,
            "site_name": None,
            "word_count": 0,
            "created_at": "2023-08-24T14:51:29.042109+00:00",
            "updated_at": "2023-08-24T14:51:29.042125+00:00",
            "published_date": None,
            "summary": None,
            "image_url": None,
            "content": 'Begets: "Begets" is a verb that means to cause or bring about something. It is often used in the context of a negative cycle or pattern that perpetuates itself, such as "violence begets violence" or "ignorance begets ignorance." In programming, the phrase "bad code begets bad code" suggests that poorly written code can lead to more poorly written code, creating a cycle of inefficiency and difficulty in maintaining the program.',
            "source_url": None,
            "notes": "",
            "parent_id": "01h8m0eks760p1bj583wf9jcas",
            "reading_progress": 0,
        },
        {
            "id": "01h8jjvrk39s3hhvc3wf7ns1d4",
            "url": "https://read.readwise.io/read/01h8jjvrk39s3hhvc3wf7ns1d4",
            "title": None,
            "author": None,
            "source": "reader-mobile-app",
            "category": "note",
            "location": "later",
            "tags": None,
            "site_name": None,
            "word_count": 0,
            "created_at": "2023-08-24T01:34:39.239540+00:00",
            "updated_at": "2023-08-24T01:34:39.239552+00:00",
            "published_date": None,
            "summary": None,
            "image_url": None,
            "content": "Sentry is a tool that helps developers fix problems with their computer programs. It tells them when something is wrong with the code and helps them figure out what caused the problem. Sentry can also track the health of different parts of the program and can help find the root cause of issues. This is important because programs are becoming more complex and it's harder for developers to keep track of everything. With Sentry, developers can make sure the program is working properly and giving customers a good experience.",
            "source_url": None,
            "notes": "",
            "parent_id": "01h8jjvevyktpjpsb0pkf0edmy",
            "reading_progress": 0,
        },
    ]

    highlights = [
        {
            "id": "01h7mzsdxnr5jhkk9phq4e7r6f",
            "url": "https://read.readwise.io/read/01h7mzsdxnr5jhkk9phq4e7r6f",
            "title": None,
            "author": None,
            "source": "reader-mobile-app",
            "category": "highlight",
            "location": None,
            "tags": {},
            "site_name": None,
            "word_count": None,
            "created_at": "2023-08-12T13:43:21.391437+00:00",
            "updated_at": "2023-08-12T13:43:28.966254+00:00",
            "published_date": None,
            "summary": None,
            "image_url": None,
            "content": "pragmatism",
            "source_url": None,
            "notes": "",
            "parent_id": "01h7mqyeq11jt98epzcfbpde9e",
            "reading_progress": 0,
        },
        {
            "id": "01h8ppzy1frk0e7gpheef5n177",
            "url": "https://read.readwise.io/read/01h8ppzy1frk0e7gpheef5n177",
            "title": None,
            "author": None,
            "source": "reader-web-app",
            "category": "highlight",
            "location": "later",
            "tags": {
                "funny": {"name": "funny", "type": "manual", "created": 1692979442334},
                "cartoon": {
                    "name": "cartoon",
                    "type": "manual",
                    "created": 1692979444972,
                },
                "drawing": {
                    "name": "drawing",
                    "type": "manual",
                    "created": 1692979447744,
                },
            },
            "site_name": None,
            "word_count": 0,
            "created_at": "2023-08-25T16:03:47.588823+00:00",
            "updated_at": "2023-08-25T16:04:08.343874+00:00",
            "published_date": None,
            "summary": None,
            "image_url": None,
            "content": "\n\n\n\n",
            "source_url": None,
            "notes": "",
            "parent_id": "01h8p7edag0ax4hnx4ks8vw8he",
            "reading_progress": 0,
        },
        {
            "id": "01h8pprff81qa4n10bfxkyc3nk",
            "url": "https://read.readwise.io/read/01h8pprff81qa4n10bfxkyc3nk",
            "title": None,
            "author": None,
            "source": "reader-web-app",
            "category": "highlight",
            "location": "later",
            "tags": {
                "stoic": {"name": "stoic", "type": "manual", "created": 1692979205575},
                "marcus-aurelius": {
                    "name": "marcus-aurelius",
                    "type": "manual",
                    "created": 1692979201653,
                },
            },
            "site_name": None,
            "word_count": 0,
            "created_at": "2023-08-25T15:59:43.430440+00:00",
            "updated_at": "2023-08-25T16:00:05.956298+00:00",
            "published_date": None,
            "summary": None,
            "image_url": None,
            "content": "character is fate.",
            "source_url": None,
            "notes": "",
            "parent_id": "01h8nzjf1sgrpgp4zk58d9zhw6",
            "reading_progress": 0,
        },
    ]

    # notes and highlights layout option
    print_layout(documents, layout="table", category=None)
    print_layout(highlights, layout="table", category="highlight")
    print_layout(notes, layout="table", category="note")
