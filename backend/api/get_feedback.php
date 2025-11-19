<?php
header('Content-Type: application/json');
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
$data = array(
    array('feedback_id' => 1, 'summary_id' => 1, 'user_id' => 2, 'rating' => 4, 'comments' => 'Good summary', 'created_at' => date('c')),
    array('feedback_id' => 2, 'summary_id' => 2, 'user_id' => 1, 'rating' => 5, 'comments' => 'Exactly right', 'created_at' => date('c')),
);
echo json_encode($data);
?>
