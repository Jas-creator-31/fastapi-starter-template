-- 1. Create the Permission
INSERT INTO permissions (permission_id, permission_slang, description)
VALUES (gen_random_uuid(), 'superuser:full_access', 'Full system access')
ON CONFLICT (permission_slang) DO NOTHING;

-- 2. Create the Role
INSERT INTO roles (role_id, name, description)
VALUES (gen_random_uuid(), 'Administrator', 'System Administrator')
ON CONFLICT (name) DO NOTHING;

-- 3. Link Role to Permission
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.role_id, p.permission_id
FROM roles r, permissions p
WHERE r.name = 'Administrator' 
AND p.permission_slang = 'superuser:full_access'
ON CONFLICT DO NOTHING;

-- 4. Create the User
INSERT INTO app_users (user_id, username, email, password_hash)
VALUES (gen_random_uuid(), 'admin', 'admin@example.com', 'your_hashed_password_here')
ON CONFLICT (email) DO NOTHING;

-- 5. Link User to Role
INSERT INTO user_roles (user_id, role_id)
SELECT u.user_id, r.role_id
FROM app_users u, roles r
WHERE u.email = 'admin@example.com' 
AND r.name = 'Administrator'
ON CONFLICT DO NOTHING;
