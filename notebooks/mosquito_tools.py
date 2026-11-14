"""Functions for my Winnipeg mosquito story.

Each function is here because I needed it more than once: on both datasets, on
every new season's data, or in more than one chapter.
"""
from pathlib import Path

import pandas as pd


def count_repeats(df, columns):
    """Count the rows whose values in `columns` appear more than once.

    0 means one row per combination of `columns`: the check of what one row is.

    Used on: the trap counts and the weather (02-clean), and every release in
    load_releases.
    """
    return int(df.duplicated(subset=columns, keep=False).sum())


def unmatched(left, right, on):
    """Return the `on` values in `left` that have no row in `right`, sorted.

    Used in: 02-clean, for count days with no weather, and for summers with no
    spring rain total.
    """
    keys = set(right[on])
    return sorted(v for v in left[on].unique() if v not in keys)
