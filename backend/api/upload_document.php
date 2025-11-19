<?php
header('Content-Type: application/json');
include __DIR__ . '/../db.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
if (!isset($_FILES['file'])) {
    http_response_code(400);
    echo json_encode(array('error' => 'No file uploaded'));
    exit;
}
$uploads_dir = __DIR__ . '/../uploads';
if (!is_dir($uploads_dir)) {
    mkdir($uploads_dir, 0755, true);
}
$file = $_FILES['file'];
$original_name = basename($file['name']);
$target = $uploads_dir . '/' . time() . '_' . $original_name;
if (move_uploaded_file($file['tmp_name'], $target)) {
    $user_id = isset($_POST['user_id']) ? intval($_POST['user_id']) : 0;
    $file_type = isset($file['type']) ? $file['type'] : '';
    $stmt = $conn->prepare('INSERT INTO documents (user_id, file_name, file_path, file_type, uploaded_at) VALUES (?, ?, ?, ?, NOW())');
    $stmt->bind_param('isss', $user_id, $original_name, $target, $file_type);
    if ($stmt->execute()) {
        echo json_encode(array('success' => true, 'document_id' => $stmt->insert_id, 'file_name' => $original_name));
    } else {
        http_response_code(500);
        echo json_encode(array('error' => 'DB insert failed'));
    }
    $stmt->close();
} else {
    http_response_code(500);
    echo json_encode(array('error' => 'Failed to move uploaded file'));
}
$conn->close();
?>
