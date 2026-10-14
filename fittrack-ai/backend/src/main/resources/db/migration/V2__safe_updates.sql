ALTER TABLE meals ADD COLUMN version BIGINT NOT NULL DEFAULT 1;
CREATE TABLE meal_requests(user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,idempotency_key UUID NOT NULL,request_hash VARCHAR(64) NOT NULL,meal_id UUID NOT NULL,response_json TEXT NOT NULL,PRIMARY KEY(user_id,idempotency_key));
CREATE TABLE nutrition_goals(user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,calories NUMERIC,protein NUMERIC,carbs NUMERIC,fat NUMERIC);
ALTER TABLE users ADD COLUMN time_zone VARCHAR(80) NOT NULL DEFAULT 'Asia/Kolkata';
