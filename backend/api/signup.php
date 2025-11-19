<?php
header('Content-Type: application/json');
include __DIR__ . '/../db.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
$name = isset($_POST['name']) ? $_POST['name'] : '';
$email = isset($_POST['email']) ? $_POST['email'] : '';
$password = isset($_POST['password']) ? $_POST['password'] : '';
if (empty($name) || empty($email) || empty($password)) {
    http_response_code(400);
    echo json_encode(array('error' => 'Missing fields'));
    exit;
}
$hash = password_hash($password, PASSWORD_DEFAULT);
$stmt = $conn->prepare('INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, NOW())');
$stmt->bind_param('sss', $name, $email, $hash);
if ($stmt->execute()) {
    echo json_encode(array('success' => true, 'user_id' => $stmt->insert_id));
} else {
    http_response_code(500);
    echo json_encode(array('error' => 'Insert failed'));
}
$stmt->close();
$conn->close();
?>
