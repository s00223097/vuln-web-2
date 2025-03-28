<?php
$db = new SQLite('vulnerable.db');

// Create users table
$db->exec('CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    email TEXT
)');

// Add some test data
$db->exec("INSERT INTO users (username, password, email) VALUES 
    ('admin', 'admin123', 'admin@test.com'),
    ('user1', 'pass123', 'user1@test.com')");

echo "Database created successfully!";
?> 