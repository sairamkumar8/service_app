INSERT INTO users (first_name, last_name, email, phone, address_line1, city, state, pincode)
VALUES
('Arun', 'Kumar', 'arun.kumar@example.com', '9999000001', '12 A Street', 'Bengaluru', 'Karnataka', '560001'),
('Sita', 'Sharma', 'sita.sharma@example.com', '9999000002', '45 MG Road', 'Mumbai', 'Maharashtra', '400001'),
('Ravi', 'Patel', 'ravi.patel@example.com', '9999000003', '56 C Road', 'Ahmedabad', 'Gujarat', '380001'),
('Meena', 'Rao', 'meena.rao@example.com', '9999000004', '78 D Colony', 'Hyderabad', 'Telangana', '500001'),
('Vikram', 'Singh', 'vikram.singh@example.com', '9999000005', '10 Lake View', 'Chennai', 'Tamil Nadu', '600001'),
('Aisha', 'Khan', 'aisha.khan@example.com', '9999000006', '23 City Line', 'Pune', 'Maharashtra', '411001'),
('David', 'Fernandes', 'david.fernandes@example.com', '9999000007', '90 Hill Top', 'Goa', 'Goa', '403001'),
('Preeti', 'Nair', 'preeti.nair@example.com', '9999000008', '8 Silver Park', 'Kochi', 'Kerala', '682001'),
('Karan', 'Malhotra', 'karan.malhotra@example.com', '9999000009', '14 Sunrise St', 'Delhi', 'Delhi', '110001'),
('Neha', 'Verma', 'neha.verma@example.com', '9999000010', '22 Rose Villa', 'Jaipur', 'Rajasthan', '302001');



INSERT INTO employment_info (user_id, company_name, designation, start_date, end_date, is_current)
VALUES
(1, 'TSL', 'Data Analyst', '2021-06-01', NULL, TRUE),
(2, 'Innotech', 'Software Engineer', '2020-01-15', '2022-11-30', FALSE),
(3, 'TSL', 'Senior Engineer', '2019-03-10', NULL, TRUE),
(4, 'Infosys', 'HR Manager', '2022-01-01', NULL, TRUE),
(5, 'Wipro', 'Team Lead', '2021-08-15', NULL, TRUE),
(6, 'TCS', 'Associate Consultant', '2020-09-20', '2023-02-28', FALSE),
(7, 'Accenture', 'Developer', '2021-12-01', NULL, TRUE),
(8, 'Cognizant', 'QA Analyst', '2021-03-05', NULL, TRUE),
(9, 'Capgemini', 'Systems Engineer', '2022-07-01', NULL, TRUE),
(10, 'TechMahindra', 'Consultant', '2019-05-20', NULL, TRUE);



INSERT INTO user_bank_info (user_id, bank_name, account_number, ifsc, account_type)
VALUES
(1, 'SBI', '11111', 'SBIN000111', 'Savings'),
(2, 'HDFC', '22222', 'HDFC000222', 'Savings'),
(3, 'SBI', '33333', 'SBIN000333', 'Current'),
(4, 'ICICI', '44444', 'ICIC000444', 'Savings'),
(5, 'Axis Bank', '55555', 'UTIB000555', 'Current'),
(6, 'SBI', '66666', 'SBIN000666', 'Savings'),
(7, 'HDFC', '77777', 'HDFC000777', 'Current'),
(8, 'ICICI', '88888', 'ICIC000888', 'Savings'),
(9, 'Axis Bank', '99999', 'UTIB000999', 'Savings'),
(10, 'SBI', '101010', 'SBIN001010', 'Current');