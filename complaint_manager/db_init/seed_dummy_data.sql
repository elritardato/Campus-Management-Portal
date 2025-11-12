-- Seed data for Complaint Management System
-- Note: The application auto-seeds this data on first launch via main.py
-- This SQL file is for reference only

INSERT INTO users (full_name, email, role) VALUES
('Admin User', 'admin@example.com', 'admin'),
('John Doe', 'john@example.com', 'user'),
('Jane Smith', 'jane@example.com', 'user'),
('Support Team', 'support@example.com', 'admin');

INSERT INTO complaint_categories (name, description) VALUES
('Technical', 'Technical issues and bugs'),
('Billing', 'Billing and payment related issues'),
('Service', 'Service quality and delivery issues'),
('General', 'General inquiries and feedback');

INSERT INTO complaints (user_id, category_id, title, description, status) VALUES
(2, 1, 'Website not loading', 'The website takes too long to load and sometimes times out', 'open'),
(3, 2, 'Incorrect billing amount', 'I was charged twice for my last order', 'open');
