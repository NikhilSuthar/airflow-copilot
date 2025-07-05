-- === MIGRATION 1: Migration Tracking Table ===
CREATE TABLE IF NOT EXISTS checkpoint_migrations (
    v INTEGER PRIMARY KEY
);

-- === MIGRATION 2: Checkpoints Table ===
CREATE TABLE IF NOT EXISTS checkpoints (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    checkpoint_id TEXT NOT NULL,
    parent_checkpoint_id TEXT,
    type TEXT,
    checkpoint JSONB NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
);

-- === MIGRATION 3: Checkpoint Blobs ===
CREATE TABLE IF NOT EXISTS checkpoint_blobs (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    channel TEXT NOT NULL,
    version TEXT NOT NULL,
    type TEXT NOT NULL,
    blob BYTEA,
    PRIMARY KEY (thread_id, checkpoint_ns, channel, version)
);

-- === MIGRATION 4: Checkpoint Writes ===
CREATE TABLE IF NOT EXISTS checkpoint_writes (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    checkpoint_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    idx INTEGER NOT NULL,
    channel TEXT NOT NULL,
    type TEXT,
    blob BYTEA NOT NULL,
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx)
);

-- === MIGRATION 5: Make blob nullable ===
ALTER TABLE checkpoint_blobs
    ALTER COLUMN blob DROP NOT NULL;

-- === MIGRATION 6: No-op (for version tracking) ===
SELECT 1;

-- === MIGRATION 7: Indexes for faster thread access ===
CREATE INDEX IF NOT EXISTS checkpoints_thread_id_idx
    ON checkpoints(thread_id);

CREATE INDEX IF NOT EXISTS checkpoint_blobs_thread_id_idx
    ON checkpoint_blobs(thread_id);

CREATE INDEX IF NOT EXISTS checkpoint_writes_thread_id_idx
    ON checkpoint_writes(thread_id);

-- === MIGRATION 8: Add task_path column to checkpoint_writes ===
ALTER TABLE checkpoint_writes
    ADD COLUMN IF NOT EXISTS task_path TEXT NOT NULL DEFAULT '';

-- === MIGRATION 9: User Credential Table ===
CREATE TABLE IF NOT EXISTS user_credentials (
    thread_id TEXT PRIMARY KEY,
    airflow_username TEXT NOT NULL,
    airflow_password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_credentials_thread_id
    ON user_credentials(thread_id);
