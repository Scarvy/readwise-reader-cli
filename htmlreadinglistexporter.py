import datetime as dt

from pandas import DataFrame
from bs4 import BeautifulSoup

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

with open("ReadingList.html", "r") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

reading_list_contents = [
    {"title": link.text, "url": link.get("href")} for link in soup.find_all("a")
]

reading_list = DataFrame.from_dict(reading_list_contents)
reading_list.to_csv("reading_list.csv")
