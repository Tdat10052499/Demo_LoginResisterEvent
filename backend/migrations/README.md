# Database Migration Guide

## Áp dụng Migration

### Option 1: Tự động (Recommended)

Backend sẽ tự động tạo tables khi khởi động:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Option 2: Chạy SQL Script thủ công

Nếu cần update database đã có data:

```bash
# Connect to PostgreSQL
psql -U demo_user -d demo_app -h localhost

# Run migration script
\i migrations/001_add_auth_columns.sql

# Verify changes
\d users
```

Hoặc dùng pgAdmin:
1. Mở pgAdmin
2. Connect to demo_app database
3. Tools → Query Tool
4. Paste nội dung file `migrations/001_add_auth_columns.sql`
5. Execute (F5)

## Rollback (nếu cần)

```sql
-- Remove added columns
ALTER TABLE users DROP COLUMN IF EXISTS username;
ALTER TABLE users DROP COLUMN IF EXISTS hashed_password;

-- Revert name column to NOT NULL
ALTER TABLE users ALTER COLUMN name SET NOT NULL;
```

## Verify Migration

```sql
-- Check table structure
\d users

-- Check if columns exist
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'users';

-- Test insert a local user
INSERT INTO users (email, username, hashed_password, provider)
VALUES ('test@example.com', 'testuser', 'hashed_pwd_here', 'local');
```

## Migration History

| Version | Date | Description |
|---------|------|-------------|
| 001 | 2025-10-17 | Add username and hashed_password columns for local authentication |
