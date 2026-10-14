# API contract v0.3

Base `/api/v1`. All routes except register/login/refresh require `Authorization: Bearer <accessToken>`. Health is `/actuator/health`. Errors use Problem Details for application validation/conflict/not-found; Spring Security authentication failures can have an empty body. Every response gets `X-Request-ID` from the request filter.

| Method/path | Request | Response |
|---|---|---|
| POST /auth/register | email, password, displayName | 201 accessToken, refreshToken, expiresIn, userId |
| POST /auth/login | email, password | 200 token pair |
| POST /auth/refresh | refreshToken | 200 rotated pair; reuse revokes family |
| POST /auth/logout | no body | 204, revokes all account sessions |
| GET /users/me | no body | profile, no password |
| GET /users/me/export | no body | profile + meal records with snapshots |
| DELETE /users/me | no body | 204, live-data cascade |
| GET /food/search | q, page=0, size=20 (max 100) | items, total, page, size |
| GET /food/{id} | source-qualified food ID | per-100g nutrients and provenance |
| POST /food/analyze | multipart image (JPEG/PNG, max 8 MiB) | candidate labels or unknown; 503 if service unavailable |
| POST /meals | foodId, grams, mealType, eatenAt, idempotencyKey, confirmed=true | 201 saved meal |
| GET /meals/{id} | UUID | owner-only meal snapshot |
| PATCH /meals/{id} | foodId, grams, mealType, eatenAt, confirmed=true, version | updated meal; stale version yields 409 |
| DELETE /meals/{id} | UUID | 204 |
| GET /meals/daily | date YYYY-MM-DD, zone (default Asia/Kolkata) | items and nutrient summary |

Valid meal types: breakfast, lunch, dinner, snack. Grams: 0.1–5000. `eatenAt` is an ISO timestamp with offset. Use a UUID `idempotencyKey`, and reuse exactly the same payload on retry. A different payload with the same user/key yields 409. Other users' meal IDs yield 404. Daily boundaries are local midnight to next local midnight, converted to timestamps; DST is handled by ZoneId.

A meal response retains a `snapshot` with the complete source `food` and computed `nutrition`. Snapshot nutrient fields are calories (kcal), protein/carbs/fat/fiber (g). Missing values are null. Summary fields include `knownSubtotal`, `complete`, and `total` (null if any entry lacks that nutrient). Empty diary totals are zero because there are no logged entries; this is not a nutrient measurement.

Server field names for database records use snake_case; token and create DTOs use camelCase. The Android types match this version. A formal generated OpenAPI document remains outstanding.

## Supported flow

Register/login → query catalog → select food and measured grams → user confirms → POST meal → GET daily diary. The Android client writes an account-scoped local draft first, removes it only after a server acknowledgement, and retains its UUID during retries. Sync occurs explicitly or on foreground return; continuous connectivity monitoring, background scheduling/backoff and offline catalog search remain outstanding.

## Added endpoints

- PATCH /users/me: displayName, timeZone.
- GET /nutrition/goals and PUT /nutrition/goals: nullable calories/protein/carbs/fat targets.
- GET /nutrition/summary: date and zone.
- GET /reports/weekly: start date and zone; seven daily summaries.
- POST /recipes/calculate: ingredients [{foodId, grams}], servings; source-derived totals and per-serving amounts.

Repeated creation returns its original response without overwriting later edits. A retry after deletion returns 410. API meal responses contain `version`, which the edit request must supply. Readiness is `/actuator/health/readiness`.
