"""Provides code to fetch all documents, notes, and highlights from a user's Reader Library."""

import json
import os
from datetime import datetime, timedelta
from typing import List, Optional

from xdg_base_dirs import xdg_data_home

from .api import list_documents
from .models import DocumentInfo

CACHE_DIR = xdg_data_home() / "reader"
CACHED_RESULT_PATH = CACHE_DIR / "full_library.json"
CACHE_EXPIRATION = 1  # Day


def todays_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")


def load_library(date: str) -> List[dict]:
    with open(CACHED_RESULT_PATH, "r") as f:
        json_file = json.load(f)
        return json_file.get(date)


def get_cache_time(cache: list[dict]) -> datetime | None:
    t = cache[-1].get("time")
    if t:
        return datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
    return t


def use_cache(t: datetime) -> bool:
    diff = datetime.now() - t
    if diff < timedelta(days=CACHE_EXPIRATION):
        return True
    return False


def fetch_full_library(debug=False) -> Optional[List[DocumentInfo]]:
    """Fetch the full library including documents, notes, and highlights.

    Returns:
        List[DocumentInfo]: A list of `DocumentInfo` objects.
    """

    tmp_library: Optional[List[DocumentInfo]] = None

    today = todays_date()

    if os.path.exists(CACHED_RESULT_PATH):
        result = load_library(date=today)
        if result:
            time = get_cache_time(cache=result)
            if not time:
                raise ValueError(time)
            if use_cache(t=time):
                if debug:
                    print("Using cache")
                tmp_library = [DocumentInfo(**doc_info) for doc_info in result[:-1]]

    if tmp_library is None:
        tmp_library = list_documents(
            debug=debug
        )  # fetch full library including all documents, notes, and highlights

        if tmp_library is None or len(tmp_library) == 0:
            return tmp_library
        else:
            tmp_library_json = [doc.model_dump(mode="json") for doc in tmp_library]

            tmp_library_json.append({"time": str(datetime.now())})
            os.makedirs(CACHE_DIR, exist_ok=True)

        with open(CACHED_RESULT_PATH, "a+") as f:
            if os.path.getsize(CACHED_RESULT_PATH) == 0:  # file is empty
                result_dict = {today: tmp_library_json}
                f.write(json.dumps(result_dict, indent=4))
            else:
                f.seek(0)
                result_dict = json.load(f)
                result_dict[today] = tmp_library_json
                f.truncate(0)
                f.write(json.dumps(result_dict, indent=4))

    full_library = tmp_library

    return full_library
