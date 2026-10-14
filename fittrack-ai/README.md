# FitTrack — Android nutrition journal

Version 0.3.0 · 14 October 2026

A functioning development project with an original warm ivory/forest-green design, real source-attributed nutrition records, Android food logging, a Java API, and actual CPU food-photo recognition. SnapCalorie was used as a functional category reference; its interface, branding and proprietary algorithms were not copied.

## Start on your laptop

Requirements: Docker Desktop with Compose, Node.js 22+, Python 3.11+, and Android Studio/SDK or a compatible Android development environment.

From the extracted `fittrack-ai` directory:

```bash
python scripts/bootstrap.py
docker compose up --build -d
```

The first image build downloads a pinned 60.4 MB pretrained Food-101 model. It verifies the published SHA-256. Allow internet access and wait for all services to start. Nutrition data is already included. No paid API key is required for this model.

Check API readiness at `http://localhost:8080/actuator/health/readiness`.

In another terminal:

```bash
cd apps/android
npm ci
npx expo run:android
```

For an Android emulator the generated client configuration uses `http://10.0.2.2:8080`. For a phone connected over USB, run `adb reverse tcp:8080 tcp:8080`, then use `EXPO_PUBLIC_API_URL=http://127.0.0.1:8080` in `apps/android/.env` and restart Metro. Do not use an emulator-only address on a physical phone. All release clients require an HTTPS API URL.

Create an account. Search and log a food, or open the photo tool, choose a meal picture, tap Analyze, review the suggestions, select the matching catalog record and enter measured grams. Confirm before saving. The diary then reads your server-confirmed entries.

## Working features

- Registration, login, rotating refresh sessions, logout and account deletion.
- 7,859 source-attributed nutrition records; unknown nutrients stay unknown.
- Food search, measured portion confirmation, meal creation, editing and deletion.
- User-owned daily diary with timezone-aware boundaries and nutrient totals.
- Account-scoped offline drafts, retry delay, failure review, retry/discard and local export.
- Camera/gallery selection and authenticated private image processing.
- A real pretrained ONNX Food-101 classifier. Classification suggestions are editable and never auto-saved.
- Personal calorie/macro goals and seven-day reports.
- Ingredient-based recipe calculation API, profile updates and server data export.
- Java 21 executable backend, Flyway migrations, PostgreSQL Compose configuration, native Android project and CI.

## What the photo model does

The image service uses a published Swin model fine-tuned on Food-101 and converted to quantized ONNX. It runs locally on CPU; meal pictures are not sent to an external AI provider. This is a **pretrained baseline**, not a custom FitTrack model. The custom training/manifest/evaluation pipeline remains in `ml/` for future licensed regional training.

The model suggests a food label. It does not measure serving mass, identify every ingredient, quantify hidden oil, detect every item on a mixed plate, or establish complete Indian/South Indian coverage. Low-score/high-entropy inputs return unknown using documented heuristic thresholds. These thresholds are not validated statistical guarantees. Select the correct catalog record and enter your own grams. Nutrition comes from that source record, not from generated model numbers.

Raw images are processed in memory, not retained on the server and not reused for training. The included pizza fixture is a public-domain test image, not a training corpus.

## Reproduce the checks

```bash
python -m pip install -r ml/runtime-requirements.txt
python -m unittest discover -s tests -v
cd backend
mvn verify
cd ../apps/android
npm run typecheck
npm test
npx expo export --platform android
```

After the disposable local services are running:

```bash
python scripts/integration.py
```

That script creates two temporary accounts, checks the entire API/database/photo flow and deletes the test accounts. Use only a disposable local database. Test evidence and the exact limitations of the delivery environment are in `docs/BUILD_STATUS.md`.

## Android release

The native Android project is included. Development prebuild and Hermes bundling were verified; an installed phone/emulator session and APK generation were not executed here.

The release signing guard requires these environment variables:

- `FITTRACK_KEYSTORE_FILE`
- `FITTRACK_KEYSTORE_PASSWORD`
- `FITTRACK_KEY_ALIAS`
- `FITTRACK_KEY_PASSWORD`

Set `EXPO_PUBLIC_API_URL` to your deployed HTTPS endpoint before building a release. Then use Android Studio or Gradle to build the APK/AAB. No production signing key is shipped; no Play Store release or public backend deployment is claimed. Expo regeneration can rewrite native signing configuration, so keep/reapply the release guard after prebuild.

## Source/data/model rights

Read `data/ATTRIBUTION.md`, `ml/MODEL_SOURCE.md`, and `tests/fixtures/ATTRIBUTION.md`. Source data includes USDA CC0 records and Open Food Facts ODbL records. The combined catalog is distributed under ODbL. The model source declares Apache-2.0. Preserve the relevant attribution and license obligations when distributing modifications.

## Remaining release gates

Phone/emulator user-journey tests, native PostgreSQL concurrency/load and recovery tests, encrypted local draft storage, email verification/password reset, robust delete-account local cleanup recovery, regional model training/evaluation, production monitoring/backups, HTTPS hosting, signed Android release and store submission. Tamil voice, depth-based portions, multi-food segmentation, nutrition label OCR, Health Connect, and subscriptions are not implemented.

This package is a verified development project. It does not claim SnapCalorie-level accuracy or a completed production launch.
