# FitTrack AI — Professional Implementation Master Prompt

## 1. Role and Mission

Act as a principal software architect, senior Java backend engineer, Android engineer, ML engineer, PostgreSQL database architect, DevSecOps engineer, QA engineer, and product designer.

Build **FitTrack AI**, an Android-first, AI-assisted food recognition and nutrition tracking platform designed for real-world use, with a web application planned for a later phase.

This is an implementation assignment, not a concept-design exercise. Inspect the existing repository, create or modify actual source files, install dependencies where appropriate, run builds and tests, diagnose errors, and document the verified state of the application.

The product must be original. Use established nutrition-tracking products as category references, but do not copy proprietary interfaces, assets, branding, datasets, or implementation details.

### Product objective

Help users understand what they eat by allowing them to:

- Photograph a meal and receive food-identification suggestions.
- Review and correct predicted food items.
- Estimate serving sizes and calculate nutrition.
- Maintain a daily food diary.
- Track calories, protein, carbohydrates, fat, and other available nutrients.
- Explore Indian and South Indian foods, including regional meals and mixed dishes.
- Log food using searchable food records and supported Tamil/Tanglish voice input.
- Understand food costs, budget-friendly nutrition, and grocery requirements.
- Review historical consumption and nutrition trends.

**Explicit exclusion:** Do not implement AI workout plans, workout generation, AI fitness coaching, exercise prescriptions, or adaptive workout recommendations. Do not add these features as hidden modules, placeholder screens, or future-scope deliverables.

## 2. Engineering Rules

1. Build functioning software, not just mockups, static screens, or documentation.
2. Inspect the repository before making changes. Preserve working code and existing project conventions where practical.
3. Use stable, mutually compatible dependency versions. Verify current compatibility before selecting versions; do not blindly copy version numbers from examples.
4. Never hardcode production secrets, passwords, signing keys, database credentials, or API tokens.
5. Never invent API responses, food data, model accuracy, test results, or deployment status.
6. Do not mark a feature complete until its implementation and relevant verification evidence exist.
7. Distinguish implemented, tested, partially implemented, blocked, and planned functionality.
8. Prefer a modular monolith for the Java backend. Do not introduce microservices, Kafka, Kubernetes, or Redis without a documented requirement and measured justification.
9. Use typed interfaces, clear domain boundaries, migrations, structured error responses, automated tests, and reproducible build commands.
10. If a dependency, credential, dataset, GPU, external service, or deployment account is unavailable, build the appropriate integration boundary, document the limitation, and continue with independently testable work.
11. Never silently replace an unavailable real service with mock behavior in a production flow.
12. Do not declare the product production-ready merely because it compiles.

## 3. Required Technology Stack

### Android application

- React Native with Expo and TypeScript.
- Expo Router for navigation.
- Expo Camera or Expo Image Picker for meal photographs.
- Secure token storage using an appropriate platform-secure storage library.
- SQLite for offline meal-log drafts and synchronization queues.
- A maintainable state-management and data-fetching strategy.
- Accessible components, loading states, empty states, error handling, and responsive layouts.
- Automated unit/component tests and end-to-end tests where practical.

Use supported Expo SDK packages and verify compatibility before installing them. Avoid exposing access tokens or refresh tokens in logs, screenshots, analytics, or ordinary local storage.

### Backend

- Java 21 LTS.
- A compatible Spring Boot 3.x release with supported dependencies.
- Spring Web, Spring Security, Spring Data JPA, Hibernate, Jakarta Bean Validation, Spring Boot Actuator, and Maven.
- PostgreSQL as the primary relational database.
- Flyway for version-controlled schema migrations.
- JWT-based authentication and authorization implemented with Spring Security.
- OpenAPI documentation.
- JUnit 5, Mockito, Spring Boot Test, and Testcontainers for integration testing.

Keep the backend as a modular monolith with distinct authentication, user, food catalog, recognition, nutrition, meal diary, recipe, budget, reporting, and privacy modules.

