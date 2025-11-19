<?php
header('Content-Type: application/json');
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
$data = array(
    array('flashcard_id' => 1, 'summary_id' => 1, 'question' => 'What are the pain points?', 'answer' => 'X, Y, Z', 'created_at' => date('c')),
    array('flashcard_id' => 2, 'summary_id' => 2, 'question' => 'What is the MVP?', 'answer' => 'Features A, B, C', 'created_at' => date('c')),
);
echo json_encode($data);
?>
