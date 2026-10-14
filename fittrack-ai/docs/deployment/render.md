# Render deployment checklist

The logs showing `Connection to localhost:5432 refused` are from a deployment where `DATABASE_URL` was not available to the running container, so Spring used its local-development fallback.

## Render Web Service settings

1. Deploy the current `main` branch after commit `444018a999a8d9844695b2e09b9e6fdf18c97f67`.
2. Use the repository root `Dockerfile`, or set the Dockerfile path to `fittrack-ai/backend/Dockerfile`.
3. Create or select a Render PostgreSQL database in the same region as the web service.
4. Add this environment variable to the **web service**:

   `DATABASE_URL` = the database's **Internal Database URL** / connection string.

   It must look like `postgresql://user:password@host:5432/database` (or `postgres://...`). Never set it to `localhost`.
5. Add `JWT_SECRET` with a randomly generated value of at least 32 bytes.
6. Add `DATABASE_USER` and `DATABASE_PASSWORD` only if they are not already embedded in `DATABASE_URL`.
7. Leave `PORT` managed by Render. The application binds to `${PORT:8080}` on `0.0.0.0`.
8. Redeploy with **Clear build cache & deploy** if the service still shows logs from the pre-fix image.

The application converts Render's `postgresql://`/`postgres://` connection string to JDBC before Hikari/Flyway starts. Flyway remains enabled and will run migrations against the configured Render database.

Render can wire the value automatically in a Blueprint with:

```yaml
envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: fittrack-db
      property: connectionString
```

If you already have a database, use its actual Render database name rather than creating another one. Do not commit a real connection string or secret.