### Machine learning

- Python for custom food-model training, evaluation, and inference.
- PyTorch or another justified, reproducible ML framework.
- A documented training pipeline, dataset manifest, experiment configuration, evaluation scripts, model versioning, and inference interface.
- A versioned model-serving interface accessible only through an authenticated or appropriately network-restricted backend integration.

Use Java as the primary application backend. Do not move authentication, meal ownership, nutrition persistence, or authorization into the Python service.

### Web application — later phase

- Next.js App Router.
- TypeScript.
- Tailwind CSS and accessible UI components.
- Recharts or an equivalent charting library where analytics justify charts.
- A shared API contract with the Android application.

The web app is a subsequent release. Design the API to support it from the beginning, but do not delay the Android MVP by attempting to build both platforms simultaneously.

### Delivery infrastructure

- Docker for reproducible local services and production container images.
- Docker Compose for local development.
- CI/CD using the repository's available CI platform.
- Managed PostgreSQL for production.
- Private object storage for meal photographs when persistence is necessary.
- HTTPS, application monitoring, structured logs, error reporting, database backups, and restore procedures.

## 4. Product Scope and Priorities

### Phase 1 — Functional Android MVP

Implement the following end-to-end:

1. Registration, login, logout, and token lifecycle.
2. User profile and basic nutrition preferences.
3. Food catalog search, including Indian foods.
4. Meal photo selection or capture.
5. Custom model inference through the backend.
6. Editable food identification and portion estimates.
7. Nutrition calculation using trusted food records or verified recipes.
8. Saving, editing, and deleting meal entries.
9. Daily food diary and nutrition summary.
10. User corrections and correction-history records.
11. Account data export and deletion workflows.
12. Error handling, automated tests, security checks, and deployment documentation.

### Phase 2 — Nutrition intelligence

Add only after Phase 1 has been verified:

- Tamil/Tanglish speech-to-text food logging.
- Regional food and recipe expansion.
- Weekly and monthly nutrition reports.
- Budget-based meal and grocery planning.
- Cost per serving and cost per gram of protein.
- Ingredient-based recipe nutrition calculations.
- Offline draft logging and reliable synchronization.

Budget features must not generate unsupported health claims. Grocery planning should use user-selected or clearly defined dietary constraints and available ingredient data.

### Phase 3 — Web application

Implement the Next.js application using the same versioned backend APIs. Support account management, meal history, nutrition summaries, reporting, and other capabilities already proven on Android.

Do not create separate nutrition-calculation rules for web and Android.

## 5. Android UX and Design Requirements

Create a distinctive, premium, practical nutrition application. Avoid excessive animation, decorative 3D effects, and layouts that interfere with logging food quickly.

Required screens:

- Welcome and onboarding.
- Registration and login.
- Home dashboard.
- Camera/photo selection.
- Analysis progress and results.
- Food identification and portion editor.
- Food search.
- Meal diary by date and meal type.
- Meal details and edit screen.
- Nutrition dashboard.
- Goals and preferences.
- Recipes and ingredient calculator, when implemented.
- Budget and grocery tools, when implemented.
- Profile, privacy, export, and account deletion.
- Network/offline and synchronization error states.

### Food-analysis interaction

1. User captures or selects a photograph.
2. The application explains that nutritional values are estimates.
3. The image is uploaded securely.
4. The backend validates the request and initiates inference.
5. The model returns candidate food labels and supported confidence information.
6. The application displays identified items, editable portions, and available nutrition sources.
7. The user corrects incorrect labels, removes false detections, or adds missing items.
8. The application recalculates nutrition when the user changes food or portion size.
9. The user explicitly confirms the meal before it is saved.

Never save uncertain predictions as confirmed facts without an intentional user action. Support manual logging when recognition fails.

## 6. Custom Food-Recognition Model

