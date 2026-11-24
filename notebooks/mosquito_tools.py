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


def ranked_bars(ax, values, title, xlabel):
    """Draw `values` (a Series) as horizontal bars on `ax`, largest at the top.

    Used in: chapter 1 and chapter 2 (03-story).
    From: my A2 report's Q1 chart; the data, title and label are parameters now.
    """
    ordered = values.sort_values()
    ax.barh(ordered.index.astype(str), ordered.values, color="#4a6b8a")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    return ax


def side_averages(daily, sides):
    """Average mosquitoes per trap for each side of the city, labelled for a chart.

    `sides` maps each column in `daily` to the name to show, for example
    {"north_west": "North West"}.

    Used in: chapter 2's chart and the key numbers (03-story).
    """
    averages = daily[list(sides)].mean()
    return averages.rename(index=sides)


def is_wet(seasons, wet_mm):
    """True for each summer whose May and June rain was `wet_mm` or more.

    Used in: chapter 3's chart (the colours) and the key numbers.
    """
    return seasons["spring_precip_mm"] >= wet_mm


def key_numbers(seasons, daily, wet_mm, sides):
    """Every number the story quotes, as one labelled Series.

    Run it before and after each new season and compare: anything that moved
    is a sentence to reread.

    Used in: the key numbers cell (03-story), at every rerun.
    """
    wet = is_wet(seasons, wet_mm)
    avg = seasons["season_avg"]
    top5 = avg.nlargest(5).index
    wettest = seasons["spring_precip_mm"].idxmax()
    side = side_averages(daily, sides)
    worst_day = daily.loc[daily["city_avg"].idxmax()]
    return pd.Series({
        "summers": f"{seasons.index.min()} to {seasons.index.max()} ({len(seasons)})",
        "count days per summer": f"{seasons['count_days'].min()} to {seasons['count_days'].max()}",
        "worst summer": f"{avg.idxmax()} ({avg.max():.1f} per trap)",
        "quietest summer": f"{avg.idxmin()} ({avg.min():.1f} per trap)",
        "worst day": f"{worst_day['date'].date()} ({worst_day['city_avg']:.0f} per trap)",
        "peaks in June or July": f"{seasons['peak_date'].dt.month.isin([6, 7]).sum()} of {len(seasons)}",
        "buggiest side": f"{side.idxmax()} ({side.max():.1f})",
        "quietest side": f"{side.idxmin()} ({side.min():.1f})",
        "wet springs": f"{wet.sum()}, {wet[top5].sum()} of them in the five buggiest summers",
        "wet vs dry summers": f"{avg[wet].mean():.1f} vs {avg[~wet].mean():.1f} per trap",
        "rain and mosquitoes, correlation": f"{avg.corr(seasons['spring_precip_mm']):.2f}",
        "wettest spring": f"{wettest} ({seasons.loc[wettest, 'spring_precip_mm']:.0f} mm)",
        "its summer": (f"rank {int(avg.rank(ascending=False)[wettest])}, average {avg[wettest]:.1f}, "
                       f"peak {seasons.loc[wettest, 'peak']:.0f}"),
    }, name="key number")


def load_releases(paths, key):
    """Read every file in `paths`, in order, and stack them into one DataFrame.

    Stops if a `key` combination (for example a date) appears in two files,
    because then one release overlaps another and would double count.

    Used in: 02-clean, for the trap counts and for the weather.
    """
    paths = [Path(p) for p in paths]
    if not paths:
        raise FileNotFoundError("No files to read")
    combined = pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)
    repeats = count_repeats(combined, key)
    if repeats > 0:
        raise ValueError(f"{repeats} rows repeat across files")
    print(f"{len(paths)} file(s), {len(combined)} rows")
    return combined
def rain_scatter(ax, seasons, wet_mm, title):
    """Spring rain against mosquitoes per trap, one labelled dot per summer, on `ax`.

    Wet springs (`wet_mm` or more) are green, with a dashed line at the threshold.

    Used in: chapter 3 and the README figure (03-story).
    """
    wet = is_wet(seasons, wet_mm)
    ax.scatter(seasons["spring_precip_mm"], seasons["season_avg"],
               c=wet.map({True: "#2f6f4f", False: "#9a9a92"}), s=60)
    for year, row in seasons.iterrows():
        ax.annotate(str(year), (row["spring_precip_mm"], row["season_avg"]),
                    xytext=(5, 3), textcoords="offset points")
    ax.axvline(wet_mm, color="#9a9a92", linestyle="--", linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("Rain in May and June (mm)")
    ax.set_ylabel("Mosquitoes per trap per count day")
    return ax
