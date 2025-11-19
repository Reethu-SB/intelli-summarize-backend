<?php
header('Content-Type: application/json');
include __DIR__ . '/../db.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
$document_id = isset($_POST['document_id']) ? intval($_POST['document_id']) : 0;
$user_id = isset($_POST['user_id']) ? intval($_POST['user_id']) : 0;
$summary = 'This is a test summary.';
$stmt = $conn->prepare('INSERT INTO summaries (document_id, user_id, summary_text, created_at) VALUES (?, ?, ?, NOW())');
$stmt->bind_param('iis', $document_id, $user_id, $summary);
if ($stmt->execute()) {
    echo json_encode(array('success' => true, 'summary_id' => $stmt->insert_id, 'summary_text' => $summary));
} else {
    http_response_code(500);
    echo json_encode(array('error' => 'DB insert failed'));
}
$stmt->close();
$conn->close();
?>
