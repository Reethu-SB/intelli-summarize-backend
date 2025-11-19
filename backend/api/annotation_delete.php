<?php
header('Content-Type: application/json');
include __DIR__ . '/../db.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
$id = isset($_POST['id']) ? intval($_POST['id']) : 0;
$stmt = $conn->prepare('DELETE FROM annotations WHERE id = ?');
$stmt->bind_param('i', $id);
if ($stmt->execute()) {
    echo json_encode(array('success' => true, 'affected_rows' => $stmt->affected_rows));
} else {
    http_response_code(500);
    echo json_encode(array('error' => 'Delete failed'));
}
$stmt->close();
$conn->close();
?>
