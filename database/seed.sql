
USE project_atlas;

INSERT INTO conversations
(client_id, user_message, assistant_response)
VALUES
('C-01', 'Test question', 'Test response');

INSERT INTO escalations
(client_id, question, reason, status)
VALUES
('C-01', 'Test question', 'Low confidence', 'open');
