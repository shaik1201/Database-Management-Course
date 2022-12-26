CREATE TABLE Households(
    hID         INTEGER PRIMARY KEY,
    size        INTEGER,
    netWorth    INTEGER
);

CREATE TABLE Devices(
    dID         VARCHAR(20) PRIMARY KEY,
    hID         INTEGER NOT NULL,
    FOREIGN KEY (hID) REFERENCES Households
                    ON DELETE CASCADE
);

CREATE TABLE Programs(
    pCode       VARCHAR(20) PRIMARY KEY,
    title       VARCHAR(45),
    genre       VARCHAR(25),
    duration    INT
);

CREATE TABLE Viewing(
    dID         VARCHAR(20),
    eTime   DATETIME,
    pCode       VARCHAR(20) NOT NULL,
    PRIMARY KEY (dID, eTime),
    FOREIGN KEY (dID) REFERENCES Devices
                ON DELETE CASCADE,
    FOREIGN KEY (pCode) REFERENCES Programs
                    ON DELETE CASCADE
);
