<?php
header('Content-Type: application/json');
include __DIR__ . '/../db.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
$summary_id = isset($_POST['summary_id']) ? intval($_POST['summary_id']) : 0;
$question = 'Sample question?';
$answer = 'Sample answer.';
$stmt = $conn->prepare('INSERT INTO flashcards (summary_id, question, answer, created_at) VALUES (?, ?, ?, NOW())');
$stmt->bind_param('iss', $summary_id, $question, $answer);
if ($stmt->execute()) {
    echo json_encode(array('success' => true, 'flashcard_id' => $stmt->insert_id, 'question' => $question, 'answer' => $answer));
} else {
    http_response_code(500);
    echo json_encode(array('error' => 'DB insert failed'));
}
$stmt->close();
$conn->close();
?>
