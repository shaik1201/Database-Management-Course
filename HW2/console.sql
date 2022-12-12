CREATE TABLE Department(
    deptName VARCHAR(100) PRIMARY KEY,
    deptDescription VARCHAR(100),
    managerID INTEGER NOT NULL,
--  FOREIGN KEY (managerID) REFERENCES Manager(managerID)
--  Tirgoul 1 page 24
)

CREATE TABLE Employee(
    employeeID INTEGER PRIMARY KEY,
    employeeName VARCHAR(100),
    deptName VARCHAR(100) NOT NULL,
    FOREIGN KEY (deptName) REFERENCES Department(deptName) ON DELETE CASCADE
)

CREATE TABLE Manager(
    salary INTEGER,
    managerID INTEGER PRIMARY KEY,
    FOREIGN KEY (managerID) REFERENCES Employee(employeeID) ON DELETE CASCADE
)

CREATE TABLE TechnicalExpert(
    expertiseArea VARCHAR(100),
    technicalExpertID INTEGER PRIMARY KEY ,
    FOREIGN KEY (technicalExpertID) REFERENCES Employee(employeeID) ON DELETE CASCADE
)

-- We can not check if a family has at least one person
-- We can not check the cover constraint
CREATE TABLE Family(
    familyID INTEGER PRIMARY KEY,
    familyName VARCHAR(100),
    wealthLevel INTEGER CHECK (wealthLevel BETWEEN 1 AND 9),
    UNIQUE (familyID, wealthLevel)
)

CREATE TABLE Person(
    firstName VARCHAR(100),
    personPhoneNumber INTEGER,
    personBirthDate VARCHAR(100),
    familyID INTEGER,
    FOREIGN KEY (familyID) REFERENCES Family(familyID) ON DELETE CASCADE,
    PRIMARY KEY (firstName, familyID)
)

CREATE TABLE NormalFamily(
    familyID INTEGER PRIMARY KEY ,
    wealthLevel INTEGER CHECK (wealthLevel < 7),
    FOREIGN KEY (familyID,wealthLevel) REFERENCES Family(familyID, wealthLevel) ON DELETE CASCADE ,
)

CREATE TABLE PremiumFamily(
    familyID INTEGER PRIMARY KEY ,
    wealthLevel INTEGER CHECK (wealthLevel >= 7),
    technicalExpertID INTEGER,
    FOREIGN KEY (familyID,wealthLevel) REFERENCES Family(familyID, wealthLevel) ON DELETE CASCADE,
    FOREIGN KEY (technicalExpertID) REFERENCES TechnicalExpert(technicalExpertID)
)

CREATE TABLE DisconnectionRequest(
    submissionDate varchar(100),
    finalDecision varchar(100),
    disconnectionReason varchar(100),
    managerID INTEGER,
    familyID INTEGER,
    wealthLevel INTEGER,
    FOREIGN KEY (managerID) REFERENCES Manager(managerID) ON DELETE CASCADE,
    PRIMARY KEY (managerID, familyID, submissionDate)
)


CREATE TABLE TransferRequest(
    transferReason VARCHAR(100),
    fromManagerID INTEGER,
    familyID INTEGER,
    submissionDate VARCHAR(100),
    toManagerID INTEGER,
    CHECK (fromManagerID != toManagerID),
    FOREIGN KEY (fromManagerID, familyID, submissionDate) REFERENCES disconnectionRequest(managerID, familyID, submissionDate) ON DELETE CASCADE,
    FOREIGN KEY (toManagerID) REFERENCES Manager(managerID),
    PRIMARY KEY (toManagerID, familyID, submissionDate)
)

CREATE TABLE DigitalConverter(
    serialNumber INTEGER PRIMARY KEY,
    familyID INTEGER,
    FOREIGN KEY (familyID) REFERENCES Family(familyID) ON DELETE CASCADE,
    UNIQUE (serialNumber,familyID)
)

CREATE TABLE FixedBy(
    cost FLOAT,
    technicalExpertID INTEGER,
    serialNumber INTEGER PRIMARY KEY,
    familyID INTEGER
    FOREIGN KEY (technicalExpertID) REFERENCES TechnicalExpert(technicalExpertID),
    FOREIGN KEY (serialNumber, familyID) REFERENCES DigitalConverter(serialNumber,familyID) ON DELETE CASCADE,
)

CREATE TABLE Channel(
    channelNumber INTEGER PRIMARY KEY,
    channelName VARCHAR(100)
)

-- ON DELETE CASCADE ???????
CREATE TABLE DCcontainsChannel(
    channelNumber INTEGER,
    serialNumber INTEGER,
    FOREIGN KEY (channelNumber) REFERENCES Channel(channelNumber),
    FOREIGN KEY (serialNumber) REFERENCES DigitalConverter(serialNumber),
    PRIMARY KEY (channelNumber,serialNumber)
)

CREATE TABLE SwitchingChannel(
    channelNumberFrom INTEGER,
    channelNumberTo INTEGER,
    serialNumberFrom INTEGER,
    serialNumberTo INTEGER,
    switchingDate VARCHAR(100),
    CHECK (channelNumberFrom != channelNumberTo),
    CHECK (serialNumberFrom = serialNumberTo),
    FOREIGN KEY (channelNumberFrom, serialNumberFrom) REFERENCES DCcontainsChannel(channelNumber, serialNumber) ON DELETE CASCADE,
    FOREIGN KEY (channelNumberTo, serialNumberTo) REFERENCES DCcontainsChannel(channelNumber, serialNumber),
    PRIMARY KEY (channelNumberFrom, channelNumberTo, switchingDate),
)

CREATE TABLE TvShow(
    tvShowName VARCHAR(100) PRIMARY KEY,
    tvShowGenre VARCHAR(100),
    tvShowDuration INTEGER
)

CREATE TABLE ChannelBroadcastTvShow(
    channelNumber INTEGER,
    tvShowName VARCHAR(100),
    schedule VARCHAR(100) NOT NULL,
    PRIMARY KEY (channelNumber, tvShowName),
    FOREIGN KEY (channelNumber) REFERENCES Channel(channelNumber) ON DELETE CASCADE,
    FOREIGN KEY (tvShowName) REFERENCES TvShow(tvShowName)
)


