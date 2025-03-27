<?php
$db = new SQLite3('vulnerable.db');

$search = $_GET['q'];
// Vulnerable query
$query = "SELECT * FROM users WHERE username LIKE '%$search%'";
$result = $db->query($query);

$users = [];
while($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $users[] = $row;
}

echo json_encode($users);
?> 