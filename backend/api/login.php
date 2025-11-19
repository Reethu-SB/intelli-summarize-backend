<?php
header('Content-Type: application/json');
include __DIR__ . '/../db.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
$email = isset($_POST['email']) ? $_POST['email'] : '';
$password = isset($_POST['password']) ? $_POST['password'] : '';
if (empty($email) || empty($password)) {
    http_response_code(400);
    echo json_encode(array('error' => 'Missing fields'));
    exit;
}
$stmt = $conn->prepare('SELECT user_id, password_hash FROM users WHERE email = ?');
$stmt->bind_param('s', $email);
$stmt->execute();
$stmt->bind_result($user_id, $password_hash);
if ($stmt->fetch()) {
    if (password_verify($password, $password_hash)) {
        echo json_encode(array('success' => true, 'user_id' => $user_id));
    } else {
        http_response_code(401);
        echo json_encode(array('error' => 'Invalid credentials'));
    }
} else {
    http_response_code(401);
    echo json_encode(array('error' => 'Invalid credentials'));
}
$stmt->close();
$conn->close();
?>
