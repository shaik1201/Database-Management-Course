CREATE TABLE Company (
    companyNumber INTEGER PRIMARY KEY,
    companyName VARCHAR(50),
    companyFoundationYear CHAR(4),
    companyWebsite VARCHAR(50) UNIQUE CHECK (companyWebsite LIKE '_%.com'),
    companyDomain VARCHAR(50)
)

CREATE TABLE Department(
    deptName VARCHAR(50),
    deptDescription VARCHAR(100),
    companyNumber INTEGER,
    FOREIGN KEY (companyNumber)
        REFERENCES Company(companyNumber) ON DELETE CASCADE,
    PRIMARY KEY (deptName, companyNumber),
    UNIQUE (companyNumber, deptDescription)
)

CREATE TABLE Salary(
    positionName VARCHAR(50) PRIMARY KEY,
    salary FLOAT NOT NULL CHECK (salary > 0),
    experienceLevel VARCHAR(20)
        CHECK (experienceLevel = 'Entry Level' or
               experienceLevel = 'Associate' or
               experienceLevel = 'Director' or
               experienceLevel = 'Executive')
    UNIQUE (positionName, experienceLevel)
)

CREATE TABLE Recruiter(
    recruiterID CHAR(9) PRIMARY KEY,
    recruiterName VARCHAR(50),
    bonus FLOAT
)

CREATE TABLE Job(
    jobNumber INTEGER PRIMARY KEY NOT NULL,
    deptName VARCHAR(50) NOT NULL,
    companyNumber INTEGER NOT NULL,
    positionName VARCHAR(50) NOT NULL,
    experienceLevel VARCHAR(20) NOT NULL,
    monthlyHours INTEGER DEFAULT (182) NOT NULL,
    recruiterID CHAR(9) NOT NULL,
    FOREIGN KEY (deptName, companyNumber)
            REFERENCES Department(deptName, companyNumber) ON DELETE CASCADE,
    FOREIGN KEY (positionName, experienceLevel)
            REFERENCES Salary (positionName, experienceLevel),
    FOREIGN KEY (recruiterID)
            REFERENCES Recruiter(recruiterID),
    UNIQUE (jobNumber, recruiterID),
);

