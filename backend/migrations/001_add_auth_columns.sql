-- Migration script to add username and hashed_password columns to users table

-- Add username column (unique, nullable for existing SSO users)
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS username VARCHAR(100) UNIQUE;

-- Add hashed_password column (nullable for SSO users)
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS hashed_password VARCHAR(255);

-- Make name column nullable (for local registered users without name)
ALTER TABLE users 
ALTER COLUMN name DROP NOT NULL;

-- Make provider nullable and set default
ALTER TABLE users 
ALTER COLUMN provider DROP NOT NULL;

-- Update existing users to have 'microsoft' as provider if not set
UPDATE users 
SET provider = 'microsoft' 
WHERE provider IS NULL;

-- Create index on username for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Create index on email for faster lookups (if not exists)
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

COMMENT ON COLUMN users.username IS 'Username for local login, NULL for SSO users';
COMMENT ON COLUMN users.hashed_password IS 'Hashed password for local login, NULL for SSO users';
COMMENT ON COLUMN users.provider IS 'Authentication provider: local, microsoft, google, etc.';
