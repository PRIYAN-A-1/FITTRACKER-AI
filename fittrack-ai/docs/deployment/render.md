# FitTrack AI — Render deployment

For a Render Web Service, configure the service to build from the repository root `Dockerfile` (or set the Dockerfile path to `fittrack-ai/backend/Dockerfile`). The application listens on Render's `PORT` automatically and binds to `0.0.0.0`.

## Required environment variables

Set these in the Render service's Environment page; do not commit their values:

- `DATABASE_URL`: the Render PostgreSQL **internal connection URL**. The application accepts either Render's `postgresql://...`/`postgres://...` URL or a JDBC URL. Do not use `localhost` in production.
- `DATABASE_USER`: optional when the username is included in `DATABASE_URL`.
- `DATABASE_PASSWORD`: optional when the password is included in `DATABASE_URL`; set it if your Render database exposes credentials separately.
- `JWT_SECRET`: a randomly generated secret of at least 32 bytes.
- `CATALOG_PATH`: set to the path of the catalog available inside the image, if different from the default.
- `MODEL_SERVICE_URL` and `MODEL_SERVICE_TOKEN`: required if photo analysis is enabled and the model service is deployed separately.

Example local-only values:

```dotenv
DATABASE_URL=jdbc:postgresql://localhost:5432/fittrack
DATABASE_USER=fittrack
DATABASE_PASSWORD=local-password
```

The startup failure `Connection to localhost:5432 refused` means the deployed service did not receive a production database URL and fell back to the local-development default. After adding `DATABASE_URL`, redeploy so Flyway can connect and run migrations.
