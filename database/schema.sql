CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    url TEXT,
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    location TEXT,
    salary_raw TEXT,
    jd_text TEXT NOT NULL,
    jd_parsed TEXT,
    status TEXT DEFAULT 'FOUND',
    match_score INTEGER,
    recommendation TEXT,
    strengths TEXT,
    weaknesses TEXT,
    date_found TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'FOUND',
    match_score INTEGER,
    recommendation TEXT,
    cv_text TEXT,
    cover_letter_text TEXT,
    qa_json TEXT,
    validation_json TEXT,
    notes TEXT,
    url TEXT,
    date_found TEXT,
    date_approved TEXT,
    date_applied TEXT,
    follow_up_date TEXT,
    outcome TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS artifacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER,
    artifact_kind TEXT NOT NULL,
    file_path TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
