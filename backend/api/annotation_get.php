<?php
header('Content-Type: application/json');
include __DIR__ . '/../db.php';
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
$document_id = isset($_GET['document_id']) ? intval($_GET['document_id']) : 0;
$stmt = $conn->prepare('SELECT id, user_id, document_id, text, x, y, page, created_at FROM annotations WHERE document_id = ?');
$stmt->bind_param('i', $document_id);
if ($stmt->execute()) {
    $res = $stmt->get_result();
    $rows = array();
    while ($row = $res->fetch_assoc()) {
        $rows[] = $row;
    }
    echo json_encode($rows);
} else {
    http_response_code(500);
    echo json_encode(array('error' => 'Query failed'));
}
$stmt->close();
$conn->close();
?>
