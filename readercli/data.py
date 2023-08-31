"""Provides code to fetch all documents, notes, and highlights from a user's Reader Library."""

import json
import os
from datetime import datetime, timedelta

from xdg_base_dirs import xdg_data_home

from readercli.api import APIHandler


CACHE_DIR = xdg_data_home() / "reader"
CACHED_RESULT_PATH = CACHE_DIR / "full_library.json"
CACHE_EXPIRATION = 1  # Day


def fetch_full_library() -> list[dict] | None:
    """Fetch the full library including documents, notes, and highlights.

    Returns:
        full_library (list[dict] | None): full library data or None
    """

    tmp_library = None

    today = datetime.strftime(datetime.now(), format="%Y-%m-%d")

    if os.path.exists(CACHED_RESULT_PATH):
        with open(CACHED_RESULT_PATH, "r") as f:
            json_file = json.load(f)
            result = json_file.get(today)
            if result:
                t = result[-1].get("time")
                time = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
                diff = datetime.now() - time
                if diff < timedelta(days=CACHE_EXPIRATION):
                    print("Using cache instead!")
                    tmp_library = result

    else:
        api = APIHandler()

        tmp_library = (
            api.fetch_documents()
        )  # fetch full library including all documents, notes, and highlights

        if len(tmp_library) == 0:  # if library is empty
            return

        tmp_library.append({"time": str(datetime.now())})
        os.makedirs(CACHE_DIR, exist_ok=True)

        with open(CACHED_RESULT_PATH, "a+") as f:
            if os.path.getsize(CACHED_RESULT_PATH) == 0:  # file is empty
                result_dict = {today: tmp_library}
                f.write(json.dumps(result_dict, indent=4))
            else:
                f.seek(0)
                result_dict = json.load(f)
                result_dict[today] = tmp_library
                f.truncate(0)
                f.write(json.dumps(result_dict, indent=4))

    full_library = tmp_library[:-1]

    return full_library
