"""starcli.layouts"""

from rich.console import Console

from rich.table import Table
from rich.text import Text

console = Console()


def reading_progress_format(reading_progress: float) -> str:
    percentage_str = f"{round(reading_progress * 100, 2)}%"
    return percentage_str


def table_layout(documents):
    """Displays documents in a table format using rich"""

    table = Table(leading=1)

    # make the columns
    table.add_column("Title", style="bold yellow")
    table.add_column("Author")
    table.add_column("Category")
    table.add_column("Summary")
    table.add_column("Reading Progress")
    table.add_column("Tags")
    table.add_column("Location", justify="right")

    for document in documents:
        if (
            document["category"] == "highlight" or document["category"] == "note"
        ):  # skip highlights and notes
            continue
        author = (
            Text(document["author"], style="cyan")
            if document["author"]
            else Text("no author", style="italic")
        )
        category = (
            Text(document["category"], style="cyan")
            if document["category"]
            else Text("no category", style="italic")
        )
        summary = (
            Text(document["summary"])
            if document["summary"]
            else Text("no summary", style="italic")
        )

        reading_progress = (
            Text(reading_progress_format(document["reading_progress"]))
            if document["reading_progress"]
            else Text("no reading progress", style="italic")
        )

        title = (
            Text(document["title"])
            if document["title"]
            else Text("no title", style="italic")
        )
        title.stylize(f"yellow link {document['url']}")

        location = Text(document["location"], style="blue")

        tags = list(document["tags"].keys())
        tags = ", ".join([tag for tag in tags])

        tags = Text(tags, style="magenta") if tags else Text("No tags", style="italic")

        table.add_row(
            title, author, category, summary, reading_progress, tags, location
        )

    console.print(table)


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

    table_layout(documents=documents)
