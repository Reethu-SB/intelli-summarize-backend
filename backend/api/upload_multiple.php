<?php
header('Content-Type: application/json');
include __DIR__ . '/../db.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
if (!isset($_FILES['files'])) {
    http_response_code(400);
    echo json_encode(array('error' => 'No files uploaded'));
    exit;
}
$uploads_dir = __DIR__ . '/../uploads';
if (!is_dir($uploads_dir)) {
    mkdir($uploads_dir, 0755, true);
}
$files = $_FILES['files'];
$count = is_array($files['name']) ? count($files['name']) : 0;
$results = array();
$user_id = isset($_POST['user_id']) ? intval($_POST['user_id']) : 0;
$stmt = $conn->prepare('INSERT INTO documents (user_id, file_name, file_path, file_type, uploaded_at) VALUES (?, ?, ?, ?, NOW())');
for ($i = 0; $i < $count; $i++) {
    $original_name = basename($files['name'][$i]);
    $tmp = $files['tmp_name'][$i];
    $type = isset($files['type'][$i]) ? $files['type'][$i] : '';
    $target = $uploads_dir . '/' . time() . '_' . $i . '_' . $original_name;
    if (move_uploaded_file($tmp, $target)) {
        $stmt->bind_param('isss', $user_id, $original_name, $target, $type);
        if ($stmt->execute()) {
            $results[] = array('success' => true, 'document_id' => $stmt->insert_id, 'file_name' => $original_name);
        } else {
            $results[] = array('success' => false, 'error' => 'DB insert failed', 'file' => $original_name);
        }
    } else {
        $results[] = array('success' => false, 'error' => 'Failed to move file', 'file' => $original_name);
    }
}
$stmt->close();
$conn->close();
echo json_encode($results);
?>
