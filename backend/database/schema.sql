CREATE TABLE documents (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255),
  source VARCHAR(255),
  content LONGTEXT
);

CREATE TABLE sentences (
  id INT AUTO_INCREMENT PRIMARY KEY,
  document_id INT,
  sentence TEXT,
  FOREIGN KEY (document_id) REFERENCES documents(id)
);
