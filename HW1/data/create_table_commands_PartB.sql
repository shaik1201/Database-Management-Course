
CREATE TABLE Employee(
    eID int primary key,
    compID int not null,
    depName varchar(50) not null,
    hourlyWage int not null,
    check (eID > 0 and compID > 0 and hourlyWage > 0)
);

CREATE TABLE Project(
    compID int,
    depName varchar(50),
    pID int,
    budget int not null,
    check (compID > 0 and pID > 0 and budget > 0),
    primary key (compID, depName, pID)
);

CREATE TABLE WorkOnProject(
    compID int,
    depName varchar(50),
    pID int,
    wDate date,
    eID int,
    hours int not null,
    check (hours > 0),
    primary key (compID, depName, pID, wDate, eID),
    foreign key (compID, depName, pID) references Project,
    foreign key (eID) references Employee
);
