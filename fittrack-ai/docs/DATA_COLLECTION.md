# Data collection and expansion

## Measured current state

| Dataset | Fetched | Accepted | Purpose |
|---|---:|---:|---|
| USDA SR Legacy official archive | 7,793 food records | 7,793 | Ingredient and food nutrient lookup |
| OFF idli search | 100 products | 66 | Packaged mixes, batters and meals; community data |
| Broader OFF India search | 0 | 0 | Attempt returned 503 |
| Consented training photos | 0 | 0 | Required before custom image model training |

No count here is a target disguised as a completed collection. Nutrition records do not substitute for food photos, and food photos do not establish nutrient composition.

## Next photo collection batch — targets, not collected results

Start with 20 locally useful classes, for example idli, plain dosa, masala dosa, uttapam, ven pongal, upma, medu vadai, sambar, rasam, coconut chutney, tomato chutney, curd rice, lemon rice, tomato rice, plain cooked rice, chapati, parotta, dal, chicken biryani and vegetable biryani. Have Tamil labels reviewed by a fluent annotator before adding aliases.

Aim initially for 150–300 independent photos per class, collected across at least 20 meal sessions per class and several venues/cameras. This is an initial planning range, not a guarantee of accuracy or sufficient coverage. Include low light, different plates, clutter, camera angles, food leftovers, visually similar foods, and an independent unknown/non-food evaluation set. Multi-dish plates need additional annotations and a detector/segmenter; this baseline classifier does not solve them.

Keep a consent reference for personal submissions, and a license URL/attribution record for open images. A public photo is not automatically licensed for training. Do not ingest restricted academic food datasets or social media photos without verifying rights. Product packaging photographs are not representative of home-cooked plates.

## Annotation and leakage

Each image manifest row records path, label, source URL, allowed license, meal-session group ID and consent/licensing reference. Validation checks file size, pixel count, decoding, root confinement and identity. Exact decoded duplicates are removed; duplicate images with conflicting labels stop the pipeline. Near duplicates using dHash and shared group IDs are joined into connected components before deterministic splitting. Hashing is a leakage-reduction heuristic; manually audit near duplicates and split statistics.

The near-duplicate comparison is quadratic and intended for an initial small collection, not millions of images. Replace with a reviewed indexed approach before scaling. Freeze each accepted manifest version; changed group composition may change its split. Collection quality takes priority over record count.

## Nutrition expansion

Add measured, properly licensed Indian food-composition records only after permission is clear. For cooked dishes, collect recipe ingredients, raw ingredient masses, cooked yield, oil/ghee amounts and serving mass. Calculate recipe nutrients from known ingredients; do not copy an arbitrary online calorie value or infer exact grams from one photo. Tamil names and serving weights require human review.

The current OFF filter excludes likely liquid products. Records that remain are community values and may still have unit or food-state errors. Review before presenting a record as verified. USDA is source-published historical data and regional coverage remains incomplete.

## More collection commands

See the README for rate-limited page collection and USDA imports. Keep raw data privately with checksums, collection date, source terms, rejection counts and a review log. Do not claim "real-time nutrition" from an old dataset. The app performs live API persistence; catalog refresh is an operator task.
