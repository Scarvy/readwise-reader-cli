"""Provides code to fetch all documents, notes, and highlights from a user's Reader Library."""

import json
import os
from datetime import datetime, timedelta
from typing import List

from xdg_base_dirs import xdg_data_home

from .api import list_documents
from .models import DocumentInfo

CACHE_DIR = xdg_data_home() / "reader"
CACHED_RESULT_PATH = CACHE_DIR / "full_library.json"
CACHE_EXPIRATION = 1  # Day


def fetch_full_library() -> List[DocumentInfo] | None:
    """Fetch the full library including documents, notes, and highlights.

    Returns:
        List[Dict[str, int]]: Full list of document information from a user's Reader library
    """

    tmp_library = None

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    if os.path.exists(CACHED_RESULT_PATH):
        with open(CACHED_RESULT_PATH, "r") as f:
            json_file = json.load(f)
            result = json_file.get(today)
            if result:
                t = result[-1].get("time")
                time = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
                diff = datetime.now() - time
                if diff < timedelta(days=CACHE_EXPIRATION):
                    tmp_library = result

    if not tmp_library:
        tmp_library = (
            list_documents()
        )  # fetch full library including all documents, notes, and highlights

        if len(tmp_library) == 0:  # if library is empty
            return None

        else:  # Cache documents
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

    full_library = tmp_library[:-1]

    return full_library
