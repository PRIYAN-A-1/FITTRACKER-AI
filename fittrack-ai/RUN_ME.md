# FitTrack Android — Quick start

1. Install Docker Desktop, Android Studio/SDK, Node.js 22+, and Python 3.11+.
2. Extract this ZIP and open a terminal in `fittrack-ai`.
3. Run:

```bash
python scripts/bootstrap.py
docker compose up --build -d
```

The first build downloads the checksum-verified pretrained food model. No paid AI API key is needed.

4. Start an Android emulator in Android Studio. Open another terminal:

```bash
cd apps/android
npm ci
npx expo run:android
```

5. Register → search or photograph food → review the correct catalog record → enter measured grams → confirm → check your diary.

This is source plus a compiled Java 21 API. It is not a preinstalled APK or a publicly hosted production service. Complete setup and verified test evidence are in README.md and docs/BUILD_STATUS.md.
