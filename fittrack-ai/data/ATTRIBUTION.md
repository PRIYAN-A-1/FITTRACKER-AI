# Nutrition data attribution

This package intentionally includes a small reproducible catalog so manual logging does not depend on a remote food API on every search.

- **7,793 records**: USDA FoodData Central, SR Legacy April 2018. Public domain / CC0 1.0. Downloaded 13 October 2026. Source: https://fdc.nal.usda.gov/ . Archive: https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_sr_legacy_food_csv_2018-04.zip . SHA-256 is in `usda-catalog.report.json`.
- **66 records**: Open Food Facts, selected from 100 results for `idli`. Database license ODbL 1.0: https://opendatacommons.org/licenses/odbl/1-0/ . Source attribution: https://world.openfoodfacts.org/ . 34 records were rejected for missing/invalid nutrients, missing identity, or ambiguous volume basis. These are community-contributed packaged-product records, not verified universal recipes for homemade idli. Some may be mixes or batters: read the product name before logging.
- **7,859 unique source-qualified IDs** in `catalog.jsonl`. USDA and OFF source partitions remain available as separate files. The combined database is distributed under ODbL 1.0 with the underlying USDA facts remaining CC0. Preserve attribution, make applicable derivative databases available under ODbL, and review the license before distributing changes. Code is separate from the database license.
- No product photographs are included. The nutrition catalog is **not an image training dataset**.

Source-published measurements do not establish independent verification by FitTrack. Missing nutrients stay null; an actual zero stays zero. USDA coverage is broad but does not establish comprehensive Tamil or South Indian dish coverage. The data contains older source measurements; collection today does not make those measurements current.

## Refresh and source separation

The default runtime loads `catalog.jsonl`; replacing that file updates the source snapshot for future meals. Existing meal nutrition snapshots are preserved. Import only approved datasets into this operator-controlled file. Do not point the server at untrusted uploaded files.

For OFF updates, use the collector command in the README. Its output is a separate dataset; review the rejection report before combining it. Broader India collection was attempted but returned HTTP 503, so its count is zero and it is not represented as successful coverage.

Official source guidance checked during this build:
- https://fdc.nal.usda.gov/api-guide — CC0 licensing, API-key requirements.
- https://openfoodfacts.github.io/openfoodfacts-server/api/ — API and rate limits.
- https://wiki.openfoodfacts.org/Reusing_Open_Food_Facts_Data — database reuse.
