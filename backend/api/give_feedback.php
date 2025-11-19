<?php
header('Content-Type: application/json');
include __DIR__ . '/../db.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
$summary_id = isset($_POST['summary_id']) ? intval($_POST['summary_id']) : 0;
$user_id = isset($_POST['user_id']) ? intval($_POST['user_id']) : 0;
$rating = isset($_POST['rating']) ? intval($_POST['rating']) : 0;
$comments = isset($_POST['comments']) ? $_POST['comments'] : '';
 $stmt = $conn->prepare('INSERT INTO feedback (summary_id, user_id, rating, comments, created_at) VALUES (?, ?, ?, ?, NOW())');
 $stmt->bind_param('iiis', $summary_id, $user_id, $rating, $comments);
 if ($stmt->execute()) {
    $feedback_id = $stmt->insert_id;
    $feedbackData = array(
        'feedback_id' => $feedback_id,
        'summary_id' => $summary_id,
        'user_id' => $user_id,
        'rating' => $rating,
        'comments' => $comments,
        'created_at' => date('c')
    );
    $uploads_dir = __DIR__ . '/../uploads';
    if (!is_dir($uploads_dir)) {
        mkdir($uploads_dir, 0755, true);
    }
    $filePath = $uploads_dir . '/feedback_' . $feedback_id . '.json';
    $written = file_put_contents($filePath, json_encode($feedbackData));
    if ($written === false) {
        echo json_encode(array('success' => true, 'feedback_id' => $feedback_id, 'warning' => 'DB insert succeeded but failed to write feedback file'));
    } else {
        echo json_encode(array('success' => true, 'feedback_id' => $feedback_id));
    }
 } else {
    http_response_code(500);
    echo json_encode(array('error' => 'DB insert failed'));
 }
 $stmt->close();
 $conn->close();
?>