Implement an actual model-training and evaluation pipeline. A pretrained model may be used for experimentation, but the deliverable must distinguish a pretrained baseline from a genuinely trained and evaluated custom model.

### 6.1 Dataset strategy

Build a documented, legally usable dataset covering representative Indian foods. Include, where available:

- Idli, dosa, uttapam, pongal, upma, and common chutneys.
- Rice varieties, sambar, rasam, kootu, poriyal, and curd rice.
- Chapati, roti, parotta, and common gravies.
- Biryani, pulao, and mixed rice dishes.
- Dal, legumes, vegetables, eggs, fish, chicken, and paneer dishes.
- Snacks, fruits, drinks, sweets, and packaged foods.
- Regional and visually similar dishes.

Do not claim broad regional coverage unless it is supported by the actual dataset and evaluation results.

For every dataset source, record its origin, license, permitted usage, labels, image count, annotation method, class distribution, and known limitations.

Use a reproducible train/validation/test split. Prevent duplicate images and near-duplicate images from leaking between splits. When feasible, split by source, user, meal session, or collection group to better approximate real-world generalization.

Record annotation provenance and uncertainty. Do not scrape or use restricted datasets without verifying usage rights.

### 6.2 Model tasks

Separate the tasks instead of assuming a single classifier solves every nutrition problem:

- Food classification.
- Multi-item food detection or segmentation, if justified.
- Portion estimation using explicitly documented assumptions and inputs.
- Mapping recognized labels to canonical food-catalog identifiers.

Select a model architecture after benchmarking suitable candidates against latency, model size, class coverage, inference cost, and evaluation quality. Document the decision.

### 6.3 Portion estimation limitations

A single RGB photograph cannot reliably determine the exact mass, hidden ingredients, cooking oil, recipe composition, or depth of every meal.

Implement one or more practical correction mechanisms:

- User-selected serving size.
- Grams or milliliters, where appropriate.
- Small, medium, and large serving presets linked to documented reference quantities.
- Food-specific household measures.
- A reference object or additional image only if the method has been implemented and validated.

Display the source and assumptions used for the estimate. Do not present a visually inferred serving weight as a measured fact.

### 6.4 Model evaluation

Generate machine-readable and human-readable evaluation reports.

Measure, where applicable:

- Top-1 and top-5 classification accuracy.
- Per-class precision, recall, and F1 score.
- Macro-F1 for imbalanced food classes.
- Confusion matrix.
- Calibration quality and confidence reliability.
- Detection precision/recall or mAP if an object detector is used.
- Inference latency, model size, and resource usage.
- Performance by food category and representative regional subgroup.
- Nutrition error after food identification and portion correction.

Report sample counts and confidence intervals where practical. Separate validation results from final held-out test results.

Do not promise an accuracy percentage before running the evaluation. Do not claim the model is better than another product without a reproducible, fair comparative benchmark.

### 6.5 Model serving

Define a versioned inference contract containing:

- Request identifier.
- Image reference or securely transmitted image.
- Model version.
- Candidate labels and scores.
- Bounding boxes or masks if supported.
- Processing time and error status.
- Optional portion suggestions with their method and limitations.

Validate file size, image format, decoded dimensions, and processing limits. Protect the inference endpoint against unauthorized access and resource exhaustion.

If the model is not trained yet, implement the training pipeline and interface, clearly mark inference as unavailable, and do not substitute fake predictions.

## 7. Indian Food Nutrition and Calculation Engine

Food recognition and nutrition lookup are separate responsibilities.

The model predicts a food identity. The nutrition engine retrieves a verified record or calculates nutrition from documented ingredients and quantities.

### 7.1 Data sources

Use appropriately licensed and documented nutrition data. USDA FoodData Central can support relevant food records, but it is not a substitute for Indian regional coverage. Add curated Indian-food composition records from reliable sources where permitted.

Each canonical food record should support:

