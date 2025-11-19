DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS flashcards;
DROP TABLE IF EXISTS summaries;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS users;

-- -----------------------------------------------------
-- Table `users`
-- -----------------------------------------------------
CREATE TABLE users (
  user_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(200) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id),
  UNIQUE KEY ux_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table `documents`
-- -----------------------------------------------------
CREATE TABLE documents (
  document_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id INT UNSIGNED NOT NULL,
  file_name VARCHAR(255) NOT NULL,
  file_path VARCHAR(1024) NOT NULL,
  file_type VARCHAR(50) NOT NULL,
  uploaded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (document_id),
  KEY idx_documents_user_id (user_id),
  CONSTRAINT fk_documents_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table `summaries`
-- -----------------------------------------------------
CREATE TABLE summaries (
  summary_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  document_id INT UNSIGNED NOT NULL,
  user_id INT UNSIGNED NOT NULL,
  summary_text TEXT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (summary_id),
  KEY idx_summaries_document_id (document_id),
  KEY idx_summaries_user_id (user_id),
  CONSTRAINT fk_summaries_document FOREIGN KEY (document_id) REFERENCES documents(document_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_summaries_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table `flashcards`
-- -----------------------------------------------------
CREATE TABLE flashcards (
  flashcard_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  summary_id INT UNSIGNED NOT NULL,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (flashcard_id),
  KEY idx_flashcards_summary_id (summary_id),
  CONSTRAINT fk_flashcards_summary FOREIGN KEY (summary_id) REFERENCES summaries(summary_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table `feedback`
-- -----------------------------------------------------
CREATE TABLE feedback (
  feedback_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  summary_id INT UNSIGNED NOT NULL,
  user_id INT UNSIGNED NOT NULL,
  rating TINYINT UNSIGNED NOT NULL COMMENT 'Rating scale: 1-5',
  comments TEXT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (feedback_id),
  KEY idx_feedback_summary_id (summary_id),
  KEY idx_feedback_user_id (user_id),
  CONSTRAINT fk_feedback_summary FOREIGN KEY (summary_id) REFERENCES summaries(summary_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_feedback_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Sample data — users
-- -----------------------------------------------------
INSERT INTO users (user_id, name, email, password_hash, created_at) VALUES
(1, 'Alice Johnson', 'alice@example.com', 'pbkdf2_sha256$100000$saltsalt$hashedpassword1', NOW()),
(2, 'Bob Lee',       'bob@example.com',   'pbkdf2_sha256$100000$saltsalt$hashedpassword2', NOW()),
(3, 'Carol Smith',   'carol@example.com', 'pbkdf2_sha256$100000$saltsalt$hashedpassword3', NOW());

-- -----------------------------------------------------
-- Sample data — documents
-- -----------------------------------------------------
INSERT INTO documents (document_id, user_id, file_name, file_path, file_type, uploaded_at) VALUES
(1, 1, 'customer_notes.pdf',   '/var/app/uploads/1_customer_notes.pdf',   'application/pdf', NOW()),
(2, 2, 'project_brief.docx',   '/var/app/uploads/2_project_brief.docx',   'application/vnd.openxmlformats-officedocument.wordprocessingml.document', NOW()),
(3, 1, 'meeting_transcript.txt','/var/app/uploads/3_meeting_transcript.txt','text/plain', NOW());

-- -----------------------------------------------------
-- Sample data — summaries
-- -----------------------------------------------------
INSERT INTO summaries (summary_id, document_id, user_id, summary_text, created_at) VALUES
(1, 1, 1, 'This document summarizes customer feedback and highlights three major pain points that need immediate attention.', NOW()),
(2, 2, 2, 'Project brief: build MVP with core features A, B, and C in Q1; allocate two engineers and one designer.', NOW()),
(3, 3, 1, 'Transcript notes: decisions made include timeline adjustment and follow-up items assigned to the product team.', NOW());

-- -----------------------------------------------------
-- Sample data — flashcards
-- -----------------------------------------------------
INSERT INTO flashcards (flashcard_id, summary_id, question, answer, created_at) VALUES
(1, 1, 'What are the three major customer pain points?', 'The three major pain points are X, Y, and Z (see summary).', NOW()),
(2, 2, 'What is the MVP scope?', 'The MVP includes core features A, B, and C to be delivered in Q1.', NOW()),
(3, 3, 'Who was assigned follow-up items?', 'Follow-up items were assigned to the product team.', NOW());

-- -----------------------------------------------------
-- Sample data — feedback
-- -----------------------------------------------------
INSERT INTO feedback (feedback_id, summary_id, user_id, rating, comments, created_at) VALUES
(1, 1, 2, 4, 'Good summary — concise and actionable.', NOW()),
(2, 2, 1, 5, 'Exactly captures the scope we discussed.', NOW()),
(3, 3, 3, 3, 'Useful but could include more detail on timeline.', NOW());
