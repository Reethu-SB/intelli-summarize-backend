<?php
header('Content-Type: application/json');
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(array('error' => 'Method not allowed'));
    exit;
}
$data = array(
    array('document_id' => 1, 'user_id' => 1, 'file_name' => 'customer_notes.pdf', 'file_path' => '/uploads/1_customer_notes.pdf', 'file_type' => 'application/pdf', 'uploaded_at' => date('c')),
    array('document_id' => 2, 'user_id' => 2, 'file_name' => 'project_brief.docx', 'file_path' => '/uploads/2_project_brief.docx', 'file_type' => 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'uploaded_at' => date('c')),
    array('document_id' => 3, 'user_id' => 1, 'file_name' => 'meeting_transcript.txt', 'file_path' => '/uploads/3_meeting_transcript.txt', 'file_type' => 'text/plain', 'uploaded_at' => date('c')),
);
echo json_encode($data);
?>
