# Verified state — FitTrack 0.3.0

14 October 2026

## Evidence

| Check | Result |
|---|---|
| Java 21 Maven verify | PASS: 12 tests, zero failures/errors/skips; executable 0.3.0 JAR built |
| Android client transport regression tests | PASS: 7 tests |
| Python data/image/evaluation/service tests | PASS: 16 tests |
| Java → PostgreSQL protocol → data → private ONNX service integration | PASS: 19 scenario checks on PGlite |
| Android TypeScript | PASS |
| Native Android prebuild | PASS |
| Android Hermes bundle export | PASS |
| Pretrained model inference | PASS: actual public-domain pizza image identified as pizza; blank image rejected as unknown |

There are 54 passing test/scenario checks across the four suites above. This is not a count of phone UI tests.

Integration used **PGlite**, the WebAssembly PostgreSQL runtime with a PostgreSQL socket adapter. Flyway migrations, JDBC queries, actual data persistence within the test instance and API flows ran through the PostgreSQL protocol. This establishes local functional behavior; native multi-process PostgreSQL locking, concurrent production load, backups and recovery still require separate verification. Docker Compose and the CI job target native PostgreSQL 17, but neither Docker image build nor that CI job executed here.

## Fixed defects

- Transient refresh-server failures no longer erase login sessions.
- Expired access tokens can refresh before logout.
- Concurrent expired requests share a refresh; stale responses cannot restore a signed-out account.
- Cross-account responses are rejected.
- Failed drafts no longer block all later drafts; attempts, delay and permanent review state are persisted.
- Saved messages distinguish local drafts from server-confirmed entries.
- Creation retries remain safe after editing; differing request bodies conflict.
- Nanosecond timestamps are normalized consistently to database precision.
- Stale edits fail with 409 rather than silently replacing newer changes.
- Deleted meals cannot be resurrected by an old creation retry; cached response data is cleared.
- Invalid date/timezone inputs return 400.
- Catalog updates refresh provenance transactionally.
- Release builds no longer silently select the development debug signing certificate.
- Native backend artifact, documentation and launch configuration now match version 0.3.0.

## Implemented beyond the first build

Original app colors/icon, profile update API, goals API and UI, weekly reports API and UI, ingredient recipe calculation API, photo picker/camera flow, private image endpoint, real pinned pretrained Food-101 ONNX baseline, model download/checksum pipeline, and local draft management/export.

## Important scope limits

No custom regional model was trained in this session, no broad accuracy benchmark was run, and no exact mass/depth/hidden-ingredient inference is claimed. The photo smoke test is not a model evaluation dataset. Nutrition uses source catalog values and user-measured grams.

No phone/emulator UI test, APK/AAB build, production hosting, Play Store publication, security certification, production load test or backup restore was executed. Drafts use ordinary local SQLite and retain a release security limitation. Password reset/email verification and account-delete local cleanup recovery remain incomplete. Recipe UI, Tamil voice, depth portions, multi-item segmentation and nutrition-label scanning are not implemented.

## Local flow checked

Register → source catalog search → confirmed portion → save/retry → owned daily diary → edit/conflict → goals/report/recipe → real photo service → export → delete and replay protection.

Evidence files in `docs/evidence` contain the executed test/build output. No real user credentials, private photos or production keys are included.
