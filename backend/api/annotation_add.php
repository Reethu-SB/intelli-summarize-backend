<?php
header('Content-Type: application/json');
include __DIR__ . '/../db.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
$user_id = isset($_POST['user_id']) ? intval($_POST['user_id']) : 0;
$document_id = isset($_POST['document_id']) ? intval($_POST['document_id']) : 0;
$text = isset($_POST['text']) ? $_POST['text'] : '';
$x = isset($_POST['x']) ? floatval($_POST['x']) : 0.0;
$y = isset($_POST['y']) ? floatval($_POST['y']) : 0.0;
$page = isset($_POST['page']) ? intval($_POST['page']) : 0;
$stmt = $conn->prepare('INSERT INTO annotations (user_id, document_id, text, x, y, page, created_at) VALUES (?, ?, ?, ?, ?, ?, NOW())');
$stmt->bind_param('iisddi', $user_id, $document_id, $text, $x, $y, $page);
if ($stmt->execute()) {
    echo json_encode(array('success' => true, 'id' => $stmt->insert_id));
} else {
    http_response_code(500);
    echo json_encode(array('error' => 'Insert failed'));
}
$stmt->close();
$conn->close();
?>
