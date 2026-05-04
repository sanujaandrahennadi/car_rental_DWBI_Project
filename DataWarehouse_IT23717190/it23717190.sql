SELECT QuarterName, COUNT(*)
FROM CarRental_DW.dbo.DimDate
GROUP BY QuarterName
HAVING COUNT(*) > 1


USE CarRental_DW;
GO

SELECT QuarterName, COUNT(*)
FROM DimDate
GROUP BY QuarterName
HAVING COUNT(*) > 1

USE CarRental_DW;
GO

-- Check duplicate QuarterName
SELECT QuarterName, COUNT(*) AS Count
FROM DimDate
GROUP BY QuarterName
HAVING COUNT(*) > 1

USE CarRental_DW;
GO

UPDATE DimDate
SET QuarterName = 
    CAST(YEAR(FullDate) AS VARCHAR) + '-Q' +
    CAST(DATEPART(QUARTER, FullDate) AS VARCHAR)

    USE CarRental_DW;
GO

SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'DimDate'
AND COLUMN_NAME = 'QuarterName'

USE CarRental_DW;
GO

ALTER TABLE DimDate
ALTER COLUMN QuarterName VARCHAR(20);

USE CarRental_DW;
GO

UPDATE DimDate
SET QuarterName = 
    CAST(YEAR(FullDate) AS VARCHAR(4)) + '-Q' +
    CAST(DATEPART(QUARTER, FullDate) AS VARCHAR(1))


USE CarRental_DW;
GO

SELECT DISTINCT QuarterName 
FROM DimDate 
ORDER BY QuarterName



USE CarRental_DW;
GO

-- Step 1: Increase column size
ALTER TABLE DimDate
ALTER COLUMN QuarterName VARCHAR(20);
GO

-- Step 2: Update with unique values
UPDATE DimDate
SET QuarterName = 
    CAST(YEAR(FullDate) AS VARCHAR(4)) + '-Q' +
    CAST(DATEPART(QUARTER, FullDate) AS VARCHAR(1));
GO

-- Step 3: Verify no duplicates remain
SELECT QuarterName, COUNT(*) AS Count
FROM DimDate
GROUP BY QuarterName
HAVING COUNT(*) > 1;





USE CarRental_DW;
GO

-- Check current column size
SELECT COLUMN_NAME, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'DimDate'
AND COLUMN_NAME = 'QuarterName'






-- Fix: Set exact size
ALTER TABLE DimDate
ALTER COLUMN QuarterName VARCHAR(10);
GO

-- Verify
SELECT DISTINCT QuarterName FROM DimDate
ORDER BY QuarterName