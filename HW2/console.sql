CREATE TABLE Department(
    deptName VARCHAR(100) PRIMARY KEY,
    deptDescription VARCHAR(100),
    managerID INTEGER NOT NULL,
--  FOREIGN KEY (managerID) REFERENCES Manager(managerID)
--  Tirgoul 1 page 24
)

CREATE TABLE Employee(
    employeeID INTEGER PRIMARY KEY CHECK ( employeeID >= 0 ),
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

-- We can not check the cover constraint
CREATE TABLE Family(
    familyID INTEGER PRIMARY KEY CHECK ( familyID >= 0 ),
    familyName VARCHAR(100),
    wealthLevel INTEGER CHECK (wealthLevel BETWEEN 1 AND 9),
    UNIQUE (familyID, wealthLevel)
)

CREATE TABLE Person(
    firstName VARCHAR(100),
    personPhoneNumber INTEGER CHECK ( employeeID >= 0 ),
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
    submissionDate DATE,
    finalDecision VARCHAR(100),
    disconnectionReason VARCHAR(100),
    managerID INTEGER,
    familyID INTEGER,
    FOREIGN KEY (managerID) REFERENCES Manager(managerID) ON DELETE CASCADE,
    FOREIGN KEY (familyID) REFERENCES NormalFamily(familyID),
    PRIMARY KEY (managerID, familyID, submissionDate)
)


CREATE TABLE TransferRequest(
    transferReason VARCHAR(100),
    fromManagerID INTEGER,
    familyID INTEGER,
    submissionDate DATE,
    toManagerID INTEGER,
    CHECK (fromManagerID != toManagerID),
    FOREIGN KEY (fromManagerID, familyID, submissionDate) REFERENCES disconnectionRequest(managerID, familyID, submissionDate) ON DELETE CASCADE,
    FOREIGN KEY (toManagerID) REFERENCES Manager(managerID),
    PRIMARY KEY (toManagerID, familyID, submissionDate)
)

---- change
CREATE TABLE DigitalConverter(
    serialNumber INTEGER CHECK ( serialNumber >= 0 ),
    familyID INTEGER,
    FOREIGN KEY (familyID) REFERENCES Family(familyID) ON DELETE CASCADE,
    PRIMARY KEY (serialNumber,familyID)
)

CREATE TABLE FixedBy(
    cost FLOAT CHECK ( cost >= 0 ),
    technicalExpertID INTEGER,
    serialNumber INTEGER PRIMARY KEY,
    familyID INTEGER
    FOREIGN KEY (technicalExpertID) REFERENCES TechnicalExpert(technicalExpertID),
    FOREIGN KEY (serialNumber, familyID) REFERENCES DigitalConverter(serialNumber,familyID) ON DELETE CASCADE,
)

---- change
CREATE TABLE Channel(
    channelNumber INTEGER PRIMARY KEY CHECK ( channelNumber >= 0 ),
    channelName VARCHAR(100)
)

---- change
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
    serialNumber INTEGER PRIMARY KEY,
    switchingDate VARCHAR(100),
    CHECK (channelNumberFrom != channelNumberTo),
    FOREIGN KEY (channelNumberFrom, serialNumber) REFERENCES DCcontainsChannel(channelNumber, serialNumber) ON DELETE CASCADE,
    FOREIGN KEY (channelNumberTo) REFERENCES Channel(channelNumber),

)

CREATE TABLE TvShow(
    tvShowName VARCHAR(100) PRIMARY KEY,
    tvShowGenre VARCHAR(100),
    tvShowDuration INTEGER CHECK ( tvShowDuration >= 0 )
)

CREATE TABLE ChannelBroadcastTvShow(
    channelNumber INTEGER,
    tvShowName VARCHAR(100),
    schedule VARCHAR(100) NOT NULL,
    PRIMARY KEY (channelNumber, tvShowName),
    FOREIGN KEY (channelNumber) REFERENCES Channel(channelNumber) ON DELETE CASCADE,
    FOREIGN KEY (tvShowName) REFERENCES TvShow(tvShowName)
)


