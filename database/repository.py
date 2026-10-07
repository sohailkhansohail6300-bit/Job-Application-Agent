import json
import sqlite3
from datetime import datetime
from pathlib import Path

from core.paths import path_from_root

DB_PATH = path_from_root('database', 'app.db')
SCHEMA_PATH = path_from_root('database', 'schema.sql')
APPLICATION_STATUSES = [
    'FOUND', 'ANALYZING', 'TAILORED', 'READY_FOR_REVIEW', 'APPROVED',
    'APPLIED', 'INTERVIEW', 'REJECTED', 'OFFER', 'WITHDRAWN'
]


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db_file = Path(DB_PATH)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    schema_sql = Path(SCHEMA_PATH).read_text(encoding='utf-8')
    conn = get_connection()
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()


def _normalize_datetime(value=None):
    return (value or datetime.now().isoformat(timespec='seconds'))


# Jobs

def list_jobs():
    init_db()
    conn = get_connection()
    try:
        rows = conn.execute(
            'SELECT * FROM jobs ORDER BY id DESC'
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def find_job_by_url(url):
    if not url:
        return None
    conn = get_connection()
    try:
        row = conn.execute(
            'SELECT * FROM jobs WHERE url = ? LIMIT 1', (url,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def create_job(source, url, company, title, location, salary_raw, jd_text):
    init_db()
    conn = get_connection()
    try:
        cursor = conn.execute(
            '''
            INSERT INTO jobs (source, url, company, title, location, salary_raw, jd_text, status, date_found, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'FOUND', ?, ?, ?)
            ''',
            (source, url, company, title, location, salary_raw, jd_text, _normalize_datetime(), _normalize_datetime(), _normalize_datetime())
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def update_job(job_id, **kwargs):
    if not job_id:
        return None
    init_db()
    conn = get_connection()
    try:
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f'{key} = ?')
            values.append(value)
        fields.append('updated_at = ?')
        values.extend([_normalize_datetime()])
        values.append(job_id)
        conn.execute(f'UPDATE jobs SET {", ".join(fields)} WHERE id = ?', values)
        conn.commit()
        return job_id
    finally:
        conn.close()


# Applications

def list_applications():
    init_db()
    conn = get_connection()
    try:
        rows = conn.execute(
            'SELECT * FROM applications ORDER BY id DESC'
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def create_application(job_id, company, title, status='FOUND', match_score=None, recommendation=None, url=None, date_found=None):
    init_db()
    conn = get_connection()
    try:
        cursor = conn.execute(
            '''
            INSERT INTO applications (
                job_id, company, title, status, match_score, recommendation, url, date_found, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (job_id, company, title, status, match_score, recommendation, url, date_found or _normalize_datetime(), _normalize_datetime(), _normalize_datetime())
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def update_application(app_id, **kwargs):
    if not app_id:
        return None
    init_db()
    conn = get_connection()
    try:
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f'{key} = ?')
            values.append(value)
        fields.append('updated_at = ?')
        values.extend([_normalize_datetime()])
        values.append(app_id)
        conn.execute(f'UPDATE applications SET {", ".join(fields)} WHERE id = ?', values)
        conn.commit()
        return app_id
    finally:
        conn.close()


def add_artifact(app_id, artifact_kind, file_path):
    init_db()
    conn = get_connection()
    try:
        cursor = conn.execute(
            'INSERT INTO artifacts (application_id, artifact_kind, file_path, created_at) VALUES (?, ?, ?, ?)',
            (app_id, artifact_kind, file_path, _normalize_datetime())
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def dashboard_stats():
    init_db()
    conn = get_connection()
    try:
        counts = {
            'jobs_analyzed': conn.execute('SELECT COUNT(*) FROM jobs').fetchone()[0],
            'strong_matches': conn.execute("SELECT COUNT(*) FROM jobs WHERE recommendation = 'STRONG MATCH'").fetchone()[0],
            'ready_for_review': conn.execute("SELECT COUNT(*) FROM applications WHERE status = 'READY_FOR_REVIEW'").fetchone()[0],
            'approved': conn.execute("SELECT COUNT(*) FROM applications WHERE status = 'APPROVED'").fetchone()[0],
            'applied': conn.execute("SELECT COUNT(*) FROM applications WHERE status = 'APPLIED'").fetchone()[0],
            'interviews': conn.execute("SELECT COUNT(*) FROM applications WHERE status = 'INTERVIEW'").fetchone()[0],
            'rejections': conn.execute("SELECT COUNT(*) FROM applications WHERE status = 'REJECTED'").fetchone()[0],
            'offers': conn.execute("SELECT COUNT(*) FROM applications WHERE status = 'OFFER'").fetchone()[0],
        }
        return counts
    finally:
        conn.close()


# bootstrap
init_db()
