-- ===========================
-- 1. JOIN USER + EMPLOYMENT + BANK
-- ===========================
SELECT 
    u.*, 
    e.company_name, e.designation, e.start_date, e.end_date, e.is_current,
    b.bank_name, b.account_number, b.ifsc, b.account_type
FROM users u
LEFT JOIN employment_info e ON u.id = e.user_id
LEFT JOIN user_bank_info b ON u.id = b.user_id;

-- ===========================
-- 2. FILTER BY COMPANY (same as API)
-- ===========================
SELECT u.*
FROM users u
JOIN employment_info e ON u.id = e.user_id
WHERE e.company_name ILIKE '%TSL%';

-- ===========================
-- 3. FILTER BY BANK
-- ===========================
SELECT u.*
FROM users u
JOIN user_bank_info b ON u.id = b.user_id
WHERE b.bank_name ILIKE '%HDFC%';

-- ===========================
-- 4. FILTER BY PINCODE
-- ===========================
SELECT * FROM users WHERE pincode = '560001';

-- ===========================
-- 5. GROUP USERS BY COMPANY
-- ===========================
SELECT company_name, COUNT(*) AS user_count
FROM employment_info
GROUP BY company_name
ORDER BY user_count DESC;

-- ===========================
-- 6. GROUP USERS BY BANK
-- ===========================
SELECT bank_name, COUNT(*) AS user_count
FROM user_bank_info
GROUP BY bank_name;

-- ===========================
-- 7. GROUP USERS BY PINCODE
-- ===========================
SELECT pincode, COUNT(*) AS user_count
FROM users
GROUP BY pincode;
