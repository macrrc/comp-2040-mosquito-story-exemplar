# Assignment 1: Winnipeg Mosquito Trap Counts

**The dataset:** *Daily Adult Mosquito Trap Data*, City of Winnipeg Open Data, https://data.winnipeg.ca/d/du7c-8488.
Exported 2026-09-13 with a filter for complete seasons, 2015 to 2025 (the 2026 season was still being counted).
Open Government Licence - Winnipeg.

**One row** is one count day: the average number of adult mosquitoes per trap across the city, for each quadrant,
and for each trap. 880 count days.

**My questions:** which summers are the worst? When in the summer is it worst? Which side of the city is buggiest?

**Main cleaning decisions:** dates read day first; `no data` in the trap columns made a real missing value; nothing
dropped. Details in `02-prep.ipynb`.

**How to run:** Restart & Run All in `01-first-look.ipynb`, then `02-prep.ipynb` (writes `data/clean/traps-clean.csv`).
