FitTrack AI Master Prompt: Detailed Explanation
A section-by-section guide to what the prompt asks for, why each rule exists, and how to use it.
1. What This Prompt Is
The FitTrack AI prompt is a master implementation prompt. It is written to be given to an AI coding agent (such as Claude Code) so that the agent actually builds software instead of only describing it.
In one line: build an Android-first app where a user photographs a meal, the AI suggests what the food is, the user corrects it, and the app calculates nutrition and keeps a daily diary, with a strong focus on Indian and South Indian food.
The prompt has three layers:
• The product: what the app does and for whom.
• The engineering rules: how the agent must behave, including honesty about what is finished.
• The proof requirements: how every claim must be backed by evidence (tests, logs, reports).
The last sentence of the prompt sums up the attitude: FitTrack AI must be a trustworthy nutrition product, not an AI demo.
2. Role and Mission (Section 1)
The multi-role instruction
The agent is told to act as architect, Java backend engineer, Android engineer, ML engineer, database architect, DevSecOps engineer, QA engineer, and product designer all at once. This is because the project crosses many areas, and the agent must make decisions that work across all of them (for example, a database design that also supports security and testing).
Implementation, not concept design
The agent must inspect the existing repository, write real files, install dependencies, run builds and tests, fix errors, and document what is verified. A pretty plan with no working code fails the assignment.
Originality
Existing nutrition apps may be used as category references only. No copying of their interface, assets, branding, datasets, or code.
Product objectives
The user can:
• Photograph a meal and get food suggestions.
• Review and correct the predicted items.
• Estimate serving sizes and compute nutrition.
• Keep a daily food diary and track calories, protein, carbs, fat, and other nutrients.
• Explore Indian and South Indian foods, including mixed dishes.
• Log food by search and by Tamil/Tanglish voice.
• Understand food cost and plan budget-friendly nutrition and groceries.
• See history and trends.
Explicit exclusion
No workout plans, AI fitness coaching, or exercise recommendations, not even as placeholders. This keeps the scope focused on food and nutrition and avoids unsafe or unsupported health advice.
3. Engineering Rules (Section 2)
These twelve rules are the "behavior contract" for the agent. They fall into four groups.
Group
Rules
Meaning
Honesty
Never invent API responses, food data, model accuracy, test results, or deployment status. Do not mark a feature complete without evidence.
The agent must report reality, even when it is unflattering.
Safety
No hardcoded secrets, passwords, signing keys, or tokens.
Credentials live in environment configuration only.
Simplicity
Prefer a modular monolith. No microservices, Kafka, Kubernetes, or Redis without documented, measured need.
Avoid over-engineering for a first release.
Resilience
If something is unavailable (dataset, GPU, external service), build the integration boundary, document the limit, and keep going. Never silently replace a real service with mock behavior in production.
Blocked items must not stop all progress, and must not be hidden.
The agent must also distinguish five states for every feature: implemented, tested, partially implemented, blocked, planned. Compiling is not the same as production-ready.
4. Technology Stack (Section 3)
4.1 Android app
• React Native + Expo + TypeScript: one JavaScript/TypeScript codebase for Android (and easier future expansion).
• Expo Router: file-based navigation.
• Expo Camera / Image Picker: capture or select meal photos.
• Secure token storage: tokens go in platform-secure storage (Keychain/Keystore-backed), not plain storage.
• SQLite: offline meal drafts and a sync queue.
• State management and data fetching: a maintainable approach (for example React Query plus a light store).
• Quality: accessible components, loading, empty, and error states, responsive layouts, and tests.
4.2 Backend
• Java 21 LTS + Spring Boot 3.x + Maven.
• Spring Web, Security, Data JPA/Hibernate, Bean Validation, Actuator.
• PostgreSQL as the main database and Flyway for versioned schema migrations.
• JWT authentication through Spring Security, plus OpenAPI documentation.
• Testing: JUnit 5, Mockito, Spring Boot Test, Testcontainers.
• Structure as a modular monolith: auth, user, food catalog, recognition, nutrition, meal diary, recipe, budget, reporting, privacy.
4.3 Machine learning
• Python + PyTorch (or another justified framework).
• A documented training pipeline: dataset manifest, experiment configs, evaluation scripts, model versioning, and an inference interface.
• The model service is reachable only through the Java backend, authenticated or network-restricted.
• Important boundary: authentication, meal ownership, and nutrition persistence stay in Java. The Python service only does inference.
4.4 Web app (later)
Next.js App Router, TypeScript, Tailwind, and a chart library. It comes after the Android MVP, but the API is designed from day one so web can reuse it.
4.5 Delivery infrastructure
Docker and Docker Compose locally; CI/CD; managed PostgreSQL; private object storage for photos; HTTPS; monitoring; structured logs; backups and tested restore procedures.
5. Scope and Phases (Section 4)
Phase 1: Functional Android MVP
Twelve end-to-end items:
1. Registration, login, logout, token lifecycle.
2. Profile and nutrition preferences.
3. Food catalog search including Indian foods.
4. Photo capture or selection.
5. Model inference through the backend.
6. Editable food identification and portions.
7. Nutrition from trusted records or verified recipes.
8. Save, edit, delete meals.
9. Daily diary and summary.
10. User corrections with history.
11. Data export and account deletion.
12. Error handling, tests, security checks, deployment docs.
Phase 2: Nutrition intelligence
Only after Phase 1 is verified: Tamil/Tanglish voice logging, regional food expansion, weekly and monthly reports, budget and grocery planning, cost per serving and cost per gram of protein, ingredient-based recipe nutrition, and reliable offline sync. Budget features must not make unsupported health claims.
Phase 3: Web application
Built on the same versioned APIs. The prompt specifically forbids separate nutrition rules for web and Android, so there is one source of truth for calculations.
6. Android UX and the Analysis Flow (Section 5)
Design direction
Premium and practical, with no excessive animation or 3D effects that slow down quick food logging.
Required screens
Welcome/onboarding, register/login, home dashboard, camera/photo selection, analysis progress and results, food and portion editor, food search, diary by date and meal type, meal details/edit, nutrition dashboard, goals, recipes (when built), budget and grocery (when built), profile/privacy/export/deletion, and offline/sync error states.
The nine-step analysis interaction
1. The user captures or selects a photo.
2. The app explains that values are estimates.
3. The image is uploaded securely.
4. The backend validates and starts inference.
5. The model returns candidate labels with confidence.
6. The app shows items, editable portions, and nutrition sources.
7. The user corrects wrong labels, removes false detections, adds missing items.
8. Nutrition recalculates when food or portion changes.
9. The user explicitly confirms before anything is saved.
The key principle: an AI guess is never saved as a confirmed fact without a deliberate user action. Manual logging must always be available when recognition fails.
7. Custom Food-Recognition Model (Section 6)
7.1 Dataset strategy
The dataset must be legal and documented, and it should cover Indian food categories such as idli, dosa, uttapam, pongal, upma, chutneys, rice varieties, sambar, rasam, kootu, poriyal, curd rice, chapati, roti, parotta, gravies, biryani, pulao, dal, eggs, fish, chicken, paneer, snacks, fruits, drinks, sweets, and packaged foods.
Key requirements:
• For every source, record origin, license, permitted use, labels, image count, annotation method, class distribution, and limitations.
• Do not claim broad regional coverage that the data and evaluation do not support.
• Use a reproducible train/validation/test split and prevent duplicate or near-duplicate images from leaking across splits. Where possible, split by source, user, or meal session so results are closer to real-world performance.
• Do not scrape restricted datasets.
7.2 Separate model tasks
The prompt refuses to treat "one classifier solves everything." It separates:
• Food classification.
• Multi-item detection or segmentation, if justified.
• Portion estimation, with documented assumptions.
• Mapping labels to canonical food-catalog IDs.
The architecture must be chosen after benchmarking candidates on latency, size, class coverage, cost, and quality, and the decision documented.
7.3 Portion estimation limits
A single photo cannot reliably reveal exact weight, hidden ingredients, cooking oil, or depth. So the app must offer correction tools: user-selected serving, grams or millilitres, small/medium/large presets tied to documented reference quantities, and food-specific household measures (for example one cup, one ladle, one piece). Reference objects or extra images are allowed only if actually implemented and validated. The app must show the source and assumptions and must never present a visual guess as a measured fact.
7.4 Evaluation
Generate both machine-readable and human-readable reports covering:
• Top-1 and top-5 accuracy.
• Per-class precision, recall, F1, and macro-F1.
• Confusion matrix.
• Calibration (do confidence numbers match reality).
• Detection precision/recall or mAP if a detector is used.
• Latency, model size, resource use.
• Performance by food category and regional subgroup.
• Nutrition error after identification and portion correction.
Report sample counts and confidence intervals where practical, keep validation and final test results separate, never promise an accuracy number before measuring, and never claim to beat another product without a fair, reproducible benchmark.
7.5 Model serving contract
A versioned contract containing request ID, image reference, model version, candidate labels and scores, optional boxes/masks, processing time, error status, and optional portion suggestions with method and limitations. File size, format, decoded dimensions, and processing limits must be validated, and the endpoint must be protected against unauthorized access and resource exhaustion.
If the model is not trained yet: build the pipeline and interface, clearly mark inference as unavailable, and do not return fake predictions.
8. Nutrition Engine (Section 7)
Core idea
The model predicts what the food is. The nutrition engine decides how much nutrition it has. They are separate responsibilities.
Data sources
Use licensed, documented data. USDA FoodData Central is useful but does not cover Indian regional food well, so curated Indian composition records are needed where permitted.
Each canonical food record holds: stable ID, display and alternate names, English and verified Tamil names, cuisine/region, raw/cooked/prepared state, nutrient values and units, reference serving, source and provenance, verification status, and last-reviewed date.
Unknown is not zero. A missing measurement must be stored as unknown, distinct from a true zero.
Recipe-based calculation
1. Normalize ingredient quantities and units.
2. Match each ingredient to a canonical record.
3. Sum nutrient totals.
4. Apply a documented yield or cooked-weight adjustment if justified.
5. Divide by the defined serving count or mass.
6. Store the recipe version and calculation provenance.
The agent must not invent ingredients, oil amounts, or serving weights from an image.
The formula
Serving nutrition = nutrient per 100 g × serving weight (g) ÷ 100
Example: if a food has 130 kcal per 100 g and the serving is 150 g, then 130 × 150 ÷ 100 = 195 kcal. Round only for display, never during intermediate steps.
Uncertainty
Show uncertainty indicators for visually estimated values, but do not claim statistical confidence intervals unless a validated method produces them. Store the user's corrections with their provenance.
9. Java Backend Architecture (Section 8)
Package layout
com.fittrack with sub-packages: common, config, security, auth, user, food, recognition, nutrition, recipe, meal, budget, report, privacy, audit. Use controller, service, domain, and persistence layers where they help, without abstraction for its own sake.
API conventions
• All paths under /api/v1.
• DTOs, never raw JPA entities.
• Bean Validation on request bodies.
• Consistent errors, preferably RFC 9457 Problem Details.
• Pagination and filtering for history and search.
• Explicit time-zone handling and a consistent timestamp strategy.
• Idempotent mutating operations where appropriate.
• OpenAPI documentation of authorization, validation, and failures.
Endpoint groups
Area
Endpoints
Auth
register, login, refresh, logout
Profile
GET and PATCH /users/me
Food catalog
search, get by ID
Recognition
analyze, get analysis (if async), submit corrections
Meals
create, daily list, get, patch, delete
Nutrition
summary, goals (PUT), weekly report
Recipes
calculate
Privacy
data export and account deletion requests with status
Every implemented endpoint needs documented schemas, errors, pagination, validation, and ownership rules. Endpoints that return hardcoded success messages instead of real behavior are forbidden.
10. PostgreSQL Data Model (Section 9)
A normalized schema with foreign keys, unique constraints, indexes, and Flyway-managed migrations. Core tables: users, user_profiles, refresh_tokens, food_items, food_nutrients, food_aliases, nutrition_sources, recipes, recipe_ingredients, meal_logs, meal_items, food_analyses, food_corrections, nutrition_goals, budget_settings, grocery_items, privacy_requests, and audit_events where justified.
Important design points:
• Provenance of recognition and nutrition calculation is stored, including model version and correction history.
• A meal item must keep enough data to reproduce its displayed nutrition: selected food, quantity, method, and source version.
• Every user-linked table needs a defined deletion and retention behavior.
• Indexes for user/date meal queries and food search.
• Never rely on automatic schema creation in production.
11. Authentication and Security (Section 10)
Tokens
• Short-lived signed access tokens with validated issuer, expiry, and algorithm.
• Secrets or signing keys kept outside source control.
• Revocable refresh-token sessions, ideally with rotation and reuse detection, with stored verifiers rather than raw tokens.
• Defined logout, expiry, revocation, and password-reset behavior.
• Never log credentials or bearer tokens; never accept arbitrary algorithms.
• Password hashing with Argon2id or well-configured BCrypt, a password policy, and generic login errors to avoid account enumeration.
Authorization
• Ownership checks on meals, analyses, photos, recipes, exports, profile.
• The acting user always comes from the security context, never from a client-supplied owner ID.
• Deny by default.
• Cross-user access tests for every resource type.
• Upload limits (size, type) and rate limits on login, registration, refresh, analysis, and heavy endpoints.
Infrastructure
HTTPS, explicit CORS allowlist, security headers, parameterized queries, secrets in environment or a secret manager, dependency scans in CI, least-privilege DB and storage permissions, and no stack traces or internal details in public errors. Controls that depend on the proxy or host must be documented as such.
12. Privacy and Photo Handling (Section 11)
Photos may contain faces, home interiors, or GPS metadata, so the prompt requires privacy by design:
• Upload only after the user starts analysis.
• Safely decode and validate images; strip unnecessary EXIF data.
• Private storage only, with short-lived signed URLs if links are needed.
• Keep raw images only for a documented purpose and period; prefer deleting temporary images after inference.
• No use of user images for training without separate, explicit, informed consent.
• Documented export and deletion process, with a retention policy.
• Plain-language explanation of what is collected, why, and for how long.
• No images or sensitive nutrition data in logs.
• Account deletion as a reliable workflow; if asynchronous, expose status and document backup-retention limits. Do not claim instant permanent deletion from backups unless guaranteed.
13. Offline and Network Behavior (Section 12)
Handle slow networks, failed uploads, interrupted inference, expired tokens, and app restarts. For offline support:
• Persist drafts locally.
• Use a sync queue with client-generated IDs or idempotency keys so retries never create duplicate meals.
• Define conflict resolution for multi-device edits.
• Never say "saved to server" before the server confirms.
• Clearly distinguish local drafts from synchronized records.
• Avoid storing long-lived credentials in SQLite.
14. Voice Logging (Section 13)
A Phase 2 feature, built only after photo and manual logging work.
• First verify the speech provider truly supports Tamil and Tanglish.
• Show the transcript for review before saving.
• Parse it into food names and quantities, then match to the catalog.
• Ask for clarification on ambiguous names or portions.
• Never turn uncertain speech into a confirmed meal automatically.
• Test with real Tamil/Tanglish phrases, code-switching, regional food names, and noise; document unsupported cases and provider costs.
15. Testing Strategy (Section 14)
Tests are written alongside features, not at the end.
• Backend: auth flows, token expiry, invalid credentials, cross-user access, meal CRUD, nutrition math and rounding, recipe totals with missing values, upload validation, corrections, duplicate requests, migrations on real PostgreSQL (Testcontainers, not H2 only), privacy workflows, pagination and time-zone boundaries.
• Android: auth and session expiry, permission handling, upload failure and retry, editing results and portions, meal save/edit/delete, summary refresh, offline drafts and sync, empty/loading/error states, accessibility, and a full end-to-end journey where possible.
• ML: manifest validation, corrupt images, label consistency, reproducible splits, inference schema, model-version compatibility, per-class reports, confidence and fallback behavior, latency, and label-to-nutrition mapping.
• Quality gates in CI: formatting, static analysis, dependency scans, tests. No suppressing failures to get a green build. Reports must give exact commands, pass/fail/skipped counts, and environment blockers. A test that did not run is never reported as passed.
16. Deployment and Operations (Section 15)
• Local: Docker Compose for PostgreSQL and services, backend startup and migration steps, Android emulator/device steps, ML setup, an .env.example with placeholders only, health endpoints, structured logs.
• CI/CD stages: install and cache, format and static checks, backend build and unit tests, PostgreSQL integration tests, Android type-check and tests, ML validation, security scans, container build, and deployment only if all checks pass.
• Production plan: managed PostgreSQL with encrypted connections and tested restores, secure secrets, private image storage with lifecycle rules, HTTPS and restricted service traffic, monitoring and alerts, migration and rollback strategy, model versioning and rollback, rate and capacity limits, separate staging and production.
• Signed Android releases only when signing is configured. Never invent a download URL or claim a deployment that was not verified.
17. Observability (Section 16)
Liveness and readiness checks, correlated structured logs with request IDs, recognition latency and failure metrics, database health, API error rate and latency, model version and inference timing, and alerts on repeated failures. Tokens, passwords, raw photos, and unnecessary personal data are excluded from telemetry. Timeouts, retries, request-size and concurrency limits, and behavior when the model service is down must be documented. No complex distributed infrastructure without measured need.
18. Acceptance Criteria (Section 17)
These are release gates, and each needs evidence before it can be called passed.
Gate
What must be shown
A. Build and reproducibility
Backend compiles on Java 21, Flyway migrates a clean PostgreSQL, Android passes TypeScript and production build, ML environment installs from documented config, setup docs work for a fresh developer.
B. Core meal logging
A user can register, log in, search food, create, view, edit, delete meals; another user cannot touch them; summaries reconcile with stored calculations; bad input gives documented errors.
C. Recognition
A held-out evaluation report for the real custom model with sample counts, class coverage, top-1, macro-F1, per-class results, uncertainty; inference returns model version and schema; bad images and model outage handled; quality targets set from a baseline before release.
D. Nutrition
Tests for known values, scaling, recipes, unit conversion, missing values; every nutrient traceable; no silent zeros; photo results editable and confirmed before saving.
E. Security and privacy
Automated tests for auth, expiry, refresh, revocation, ownership, cross-user access, invalid uploads; no committed secrets; export and deletion testable; scan findings reviewed.
F. Performance
Targets defined first, then p50 and p95 latency, upload size, inference latency, and query behavior measured under a documented workload.
G. Android release readiness
Critical journeys pass on an emulator or device; permission denial, network loss, API errors, expired sessions handled; release build completes; signed artifact only if truly generated; no fake recognition in critical flows.
H. Documentation
Setup, architecture, API, schema, training, evaluation, security, privacy, testing, deployment, troubleshooting; each criterion has status and evidence; limitations are specific.
19. Required Workflow (Section 18)
Ten ordered steps:
1. Repository audit: inspect files, Git status, versions, manifests, tests; report findings and a prioritized plan.
2. Architecture and contracts: modules, entities, migrations, APIs, auth design, error format, ML interface, photo retention.
3. Backend foundation: Spring config, PostgreSQL, Flyway, validation, errors, security, auth, first tests, verifying each increment.
4. Food catalog and nutrition engine: schema, licensed seed data, search, unit conversions, recipe calculation, deterministic tests.
5. Custom ML pipeline: manifests, validation, training, evaluation, packaging, inference, version reporting; if data or compute is missing, make it reproducible and document needs.
6. Android vertical slice: login, select photo, analyze, review candidates, correct food and portion, calculate, confirm, save, view in diary; test fully first.
7. Remaining MVP: history, edits, summaries, goals, privacy, offline drafts, robust errors.
8. Hardening: run all tests, fix critical bugs, measure performance, validate migration and recovery.
9. Release preparation: release builds, CI/CD, configuration, deployment and rollback docs, monitoring.
10. Web readiness: confirm the API suits a future Next.js app; start web only when Android and contracts are stable.
The core idea is a vertical slice first: one complete, working path from login to diary before adding side features.
20. Repository Layout and Final Report (Sections 19 and 20)
Monorepo structure
apps/android, apps/web (later), backend (Maven project with Flyway migrations), ml (configs, datasets, src, tests, scripts, model registry, reports), infra (docker, compose, deployment), docs (architecture, api, security, privacy, testing, deployment), .github/workflows, .env.example, .gitignore, and README.md. The agent should adapt to the existing repository rather than duplicating it. Datasets, model binaries, secrets, private photos, and large artifacts are not committed unless justified and permitted.
Final delivery report
After each session the agent must report nine things: Implemented, Verified, Tests, ML status, Security, Deployment, Acceptance matrix (PASS/FAIL/BLOCKED/NOT TESTED), Known limitations, Next steps. Files existing does not mean a feature is complete, and an unrun test is never "passed".
21. The Big Ideas Behind the Prompt
1. Honesty over appearance: no fake data, fake predictions, or fake test results.
2. User control: the user confirms every AI result, and can always log manually.
3. Traceability: every nutrient value can be traced to a source or labeled estimate.
4. Separation of concerns: recognition decides what, the nutrition engine decides how much, and Java owns security and data.
5. Privacy by design: photos are sensitive, so minimize, protect, and delete.
6. Evidence-based claims: measure first, claim later.
7. Incremental delivery: a working vertical slice before extra features.
22. How to Use This Prompt Effectively
• Start with Step 1 only: ask the agent to audit the repository and report before building anything.
• Work phase by phase: do not ask for the whole product in one go; the prompt itself says correctness beats feature count.
• Check the evidence: ask for the exact commands run and their output, and run them yourself.
• Expect blockers: a trained model needs a legal dataset and compute. A good result here is a working pipeline with inference clearly marked unavailable, not made-up accuracy.
• Keep the final report format at the end of every session so progress stays measurable.
23. Quick Glossary
Term
Meaning
Modular monolith
One deployable application organized into clear internal modules.
Flyway
Tool that applies versioned database migrations.
JWT
A signed token proving who the user is.
Refresh token rotation
Issuing a new refresh token each time and invalidating the old one.
Testcontainers
Library that runs a real PostgreSQL in Docker during tests.
Top-1 / Top-5 accuracy
How often the correct food is the first guess, or among the top five guesses.
Macro-F1
Average F1 score across classes, treating each class equally.
Calibration
Whether a model's confidence matches how often it is actually right.
Idempotency key
An ID that makes a repeated request produce only one result.
Problem Details (RFC 9457)
A standard JSON format for API errors.
Provenance
The recorded origin and history of a data value.
EXIF
Metadata inside photos, such as location and device.
24. AI Deep Dive: How the AI Part Works
This section explains the AI side of FitTrack AI in more depth. The prompt uses AI in two places: food recognition from photos (the core) and speech-to-text for Tamil/Tanglish voice logging (Phase 2). Everything else, including nutrition math, is deliberately not AI.
24.1 The big picture: what the AI does and does not do
Job
Done by AI?
Why
Guess what food is in the photo
Yes (image model)
Pattern recognition from pixels is what neural networks are good at.
Find where each food is on the plate
Maybe (detection or segmentation)
Only if a plate has several items and it is justified.
Estimate how much food there is
Partly, with user correction
One photo cannot reveal true weight, so the user confirms.
Look up calories and nutrients
No
Uses verified food records and a fixed formula, so results are traceable.
Save the meal
No
Only after the user explicitly confirms.
Convert Tamil/Tanglish speech to text
Yes (speech model or provider)
Needs a language-capable speech recognizer.
The design rule: AI suggests, the user decides, and the database and formulas calculate. This is what makes the product trustworthy rather than an AI demo.
24.2 The end-to-end recognition pipeline
1. Capture: the user takes or picks a photo in the Android app.
2. Upload: the app sends it over HTTPS to the Java backend, which checks the user's token.
3. Validation: the backend checks file size, image format, decoded dimensions, and safely strips EXIF metadata such as GPS.
4. Inference request: the backend calls the Python model service using the versioned inference contract (request ID, image, model version).
5. Preprocessing: the model service resizes the image, normalizes pixel values, and converts it to a tensor.
6. Prediction: the neural network outputs a score for every known food class.
7. Post-processing: scores become probabilities, and the top candidates are kept (for example top 5).
8. Label mapping: each predicted label such as "masala_dosa" is mapped to a canonical food ID in the catalog.
9. Response: the backend returns candidates, confidence, model version, and processing time to the app.
10. User review: the user fixes labels and portions, then confirms. Nutrition is computed by the nutrition engine, never by the model.
The Python service never talks to the user directly and never owns user data. It only turns an image into predictions.
24.3 Classification vs detection vs segmentation
The prompt asks the agent to treat these as separate tasks rather than assuming one model does everything.
• Classification: one label for the whole image, for example "idli". Simple and fast, but weak when a thali has many items.
• Detection: draws a box around each item and labels it, for example boxes for rice, sambar, and poriyal. Useful for multi-item plates. Measured with precision, recall, and mAP (mean average precision).
• Segmentation: outlines each item pixel by pixel. Most detailed and helpful for portion estimation, but needs expensive annotation (masks).
A sensible path is to start with classification, measure the results, and add detection or segmentation only if the evaluation shows it is needed. The prompt requires the choice to be benchmarked and documented, not assumed.
24.4 How the image model learns (in plain language)
A modern image model is usually a convolutional neural network (CNN) or a vision transformer (ViT).
• Early layers learn simple things such as edges and colors.
• Middle layers learn textures and shapes, such as the grain of rice or the spongy surface of an idli.
• Final layers combine these into food-level concepts.
Training works by showing the model many labeled photos. For each one it predicts, a loss function (commonly cross-entropy) measures how wrong the guess was, and an optimizer (such as AdamW) adjusts millions of weights slightly to reduce that error. This repeats over many epochs (full passes through the data).
24.5 Pretrained baseline vs genuinely custom model
The prompt makes an important distinction:
• Pretrained baseline: a model already trained on a large general dataset (such as ImageNet). Good for quick experiments, but it has little knowledge of regional Indian dishes.
• Custom model: a model that you fine-tuned on your own documented Indian-food dataset and then evaluated on held-out data.
The usual technique is transfer learning: start from a pretrained network and fine-tune it on your food images. This needs far less data and compute than training from scratch. The prompt allows pretrained models for experiments, but the final deliverable must clearly state which one is the baseline and which one is the evaluated custom model. Calling a pretrained model "custom" without training and evaluation would break the honesty rules.
24.6 Training pipeline components
The prompt asks for a reproducible pipeline with these parts:
• Dataset manifest: a file listing every image, its label, source, license, and annotation method.
• Validation scripts: detect corrupt images, duplicate files, and inconsistent labels.
• Splits: train, validation, and test sets created reproducibly (fixed random seed), grouped by source or meal session so near-identical photos do not appear in both train and test. This avoids data leakage, which makes accuracy look better than it really is.
• Augmentation: random crops, flips, brightness and color changes, and blur, so the model copes with real phone photos. Care is needed because color matters for some foods.
• Class imbalance handling: common foods (rice) have many more images than rare dishes. Techniques include weighted loss, balanced sampling, and reporting macro-F1.
• Experiment configs: hyperparameters (learning rate, batch size, epochs, architecture) stored in config files so any run can be repeated.
• Model registry: each trained model gets a version, with its metrics, dataset version, and config recorded, enabling rollback.
24.7 Evaluation metrics explained with examples
• Top-1 accuracy: the correct food is the model's first guess. If 80 of 100 test photos are right on the first guess, top-1 is 80%.
• Top-5 accuracy: the correct food is among the five best guesses. Always at least as high as top-1, and relevant because the app shows a list the user can choose from.
• Precision: of everything the model called "dosa", how many really were dosa.
• Recall: of all real dosa photos, how many the model found.
• F1 score: a single number combining precision and recall.
• Macro-F1: the average F1 across all classes, giving rare foods equal weight. Overall accuracy can hide poor performance on rare dishes, so this metric matters.
• Confusion matrix: a grid showing which foods get mixed up, for example pulao vs biryani, or idli vs a plain rice cake.
• Calibration: whether "90% confident" really means right about 90% of the time. A model can be accurate but overconfident. Reported with reliability diagrams or expected calibration error.
• Subgroup results: performance by category (breakfast, rice dishes, gravies, sweets) and region, to show where the model is weak.
• Nutrition error: after food identification and portion correction, how far the final calories are from the true value. This is the metric users actually feel.
The prompt insists on reporting sample counts and uncertainty (such as confidence intervals), and on keeping validation results separate from the final test results so you do not tune the model on the test set.
24.8 Confidence, uncertainty, and fallback behavior
AI predictions can be wrong, so the app must handle uncertainty honestly:
• Show the top candidates, not only one answer.
• If the top confidence is low, say so, and offer search or manual entry.
• Treat "none of these" as a normal outcome, not an error.
• Never auto-confirm a prediction. Saving always needs a deliberate user tap.
• Do not show a made-up statistical confidence interval for nutrition. Use clearly labeled estimate indicators instead.
For out-of-scope images (a non-food photo, or a dish the model has never seen), a good system returns low confidence or an "unknown" result rather than a confident wrong label. This should be tested.
24.9 Mapping labels to the nutrition catalog
A model outputs class names. The nutrition engine needs stable IDs. A mapping layer connects the two, so "masala_dosa" points to one canonical record with a defined reference serving. It must handle:
• Alternate names (Tamil, English, regional spellings).
• Visually similar dishes mapped to separate records with notes.
• Labels that map to several catalog items (the user then chooses).
• Missing mappings, which are reported instead of guessed.
The prompt includes tests for this mapping, because a wrong mapping gives wrong nutrition even if the model was right.
24.10 Portion estimation: why it is hard
From one 2D photo, the AI cannot know the depth of a bowl, hidden oil or ghee, or the exact weight. So the prompt avoids pretending. Practical options:
• User picks a serving size (small, medium, large) tied to documented reference weights.
• Food-specific household measures, such as 1 idli, 1 cup of rice, 1 ladle of sambar.
• Direct entry in grams or millilitres.
• A reference object or extra photo, but only if it is truly implemented and validated.
The app must always show the assumption used and must label visually inferred portions as estimates.
24.11 Model serving and safety
The model runs as a separate Python service behind the Java backend.
• Versioned contract: every response includes the model version, so results can be traced and rolled back.
• Access control: only the backend may call it, using authentication or network restriction.
• Resource protection: limits on file size, image dimensions, concurrency, and timeouts to stop abuse and overload.
• Latency tracking: inference time is measured and reported (p50 and p95).
• Failure handling: if the model service is down or the model is untrained, the API returns a clear "unavailable" error and the app falls back to manual logging. It must never return fake predictions.
24.12 Privacy in the AI pipeline
• Photos are uploaded only after the user starts analysis.
• Temporary images should be deleted after inference when long-term storage is not needed.
• User photos are never used to improve the model without separate, informed consent.
• Logs must not contain images or sensitive nutrition data.
24.13 AI in voice logging (Phase 2)
Voice logging has its own AI chain:
1. Speech-to-text: a provider or model converts audio to a transcript. You must verify it truly handles Tamil and Tanglish (Tamil written or spoken with English words), plus code-switching such as "two idli and one vadai saptaen".
2. Transcript review: the user sees and can edit the text.
3. Parsing: extract food names and quantities (for example "2 idli", "oru cup sambar").
4. Catalog matching: resolve names to canonical foods, including regional spellings.
5. Clarification: ask the user when a name or portion is ambiguous.
6. Confirmation: nothing is saved without the user's approval.
Testing must include noisy environments and unsupported cases, and external provider costs must be documented.
24.14 A worked example
A user photographs breakfast with two idlis, sambar, and coconut chutney.
1. The model returns candidates such as idli (0.86), medu vadai (0.07), plain rice cake (0.03), with sambar and chutney as further items if detection is used.
2. The app shows the list. The user keeps idli, corrects a wrong item, and sets the portion to 2 pieces.
3. The nutrition engine takes the idli record (per 100 g values) and the reference weight for one piece, then applies: nutrient per 100 g x serving grams / 100.
4. The app shows calories and macros with the source and an "estimate" note.
5. The user taps confirm, and only then is the meal saved with its model version and correction history.
24.15 Honest limits of the AI
• Accuracy depends on the dataset. Regional dishes missing from the data will be misidentified.
• Visually similar foods (different biryanis, similar chutneys) will be confused.
• Hidden ingredients, oil, and sugar cannot be seen.
• Lighting, camera angle, and plating change results.
• No accuracy percentage should be quoted until it is measured on a held-out test set.
• The model is not a substitute for medical or dietary advice.
24.16 Practical learning path for the AI work
For someone building this step by step:
1. Learn Python and PyTorch basics (tensors, datasets, training loop).
2. Fine-tune a small pretrained image model (for example a lightweight CNN) on a small food dataset to understand the workflow.
3. Learn evaluation: confusion matrix, F1, calibration.
4. Build the dataset manifest and leakage-safe splits.
5. Wrap the model in a simple inference API with a versioned schema.
6. Connect it to the backend, then to the Android app, and test the failure cases.
7. Only then consider detection, segmentation, or voice.
25. Project Deep Dive: Backend, Data, App, and Delivery in Detail
This section goes deeper into the non-AI parts of the project. All field names and values below are illustrative examples to help you understand the design. The real implementation may differ, and nothing here is measured data.
25.1 API contract in more detail
Every public endpoint lives under /api/v1. Below, each main endpoint is described with what it receives, what it returns, and how it can fail.
Endpoint
Purpose
Request (main fields)
Success response
Typical errors
POST /auth/register
Create an account
email, password, display name
201 with user ID (no password ever returned)
400 invalid input, 409 email already used, 429 rate limited
POST /auth/login
Sign in
email, password
200 with access token, refresh token, expiry
401 generic invalid credentials, 429 rate limited
POST /auth/refresh
Get a new access token
refresh token
200 with new access and rotated refresh token
401 expired, revoked, or reused token
POST /auth/logout
End a session
refresh token
204 no content
401 if not authenticated
GET /users/me
Read own profile
none (user taken from token)
profile and preferences
401
PATCH /users/me
Update profile
only fields being changed
updated profile
400 validation, 401
GET /food/search
Search the catalog
query text, page, size, optional filters
paged list of foods with reference serving
400 bad paging values
GET /food/{foodId}
Food detail
food ID in path
full nutrient list, sources, verification status
404 not found
POST /food/analyze
Analyze a meal photo
image file (multipart), optional meal type
analysis ID, candidate foods with confidence, model version
400 or 415 invalid image, 413 too large, 503 model unavailable, 429
POST /food/analyze/{id}/corrections
Record user corrections
corrected food IDs, portions, removed items
stored correction and recalculated nutrition
403 or 404 for another user's analysis
POST /meals
Save a confirmed meal
meal type, time, items, idempotency key
201 with meal and computed nutrition
400, 409 duplicate key handled safely
GET /meals/daily
Diary for one day
date, time zone
meals grouped by meal type with totals
400 bad date
PATCH /meals/{id}
Edit a meal
changed fields
updated meal
403 or 404 for another user's meal
DELETE /meals/{id}
Remove a meal
none
204
404
GET /nutrition/summary
Totals vs goals
date range
calories and macros, goal progress
400
PUT /nutrition/goals
Set goals
calorie and macro targets
stored goals
400
GET /reports/weekly
Weekly report
week start
daily totals, averages
400
POST /recipes/calculate
Recipe nutrition
ingredients with quantities and units, serving count
per-serving nutrients with provenance
422 unknown ingredient or unit
Error format. Errors follow RFC 9457 Problem Details: a type, a title, an HTTP status, a human-readable detail, and a request ID. Stack traces, database messages, and internal paths never appear in responses.
Pagination. List endpoints take a page number and size with a documented maximum size, and return total count and page info.
Time handling. Timestamps are stored in UTC. The app sends the user's time zone so that a late-night meal belongs to the correct local day in the diary. This is a classic bug area, so it needs explicit tests around midnight.
Duplicate protection. Meal creation carries a client-generated idempotency key. If the phone retries after a timeout, the server recognizes the key and returns the original result instead of creating a second meal.
25.2 Database schema in more detail
The table below lists key columns for the most important tables. Types and exact names are decided during implementation.
Table
Key columns
Notes
users
id, email (unique), password hash, status, created at
Never stores plain passwords.
user_profiles
user id (FK), display name, time zone, dietary preferences
One row per user.
refresh_tokens
id, user id (FK), token verifier hash, expires at, revoked at, replaced by
Supports rotation and reuse detection.
food_items
id, display name, cuisine or region, state (raw, cooked, prepared), reference serving grams, verification status, last reviewed
Canonical food records.
food_nutrients
food id (FK), nutrient code, amount per 100 g, unit, is measured
Missing means no row or an unknown flag, not zero.
food_aliases
food id (FK), alias, language
English, Tamil, and regional names, used by search and voice matching.
nutrition_sources
id, name, license, version, URL
Every nutrient row links back to a source.
recipes
id, owner id, name, version, serving count, yield factor
Versioned so old meals stay reproducible.
recipe_ingredients
recipe id (FK), food id (FK), quantity, unit
Quantities are normalized to grams for calculation.
meal_logs
id, user id (FK), meal type, eaten at, idempotency key (unique per user)
Index on user id and eaten at for diary queries.
meal_items
id, meal id (FK), food id (FK), quantity, unit, grams, calculation method, source version, user confirmed
Stores enough to reproduce the displayed nutrition.
food_analyses
id, user id (FK), model version, status, created at, image retention state
Links a photo analysis to its outcome.
food_corrections
id, analysis id (FK), predicted food, corrected food, portion change
Correction history.
nutrition_goals
user id (FK), calories, protein, carbs, fat targets
One current goal set per user.
privacy_requests
id, user id, type (export or delete), status, requested at, completed at
Tracks asynchronous workflows.
audit_events
id, user id, event type, time
Only where justified, without sensitive content.
Deletion behavior. For each user-linked table the design must say what happens on account deletion: delete the rows, or anonymize them. Photos and analyses are removed first, then meals and corrections, then the account. Backups may keep data for a documented period, and this limit must be stated honestly to users.
Indexes. The most important are meals by user and date, food search (names and aliases), and unique constraints for email and idempotency keys.
25.3 Authentication flow step by step
1. Register: the server validates the password policy, hashes the password with Argon2id or BCrypt, and stores the user.
2. Login: the server checks the hash. Wrong email and wrong password give the same generic message, so attackers cannot discover which emails exist.
3. Tokens issued: a short-lived access token (for example 10 to 15 minutes, a value chosen during implementation) and a longer-lived refresh token. Only a hash of the refresh token is stored in the database.
4. Using the API: the app sends the access token in the Authorization header. The server verifies signature, algorithm, issuer, and expiry.
5. Refresh with rotation: when the access token expires, the app sends the refresh token. The server issues a new pair and marks the old refresh token as used.
6. Reuse detection: if an already-used refresh token appears again, it may have been stolen. The server revokes the whole session family, forcing a new login.
7. Logout: the refresh token is revoked server-side, and the app deletes tokens from secure storage.
On the phone, tokens are kept in secure storage (Android Keystore-backed), never in plain storage, SQLite, or logs.
25.4 Android app architecture
Navigation. Expo Router uses file-based routes. A likely structure is an auth group (welcome, login, register), a tabs group (home, diary, add, nutrition, profile), and detail screens (analysis results, meal detail, settings).
Layers.
• UI components: reusable, accessible pieces (buttons, cards, nutrient rings).
• Screens: compose components and handle loading, empty, and error states.
• Data layer: an API client that attaches tokens and refreshes them automatically, plus query caching so screens refresh sensibly.
• Local storage: SQLite for drafts and the sync queue, and secure storage for tokens.
• Shared types: TypeScript types matching the API contract, so mistakes are caught at build time.
Accessibility. Labels for screen readers, sufficient color contrast, large touch targets, and text that scales.
Core states on every screen. Loading, empty, error with retry, offline, and success. The prompt treats these as required, not optional polish.
25.5 Offline drafts and synchronization in detail
1. The user logs a meal while offline. The app stores it as a draft in SQLite with a client-generated ID and idempotency key, marked as not synchronized.
2. A sync queue tries to send drafts when the network returns, with retry and backoff.
3. The server uses the idempotency key, so a retry never creates a duplicate.
4. Only after the server confirms does the app mark the meal as synchronized. Until then the UI clearly shows it as a local draft.
5. Conflicts: if the same meal was edited on two devices, a documented rule decides the result (for example the latest server-confirmed edit wins, with the other version kept or flagged). The rule must be written down and tested.
6. If the session has expired during the offline period, the app asks the user to sign in, and drafts remain safe locally.
25.6 Nutrition calculation: a worked recipe example
Illustrative numbers only, not real food data.
Suppose a recipe has two ingredients with values per 100 g:
Ingredient
Quantity used
Calories per 100 g (example)
Contribution
Ingredient A
200 g
130
130 x 200 / 100 = 260
Ingredient B
50 g
400
400 x 50 / 100 = 200
• Total for the recipe = 260 + 200 = 460 kcal.
• If the recipe yields 4 equal servings, one serving = 460 / 4 = 115 kcal.
• If instead the serving is defined by cooked mass, say the recipe weighs 600 g after cooking and a serving is 150 g, then one serving = 460 x 150 / 600 = 115 kcal. Cooking changes weight (water loss or gain), which is why a documented yield adjustment is required.
Rounding rule. Keep full precision through every step and round only when displaying, so totals over a day still add up within the documented tolerance.
Missing values. If an ingredient has no fiber measurement, the recipe's fiber total is flagged as incomplete rather than silently treated as zero.
25.7 CI/CD pipeline in detail
Each push or pull request runs stages in this order. Later stages only run if earlier ones pass.
1. Install and cache dependencies for Java, Node, and Python.
2. Format and static checks: code style, linting, TypeScript type checks.
3. Backend build and unit tests.
4. Integration tests on real PostgreSQL through Testcontainers, including Flyway migrations.
5. Android checks: type-check, unit and component tests.
6. ML validation: manifest checks, schema tests, selected evaluation tests.
7. Security scans: dependency vulnerabilities and secret scanning.
8. Container build and artifact generation.
9. Deploy to staging, then production, only after all required checks pass and with a documented rollback plan.
Failures are fixed, not suppressed.
25.8 Production architecture in simple terms
• The Android app talks over HTTPS to the Java API.
• The Java API talks to managed PostgreSQL (encrypted connections, backups, tested restores) and to private object storage for photos.
• The Java API calls the Python model service on a private network. The model service is not exposed publicly.
• Monitoring collects logs, error rates, latency, and model metrics, and alerts the team on repeated failures.
• Staging and production are separate, each with its own secrets.
• Database migrations and model versions both have rollback procedures.
25.9 Main risks and how the prompt addresses them
Risk
Why it matters
Mitigation in the prompt
No suitable dataset for Indian foods
Model cannot be trained or will be inaccurate
Document dataset needs, build the pipeline anyway, mark inference unavailable, never fake results.
Wrong portion estimates
Calories can be far off
User-selected servings, household measures, assumptions shown, estimates labeled.
Incomplete or unlicensed nutrition data
Wrong values or legal problems
Licensed sources only, provenance for each value, unknown is not zero.
Over-claiming progress
Loses trust, hides defects
Five status levels, evidence required, final report format.
Security mistakes
Account or data exposure
Ownership checks, token rotation, rate limits, cross-user tests, scans.
Photo privacy
Faces or location in images
EXIF stripping, private storage, short retention, consent for training.
Scope creep
Delays the MVP
Phases, explicit exclusion of workout features, Android first.
Duplicate or lost data offline
Frustrates users
Idempotency keys, sync queue, conflict rules.
25.10 Suggested way to plan the work
The prompt does not give calendar dates, so any timeline is your own planning. One sensible ordering, with durations left for you to decide based on team size:
1. Repository audit and architecture documents.
2. Backend foundation: security, database, migrations.
3. Food catalog and nutrition engine with calculation tests.
4. ML pipeline in parallel, as data and compute allow.
5. Android vertical slice from login to diary.
6. Remaining MVP features, privacy workflows, offline drafts.
7. Hardening: performance measurement, security review, recovery drills.
8. Release preparation and documentation.
9. Phase 2 features, then the web app.
25.11 Sample instructions you can give an AI coding agent
Because the master prompt is large, it works best when you feed it in controlled steps:
• Step one: Perform only Step 1 of the workflow: audit the repository and give me a summary and prioritized plan. Do not change any files yet.
• After the audit: Implement Step 2: write the architecture and API contract documents, then wait for my review.
• During building: Implement the backend authentication slice with tests, run the tests, and show me the exact commands and results.
• Before accepting work: Give me the acceptance matrix with PASS, FAIL, BLOCKED, or NOT TESTED for each criterion, with evidence.
This keeps each session small, verifiable, and aligned with the prompt's rule that correctness matters more than the number of features.
25.12 Self-review checklist for the whole project
• Does every nutrient shown have a source or an estimation label?
• Can a user only see their own data, for every resource type?
• Is every AI result editable, and does saving require confirmation?
• Does the app still work, in manual mode, when the model is unavailable?
• Are there any secrets, photos, datasets, or model files committed by mistake?
• Did every claimed test actually run, with counts reported?
• Are limitations written down plainly in the documen