- Stable food ID.
- Display name and alternate names.
- English name and Tamil name where verified.
- Regional or cuisine classification.
- Raw, cooked, or prepared state.
- Nutrient values and units.
- Reference serving size.
- Source, source identifier, and provenance.
- Verification status and last-reviewed date.

Represent unknown values as unknown rather than zero. Distinguish an actual zero nutrient value from a missing measurement.

### 7.2 Recipe-based calculation

For recipes with known ingredients, quantities, and preparation assumptions:

1. Normalize ingredient quantities and units.
2. Match ingredients to canonical nutrition records.
3. Calculate nutrient totals for the recipe.
4. Apply a documented yield or cooked-weight adjustment where justified.
5. Divide by the defined serving count or serving mass.
6. Store the recipe version and calculation provenance.

Do not invent ingredients, oil amounts, or serving weights based on an image.

### 7.3 Nutrition formula

For a nutrient value measured per 100 g:

Nutrition for a serving = nutrient per 100 g × serving weight in grams ÷ 100.

For recipes, sum the contributions from the ingredients and divide according to the documented serving definition.

Maintain consistent units and decimal precision. Apply rounding for display only, not prematurely during intermediate calculations.

### 7.4 Nutrition uncertainty

Show appropriate uncertainty indicators for visually estimated values. Do not claim statistical confidence intervals unless they are derived from a validated method.

Allow users to correct the food identity, portion, and relevant recipe assumptions. Store the corrected result and its provenance.

## 8. Java Backend Architecture

Organize code by business domain rather than creating a single large controller or service.

Suggested package structure:

com.fittrack
- common
- config
- security
- auth
- user
- food
- recognition
- nutrition
- recipe
- meal
- budget
- report
- privacy
- audit

Use controller, application-service, domain, and persistence boundaries where they add clarity. Avoid excessive abstraction for its own sake.

### API conventions

- Version all public API paths using `/api/v1`.
- Use DTOs rather than exposing JPA entities directly.
- Validate request bodies using Bean Validation.
- Return consistent error responses, preferably Problem Details compatible with RFC 9457.
- Use pagination and filtering for history and search endpoints.
- Use explicit time-zone handling and a consistent strategy for stored timestamps.
- Make mutating operations safe against unintended duplicate submissions where appropriate.
- Document authorization requirements, validation rules, and failure cases using OpenAPI.

### Initial endpoint contract

Implement and document the following endpoints:

