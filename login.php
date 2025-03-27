<?php
$db = new SQLite3('vulnerable.db');

// Vulnerable login
$username = $_POST['username'];
$password = $_POST['password'];

// Vulnerable query
$query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
$result = $db->query($query);

if($row = $result->fetchArray(SQLITE3_ASSOC)) {
    echo json_encode(['success' => true, 'user' => $row]);
} else {
    echo json_encode(['success' => false]);
}
?> 