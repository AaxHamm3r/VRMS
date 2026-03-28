-- Vehicle Rental Management System (VRMS)


DROP DATABASE IF EXISTS VRMS;
CREATE DATABASE VRMS;
USE VRMS;


-- 1. VehicleType
CREATE TABLE VehicleType (
   VehicleTypeID INT PRIMARY KEY AUTO_INCREMENT,
   TypeName VARCHAR(50) NOT NULL UNIQUE
);


-- 2. RentalBranch
CREATE TABLE RentalBranch (
   BranchID INT PRIMARY KEY AUTO_INCREMENT,
   Name VARCHAR(100) NOT NULL,
   Address VARCHAR(200) NOT NULL,
   PhoneNumber VARCHAR(20) NOT NULL
);


-- 3. Customer
CREATE TABLE Customer (
   CustomerID INT PRIMARY KEY AUTO_INCREMENT,
   FirstName VARCHAR(50) NOT NULL,
   LastName VARCHAR(50) NOT NULL,
   Address VARCHAR(200),
   Phone VARCHAR(20),
   Email VARCHAR(100),
   DriversLicenseNumber VARCHAR(50) NOT NULL UNIQUE,
   LicenseExpiryDate DATE NOT NULL
);


-- 4. Vehicle
CREATE TABLE Vehicle (
   VehicleID INT PRIMARY KEY AUTO_INCREMENT,
   LicensePlate VARCHAR(20) NOT NULL UNIQUE,
   Make VARCHAR(50) NOT NULL,
   Model VARCHAR(50) NOT NULL,
   Year INT NOT NULL,
   Color VARCHAR(30),
   DailyRate DECIMAL(10,2) NOT NULL,
   CurrentMileage INT NOT NULL,
   VehicleTypeID INT NOT NULL,
   BranchID INT NOT NULL,
   FOREIGN KEY (VehicleTypeID) REFERENCES VehicleType(VehicleTypeID),
   FOREIGN KEY (BranchID) REFERENCES RentalBranch(BranchID)
);


-- 5. MaintenanceStaff
CREATE TABLE MaintenanceStaff (
   StaffID INT PRIMARY KEY AUTO_INCREMENT,
   Name VARCHAR(100) NOT NULL,
   OfficeNumber VARCHAR(20),
   PhoneNumber VARCHAR(20),
   Email VARCHAR(100),
   BranchID INT NOT NULL,
   FOREIGN KEY (BranchID) REFERENCES RentalBranch(BranchID)
);


-- 6. RentalAgreement
CREATE TABLE RentalAgreement (
   AgreementID INT PRIMARY KEY AUTO_INCREMENT,
   CustomerID INT NOT NULL,
   VehicleID INT NOT NULL,
   PickupBranchID INT NOT NULL,
   ReturnBranchID INT NOT NULL,
   ScheduledPickup DATETIME NOT NULL,
   ScheduledReturn DATETIME NOT NULL,
   ActualPickup DATETIME,
   ActualReturn DATETIME,
   EstimatedCost DECIMAL(10,2),
   ActualCost DECIMAL(10,2),
   Status VARCHAR(20) NOT NULL,
   CHECK (Status IN ('Booked','Active','Completed','Cancelled')),
   FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
   FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID),
   FOREIGN KEY (PickupBranchID) REFERENCES RentalBranch(BranchID),
   FOREIGN KEY (ReturnBranchID) REFERENCES RentalBranch(BranchID)
);


-- 7. MaintenanceRecord
CREATE TABLE MaintenanceRecord (
   MaintenanceID INT PRIMARY KEY AUTO_INCREMENT,
   DateReported DATE NOT NULL,
   TimeReported TIME NOT NULL,
   VehicleID INT NOT NULL,
   ReportingCustomerID INT,
   IssueType VARCHAR(20) NOT NULL,
   Description TEXT,
   Status VARCHAR(25) NOT NULL,
   DateResolved DATE,
   TimeResolved TIME,
   StaffID INT,
   Notes TEXT,
   CHECK (IssueType IN ('Routine','Urgent')),
   CHECK (Status IN ('Reported','In-Progress','Complete','Awaiting Parts')),
   FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID),
   FOREIGN KEY (ReportingCustomerID) REFERENCES Customer(CustomerID),
   FOREIGN KEY (StaffID) REFERENCES MaintenanceStaff(StaffID)
);
