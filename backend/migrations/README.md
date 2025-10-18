# Database Migration Guide

## ⚠️ Khi nào CẦN Migration?

Bạn **CẦN CHẠY MIGRATION** nếu:

✅ Bảng `users` **đã tồn tại** từ trước (schema cũ)  
✅ Bảng `users` **thiếu các columns**: `username`, `hashed_password`  
✅ Đã có **data** trong bảng users (SSO users)  

Bạn **KHÔNG CẦN MIGRATION** nếu:

❌ Bảng `users` **chưa tồn tại** (fresh database)  
❌ Đây là **lần đầu tiên** chạy backend  

---

## Áp dụng Migration

### Option 1: Tự động với Python Script (RECOMMENDED) ✅

Chạy script tự động check và migrate:

```bash
cd backend
python migrate_database.py
```

Script sẽ:
- ✅ Kiểm tra bảng users có tồn tại không
- ✅ Kiểm tra columns `username` và `hashed_password` có chưa
- ✅ Tự động thêm các columns thiếu
- ✅ Update constraints (nullable)
- ✅ Tạo indexes
- ✅ Show kết quả migration

**Output mẫu:**
```
🔍 Checking required columns...
  ❌ Column 'username' not found - MIGRATION NEEDED
  ❌ Column 'hashed_password' not found - MIGRATION NEEDED

🚀 Starting migration...
  📝 Adding 'username' column... ✅ Done
  📝 Adding 'hashed_password' column... ✅ Done
  ✅ Migration completed successfully!
```

---

### Option 2: Backend Auto-create (cho fresh database)

Nếu database **chưa có bảng users**, backend sẽ tự động tạo:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Lưu ý:** Option này chỉ **TẠO BẢNG MỚI**, không update bảng đã tồn tại!

---

### Option 3: Chạy SQL Script thủ công

**Khi nào dùng:** Database production, cần kiểm soát chính xác

**Cách 1: Dùng psql command line**

```bash
# Connect to PostgreSQL
psql -U demo_user -d demo_app -h localhost

# Run migration script
\i migrations/001_add_auth_columns.sql

# Verify changes
\d users
```

**Cách 2: Dùng pgAdmin (GUI)**

1. Mở **pgAdmin**
2. Connect to `demo_app` database
3. Right-click database → **Query Tool**
4. Paste nội dung file `migrations/001_add_auth_columns.sql`
5. Click **Execute (F5)**
6. Check output: "ALTER TABLE" success messages

**Cách 3: Dùng DBeaver / DataGrip**

1. Connect to database
2. Open SQL Editor
3. Paste migration script
4. Execute
5. Refresh table structure

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
