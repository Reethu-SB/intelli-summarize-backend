<?php
$host = 'localhost';
$user = 'root';
$pass = '';
$dbname = 'myapp';
$conn = new mysqli($host, $user, $pass, $dbname);
if ($conn->connect_error) {
    http_response_code(500);
    header('Content-Type: application/json');
    echo json_encode(array('error' => 'Database connection failed'));
    exit;
}
?>
