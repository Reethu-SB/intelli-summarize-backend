<?php
header('Content-Type: application/json');
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
$data = array(
    array('summary_id' => 1, 'document_id' => 1, 'user_id' => 1, 'summary_text' => 'This is a sample summary.', 'created_at' => date('c')),
    array('summary_id' => 2, 'document_id' => 2, 'user_id' => 2, 'summary_text' => 'Another sample summary.', 'created_at' => date('c')),
    array('summary_id' => 3, 'document_id' => 3, 'user_id' => 1, 'summary_text' => 'Third sample summary.', 'created_at' => date('c')),
);
echo json_encode($data);
?>
