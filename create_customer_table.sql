CREATE TABLE Lib_customer (
    Customer_ID INT PRIMARY KEY,
    First_Name VARCHAR(100),
    Last_Name VARCHAR(100),
    MemberID VARCHAR(50),
    Expiration DATE,
    Books_CheckedOut INT,
    Member_Since DATE
);

INSERT INTO Lib_customer (Customer_ID, First_Name, Last_Name, MemberID, Expiration, Books_CheckedOut, Member_Since) VALUES
(1, 'Alice', 'Johnson', 'M1001', '2026-12-31', 2, '2023-01-15'),
(2, 'Bob', 'Smith', 'M1002', '2025-10-20', 1, '2022-04-10'),
(3, 'Carol', 'Davis', 'M1003', '2026-08-15', 3, '2021-09-05'),
(4, 'David', 'Wilson', 'M1004', '2027-02-14', 0, '2024-03-22'),
(5, 'Emma', 'Brown', 'M1005', '2026-05-01', 4, '2020-11-18'),
(6, 'Frank', 'Moore', 'M1006', '2025-11-30', 2, '2023-07-08'),
(7, 'Grace', 'Taylor', 'M1007', '2027-01-10', 1, '2022-06-12'),
(8, 'Henry', 'Anderson', 'M1008', '2026-09-25', 5, '2019-12-03'),
(9, 'Isabella', 'Thomas', 'M1009', '2027-03-20', 0, '2024-05-14'),
(10, 'Jack', 'Jackson', 'M1010', '2026-07-18', 3, '2021-02-09');

-- Update a customer's information
UPDATE Lib_customer
SET Books_CheckedOut = 4
WHERE Customer_ID = 1;

-- Delete a customer record
DELETE FROM Lib_customer
WHERE Customer_ID = 10;

-- Select all customers
SELECT * FROM Lib_customer;

-- Select a specific customer
SELECT Customer_ID, First_Name, Last_Name
FROM Lib_customer
WHERE Customer_ID = 1;

drop table Lib_customer
