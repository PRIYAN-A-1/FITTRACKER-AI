# Security and privacy status

Implemented: BCrypt cost 12; JWT HS256 with required >=32-byte secret, issuer and expiry validation; active session-family validation; 15-minute access lifetime; 30-day hashed refresh tokens; transactional refresh rotation and family revocation on reuse; logout revokes every session for the account; account deletion cascades meals and sessions. Passwords are limited to BCrypt's 72-byte UTF-8 input boundary. Android tokens use SecureStore. Public routes are limited to auth and health. SQL parameters are bound and resource queries derive user IDs from validated tokens.

A bounded in-process per-IP limiter provides 20 auth requests/minute and 300 other requests/minute. It is not a distributed or account-based abuse control. Deployments behind a proxy must configure trusted client-IP handling and shared edge limits. Do not blindly trust X-Forwarded-For. In-memory limits reset with process restarts.

The API has no anonymous catalog endpoint. No permissive CORS configuration is added. Deployed traffic must use HTTPS. The release Android client rejects HTTP API URLs. Local Docker publishes only loopback. The private Food-101 service processes photos in memory; photos are not retained or used for training. Access requires a >=32-character service token. JPEG/PNG uploads have byte/pixel limits and inference concurrency is limited.

Drafts are account-scoped in SQLite, not encrypted at the database layer. They survive sign-out and are not included in server export. Users share exports only by explicit UI action. Account deletion removes live server data then local drafts; if device cleanup fails after server deletion, the device file can remain. A recovery workflow and UI draft management remain release blockers. Device loss protections depend on the OS and passcode. Set clear retention and backup policies before production.

Current server export is synchronous and unbounded by account size. Cap or stream it before large-scale release. Backup deletion is not implemented or guaranteed; production retention and restore drills remain operator requirements. There is no email verification, password reset, MFA, account lockout, or security audit certification.

Threat tests executed use H2 for auth and ownership checks. They do not prove PostgreSQL behavior, production security, Android storage safety, or resistance to load. Additional PostgreSQL integration tests are supplied and run by the included CI job, but that job has not executed in the delivery environment.

There is a private image-upload/inference pipeline with a real pretrained baseline. No photos are stored in an object store, and no paid provider credential is required. Custom regional model training/serving remains a separate pathway. Do not deploy a mock service to mask that state. Raw model scores are not calibrated uncertainty or medically valid nutrition confidence intervals.
