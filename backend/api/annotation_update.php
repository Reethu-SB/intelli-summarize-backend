<?php
header('Content-Type: application/json');
include __DIR__ . '/../db.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
$id = isset($_POST['id']) ? intval($_POST['id']) : 0;
$text = isset($_POST['text']) ? $_POST['text'] : '';
$x = isset($_POST['x']) ? floatval($_POST['x']) : 0.0;
$y = isset($_POST['y']) ? floatval($_POST['y']) : 0.0;
$page = isset($_POST['page']) ? intval($_POST['page']) : 0;
$stmt = $conn->prepare('UPDATE annotations SET text = ?, x = ?, y = ?, page = ? WHERE id = ?');
$stmt->bind_param('sddii', $text, $x, $y, $page, $id);
if ($stmt->execute()) {
    echo json_encode(array('success' => true, 'affected_rows' => $stmt->affected_rows));
} else {
    http_response_code(500);
    echo json_encode(array('error' => 'Update failed'));
}
$stmt->close();
$conn->close();
?>
