<?php
// Vulnerable: No file type validation
// Vulnerable: No size limits
// Vulnerable: Direct file path usage
$target_dir = "uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);

echo "File uploaded successfully to: " . $target_file;
?> 