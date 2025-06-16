-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create user_details table
CREATE TABLE IF NOT EXISTS user_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    first_name TEXT,
    last_name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    phone TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Insert sample user (password is 'password123')
INSERT INTO users (username, email, password) 
VALUES ('test_user', 'test@example.com', '123456');

-- Insert sample user details
INSERT INTO user_details (
    user_id, first_name, last_name, address, city, state, country, phone
) 
VALUES (
    1, 'John', 'Doe', '123 Main St', 'New York', 'NY', 'USA', '123-456-7890'
);

-- View all users
SELECT * FROM users;

-- View all user details
SELECT * FROM user_details;

-- View user with their details (JOIN query)
SELECT 
    u.id,
    u.username,
    u.email,
    ud.first_name,
    ud.last_name,
    ud.address,
    ud.city,
    ud.state,
    ud.country,
    ud.phone
FROM users u
LEFT JOIN user_details ud ON u.id = ud.user_id; 