Authentication:
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`

Profile:
- `GET /api/v1/users/me`
- `PATCH /api/v1/users/me`

Food catalog:
- `GET /api/v1/food/search`
- `GET /api/v1/food/{foodId}`

Recognition:
- `POST /api/v1/food/analyze`
- `GET /api/v1/food/analyze/{analysisId}` if analysis is asynchronous
- `POST /api/v1/food/analyze/{analysisId}/corrections` or an equivalent versioned correction endpoint

Meals:
- `POST /api/v1/meals`
- `GET /api/v1/meals/daily`
- `GET /api/v1/meals/{mealId}`
- `PATCH /api/v1/meals/{mealId}`
- `DELETE /api/v1/meals/{mealId}`

Nutrition:
- `GET /api/v1/nutrition/summary`
- `PUT /api/v1/nutrition/goals`
- `GET /api/v1/reports/weekly`

Recipes and budget:
- `POST /api/v1/recipes/calculate`
- Add budget and grocery endpoints only with documented schemas and functioning implementations.

Privacy:
- Add authenticated data-export and account-deletion request endpoints with explicit status handling.

Specify request and response schemas, error codes, pagination rules, validation, and ownership constraints for every implemented endpoint. Do not create endpoints that return hardcoded success messages in place of real functionality.

## 9. PostgreSQL Data Model

Design a normalized relational schema with foreign keys, unique constraints, appropriate indexes, and migration-managed changes.

Core entities:

- `users`
- `user_profiles`
- `refresh_tokens` or an equivalent revocable session store
- `food_items`
- `food_nutrients`
- `food_aliases`
- `nutrition_sources`
- `recipes`
- `recipe_ingredients`
- `meal_logs`
- `meal_items`
- `food_analyses`
- `food_corrections`
- `nutrition_goals`
- `budget_settings`
- `grocery_items`
- `privacy_requests`
- `audit_events` where justified

Store the provenance of food identification and nutrition calculations. Retain the model version and relevant correction history without collecting unnecessary personal data.

A meal item should preserve sufficient information to reproduce its displayed nutrition calculation, including the selected food, serving quantity, calculation method, and source version where applicable.

Define deletion and retention behavior for every table that contains user-associated data. Use appropriate indexes for user/date meal queries and food search.

Use Flyway migrations from the first database change. Do not rely on automatic schema creation in production.

## 10. Authentication and Application Security

Implement authentication with Spring Security and backend-managed JWTs.

### 10.1 Access and refresh tokens

- Use short-lived signed access tokens with validated issuer, audience where configured, expiration, and signing algorithm.
- Use a cryptographically secure secret or asymmetric signing keys stored outside source control.
- Use revocable refresh-token sessions, preferably with rotation and reuse detection.
- Store refresh-token verifiers securely when implementing a database-backed session store.
- Define logout, token expiration, revocation, and password-reset behavior.
- Never log credentials or raw bearer tokens.
- Do not accept arbitrary algorithms or unverified claims.

Use Argon2id or a suitably configured BCrypt password encoder. Enforce password policy and generic authentication error messages to reduce account enumeration.

### 10.2 Authorization

- Enforce ownership checks for meals, analyses, photos, recipes, exports, and profile data.
- Derive the acting user from the authenticated security context, not a client-supplied owner ID.
- Deny access by default.
- Test cross-user access attempts for every resource type.
- Validate request bodies and enforce upload size, type, and rate limits.
- Add rate limits to login, registration, refresh, analysis, and resource-intensive endpoints.

### 10.3 Infrastructure security

- Use HTTPS for deployed APIs.
- Keep CORS allowlists explicit.
- Configure security headers and suitable transport policies at the hosting layer.
- Use parameterized database access and safe query construction.
- Keep secrets in environment configuration or a managed secret store.
- Run dependency and vulnerability scans in CI.
- Apply least-privilege database and object-storage permissions.
- Avoid exposing stack traces, internal paths, database details, or secrets in public errors.

Document any security controls that depend on the reverse proxy, hosting platform, or deployment environment.

## 11. Privacy and Food Photo Handling

Food photographs may contain faces, home interiors, location metadata, or other unintended personal information.

Implement privacy by design:

- Upload only after a user initiates analysis.
- Validate and safely decode images.
- Strip unnecessary EXIF metadata where practical.
- Store images privately, never in public buckets.
- Use short-lived signed URLs if image access links are necessary.
- Keep raw images only for a documented purpose and retention period.
- Prefer deleting temporary images after inference when persistent storage is not required.
- Do not use user images for model training without separate, explicit, informed consent.
- Provide a documented export and deletion process.
- Delete or anonymize associated photos, analyses, corrections, and meal data according to a defined retention policy.
- Explain what data is collected, why it is needed, and how long it is retained.
- Prevent images and sensitive nutrition data from appearing in application logs.

Implement account deletion as a reliable workflow. If deletion is asynchronous, expose request status and document any backup-retention limitations. Do not claim immediate permanent deletion from backups unless that behavior is actually guaranteed.

## 12. Android Offline and Network Behavior

Implement reliable states for slow networks, failed uploads, interrupted inference, expired tokens, and application restarts.

For offline support:

- Persist draft meal entries locally.
- Use a synchronization queue with stable client-generated identifiers or idempotency keys.
- Define conflict resolution for edits made on multiple devices.
- Avoid duplicate meals when a request is retried.
- Never report server persistence before the server confirms it.
- Clearly distinguish locally saved drafts from server-synchronized records.
- Encrypt particularly sensitive local data where appropriate and avoid storing long-lived credentials in SQLite.

## 13. Voice Logging

Implement Tamil/Tanglish voice logging only after the core photo and manual logging flows work.

- Verify the speech-recognition provider supports the required languages and actual Tamil/Tanglish usage.
- Display the transcription for user review before saving.
- Parse the transcript into candidate food names and quantities.
- Resolve candidates against the food catalog.
- Ask the user to clarify ambiguous food names or portions.
- Never convert uncertain speech into an unreviewed, confirmed meal.

Test with representative Tamil and Tanglish phrases, code-switching, regional food names, and noisy environments. Document unsupported cases and external provider costs.

## 14. Testing Strategy

Write tests alongside the implementation, not after all features are supposedly complete.

### Java backend tests

Use JUnit 5, Mockito, Spring Boot Test, and Testcontainers.

Cover:

- Registration, login, refresh, logout, and token expiration.
- Invalid credentials and authorization failures.
- Cross-user data-access attempts.
- Meal creation, updates, and deletion.
- Nutrition calculations, unit conversions, and rounding.
- Recipe ingredient totals and missing nutrition values.
- Image upload validation and recognition-service errors.
- Food correction and recalculation.
- Duplicate request handling.
- Migration execution against PostgreSQL.
- Privacy export and deletion workflows.
- Pagination, filtering, and date/time-zone boundaries.

Use real PostgreSQL through Testcontainers for critical persistence tests. Do not treat H2-only tests as proof of PostgreSQL compatibility.

### Android tests

Cover:

- Authentication and session expiry.
- Camera and image-picker permission handling.
- Image upload failure and retry.
- Food result editing and portion changes.
- Meal save, edit, and delete.
- Nutrition summary refresh.
- Offline drafts and synchronization.
- Empty states, loading states, and API error messages.
- Accessibility and critical navigation paths.

Add end-to-end tests for the most important user journey when the environment supports them.

### ML tests

Cover:

- Dataset-manifest validation.
- Invalid and corrupt images.
- Class-label consistency.
- Reproducible data splitting.
- Inference schema validation.
- Model-version compatibility.
- Per-class evaluation reporting.
- Confidence and fallback behavior.
- Latency measurement.
- Nutrition mapping for recognized labels.

### Quality gates

Run formatting, static analysis, dependency scans, and tests in CI. Do not suppress failures just to obtain a green pipeline.

Report exact test commands, pass/fail counts, skipped tests, and environmental blockers. A test that was not executed must not be reported as passed.

## 15. Deployment and Operations

Provide a reproducible local environment and a documented production deployment plan.

### Local development

- Docker Compose for PostgreSQL and any required local services.
- Backend startup and migration instructions.
- Android setup and device/emulator instructions.
- ML environment and model-training instructions.
- Sample environment configuration with placeholders only.
- Health-check endpoints and structured logs.

### CI/CD

Create pipeline stages for:

1. Dependency installation and caching.
2. Formatting and static checks.
3. Backend compilation and unit tests.
4. PostgreSQL integration tests.
5. Android TypeScript checks and tests.
6. ML pipeline validation and selected evaluation tests.
7. Dependency and security scans.
8. Container build and artifact generation.
9. Deployment only after required checks succeed.

### Production deployment

Document a suitable managed deployment architecture with:

- Managed PostgreSQL, encrypted connections, backups, and tested restoration.
- Secure application secrets.
- Private image storage and lifecycle policies.
- HTTPS and restricted service communication.
- Monitoring, error reporting, and actionable alerts.
- Database migration and rollback strategy.
- Model versioning and rollback.
- API rate limits and capacity limits.
- Staging and production environment separation.

Generate Android release artifacts only when the configured signing and build environment permits it. Never invent a download URL, claim a release was published, or claim a cloud deployment succeeded without actual verification.

## 16. Observability and Reliability

Implement:

- Liveness and readiness checks.
- Structured, correlated request logs.
- Request IDs and safe error reporting.
- Recognition latency and failure metrics.
- Database connection and query-health monitoring.
- API error-rate and latency measurements.
- Model version and inference timing.
- Appropriate alerts for repeated failures.

Exclude tokens, passwords, raw photos, and unnecessary personal data from telemetry.

Document service timeouts, retry rules, request-size limits, concurrency limits, and behavior when the model service is unavailable.

Do not add complex distributed infrastructure without a measured need.

## 17. Measurable Acceptance Criteria

Use these criteria as release gates. Values must be measured, and evidence must be produced before declaring a gate passed.

### A. Build and reproducibility

- The backend compiles using the selected Java 21-compatible configuration.
- Flyway migrations apply to a clean PostgreSQL instance.
- The Android application passes its TypeScript and production-build checks.
- The ML environment installs from documented dependency configuration.
- A fresh developer environment can follow the setup instructions without undocumented manual changes.

### B. Core meal logging

- A test user can register, authenticate, search food, and create a meal.
- The user can view, edit, and delete their own meals.
- Another authenticated user cannot access or modify those meals.
- Nutrition summaries reconcile with stored meal-item calculations within the documented rounding policy.
- Invalid inputs and failed dependencies produce documented errors instead of silent success.

### C. Recognition

- A reproducible held-out evaluation report exists for the actual custom model.
- The report includes sample counts, class coverage, top-1 accuracy, macro-F1, per-class results, and applicable uncertainty information.
- Inference returns the model version and documented prediction schema.
- Invalid images and unavailable model services are handled safely.
- Recognition quality targets are established from a baseline and accepted before release; do not invent a pass result before measurement.

### D. Nutrition

- Calculation tests cover known nutrient values, portion scaling, recipe totals, unit conversion, and missing values.
- Every displayed nutrient has a traceable source or a clearly labeled estimation method.
- Missing values are not silently converted to zero.
- Photo-based results are editable and require user confirmation before saving.

### E. Security and privacy

- Automated tests verify authentication, expiration, refresh, revocation, and resource ownership.
- Tests cover cross-user access and invalid upload requests.
- No production secrets are committed to the repository.
- Privacy export and deletion workflows have documented, testable behavior.
- Dependency and security scan findings are reviewed and documented.

### F. Performance

Define targets for the expected deployment environment and test dataset before release. Measure API latency, photo-upload size, inference latency, and database query behavior.

Record p50 and p95 latency under a documented workload. Set explicit budgets for Android application startup, analysis completion, and API availability based on the target environment. Do not claim those budgets are met until the relevant measurements exist.

### G. Android release readiness

- Critical user journeys pass on a supported Android emulator or physical device.
- Permission denial, network loss, API errors, and expired sessions are handled.
- The release build completes in the configured environment.
- A signed distributable exists only if signing is configured and the artifact has actually been generated.
- No critical user journey relies on fake recognition results or hardcoded production data.

### H. Documentation

- Setup, architecture, API contracts, database schema, model training, model evaluation, security, privacy, testing, deployment, and troubleshooting are documented.
- Every acceptance criterion has a status and supporting evidence.
- Known limitations are visible and specific.

## 18. Required Implementation Workflow

Follow this sequence, adapting only when repository findings justify a change.

### Step 1 — Repository audit

Inspect existing files, Git status, runtime versions, package manifests, configuration, current tests, and deployment setup.

Identify existing implementation, broken features, missing dependencies, and risks. Do not overwrite working code without understanding its purpose.

Deliver an audit summary and prioritized implementation plan.

### Step 2 — Architecture and contracts

Define module boundaries, core data entities, migration strategy, API contracts, authentication design, error formats, ML inference interface, and photo-retention policy.

Create architecture documentation and a concise implementation checklist.

### Step 3 — Backend foundation

Implement Spring Boot configuration, PostgreSQL integration, Flyway, validation, error handling, security configuration, authentication, and the initial automated tests.

Verify each increment before proceeding.

### Step 4 — Food catalog and nutrition engine

Create the catalog schema, seed only documented and appropriately licensed data, implement search, nutrient lookups, unit conversions, recipe calculations, and deterministic calculation tests.

### Step 5 — Custom ML pipeline

Implement dataset manifests, validation, training, evaluation, model packaging, inference, and model-version reporting.

If a dataset or suitable compute environment is unavailable, make the pipeline reproducible and document what is required to train the model. Do not invent training results.

### Step 6 — Android vertical slice

Complete one end-to-end workflow:

Login → select meal photo → submit analysis → review food candidates → correct food and portion → calculate nutrition → confirm → save → view in diary.

Test the full journey before adding secondary features.

### Step 7 — Remaining MVP

Implement meal history, edits, summaries, goals, privacy controls, offline drafts where practical, and robust error handling.

### Step 8 — Hardening

Run backend, Android, ML, security, and integration tests. Resolve critical defects. Measure performance, validate migration and recovery procedures, and record outstanding issues.

### Step 9 — Release preparation

Prepare reproducible release builds, CI/CD, environment configuration, deployment instructions, monitoring, and rollback procedures.

### Step 10 — Web readiness

Verify that the versioned API supports a future Next.js application. Begin web implementation only after the Android MVP and shared backend contracts are stable.

## 19. Repository Deliverables

Use a maintainable monorepo structure similar to:

```text
fittrack-ai/
├── apps/
│   ├── android/
│   └── web/                       # Later phase
├── backend/
│   ├── pom.xml
│   ├── src/main/java/com/fittrack/
│   ├── src/main/resources/
│   │   └── db/migration/
│   └── src/test/
├── ml/
│   ├── configs/
│   ├── datasets/
│   ├── src/
│   ├── tests/
│   ├── scripts/
│   ├── model_registry/
│   └── reports/
├── infra/
│   ├── docker/
│   ├── compose/
│   └── deployment/
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── security/
│   ├── privacy/
│   ├── testing/
│   └── deployment/
├── .github/workflows/
├── .env.example
├── .gitignore
└── README.md
```

Adapt the structure to the repository rather than duplicating an existing project unnecessarily.

Do not commit datasets, trained model binaries, secrets, private photos, generated user data, or large artifacts unless their inclusion is explicitly justified and permitted. Document external artifact storage and reproducibility where needed.

## 20. Final Delivery Report

At the end of each implementation session, provide a factual report with:

1. **Implemented:** Actual files and behavior added or changed.
2. **Verified:** Exact commands executed and their results.
3. **Tests:** Counts, pass/fail status, skipped tests, and test environment.
4. **ML status:** Dataset availability, training status, model version, evaluation results, and limitations.
5. **Security:** Controls implemented and remaining risks.
6. **Deployment:** What was built, deployed, or merely documented.
7. **Acceptance matrix:** Each criterion marked PASS, FAIL, BLOCKED, or NOT TESTED, with evidence.
8. **Known limitations:** Specific unresolved problems and their impact.
9. **Next steps:** The highest-priority tasks needed to reach the next milestone.

Use evidence such as build logs, test results, evaluation reports, migration results, and generated artifacts.

Never label a feature complete simply because its files exist. Never label a test passed if it was not run. Never claim that the app is deployed, production-ready, secure, or more accurate than competitors without the evidence necessary to support that statement.

## Final Instruction

Begin by auditing the current repository and reporting what actually exists. Then implement the highest-priority end-to-end slice, verify it, and continue incrementally.

Optimize for correctness, maintainability, security, nutritional traceability, user control, and measurable quality—not the number of features generated.

**FitTrack AI must be a trustworthy nutrition product, not an AI demo.**