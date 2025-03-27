<?php
$conn = mysqli_connect("localhost", "root", "", "vulnerable_db");

$search = $_GET['q'];
$query = "SELECT * FROM users WHERE username LIKE '%$search%'";
$result = mysqli_query($conn, $query);

$users = [];
while($row = mysqli_fetch_assoc($result)) {
    $users[] = $row;
}

echo json_encode($users);
?> 