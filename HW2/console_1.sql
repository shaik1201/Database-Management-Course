-- SHEILTA 1

CREATE VIEW FamilySizeWealth
AS
SELECT H1.hID, D1.dID
FROM Households AS H1, Devices as D1
WHERE H1.size >= 3 AND H1.netWorth > 5 and H1.hID = D1.hID

CREATE VIEW Reality
AS
SELECT DISTINCT D2.hID, D2.dID
FROM Devices as D2, Programs as P2, Viewing as V2
WHERE D2.dID = V2.dID and P2.pCode = V2.pCode and P2.genre = 'Reality'


SELECT FSW.hID, COUNT(*) As DevicesNum
FROM FamilySizeWealth as FSW
WHERE FSW.hID NOT IN (SELECT R1.hID
                      FROM Reality as R1)
GROUP BY FSW.hID
ORDER BY FSW.hID


-- SHEILTA 2

-- View of TvShow that have be seen by At least 3 families
CREATE VIEW AtLeast3Family
AS
SELECT V1.pCode
FROM Devices as D1, Viewing as V1
WHERE D1.dID = V1.dID
GROUP BY V1.pCode
HAVING COUNT(DISTINCT D1.hID) >= 3


-- View of the longest Or Equal ( >= ) TvShow's duration in each Genre
CREATE VIEW LongestOrEqualDuration
AS
SELECT P1.pCode, P1.title, P1.duration, P1.genre
FROM Programs AS P1
WHERE P1.genre IS NOT NULL
                    EXCEPT
SELECT P2.pCode,P2.title, P2.duration, P2.genre
FROM Programs AS P2, Programs AS P3
WHERE P2.duration < P3.duration AND P2.genre = P3.genre AND P2.genre IS NOT NULL


-- View of the longest duration ( > ) TvShow's duration in each Genre
CREATE VIEW LongestDuration
AS
SELECT *
FROM LongestOrEqualDuration AS P1
WHERE P1.genre IN (SELECT P2.genre
                      FROM LongestOrEqualDuration AS P2
                      GROUP BY P2.genre
                      HAVING COUNT(P2.genre) = 1)


-- View of PopularProgram
CREATE VIEW PopularProgram
AS
SELECT LD.pCode, LD.title, LD.duration, LD.genre
FROM AtLeast3Family ATL INNER JOIN LongestDuration LD ON ATL.pCode = LD.pCode


-- View of Modern Family + Popular Program details
CREATE VIEW ModernFamily
AS
SELECT DISTINCT D1.hID, D1.dID, V1.pCode, V1.eTime, PP1.title
FROM Devices AS D1, Viewing AS V1, PopularProgram AS PP1
WHERE D1.dID = V1.dID AND PP1.pCode = V1.pCode AND D1.hID IN (SELECT D2.hID
                                                                 FROM Devices AS D2, Viewing AS V2, PopularProgram AS PP2
                                                                 WHERE D2.dID = V2.dID and V2.pCode = PP2.pCode
                                                                 GROUP BY D2.hID
                                                                 HAVING (COUNT(DISTINCT PP2.pCode) >= 3))

-- Solution
SELECT MF1.hID, MF1.title, MF1.eTime AS eventTime
FROM ModernFamily AS MF1
        EXCEPT
SELECT MF2.hID, MF2.title, MF2.eTime
FROM ModernFamily AS MF2,ModernFamily AS MF3
WHERE MF2.eTime > MF3.eTime AND MF2.hID = MF3.hID
ORDER BY eventTime, hID


-------------------------

CREATE VIEW three_in_program
AS
SELECT COUNT(DISTINCT D1.hID) as hID1 , V1.pCode
FROM Viewing V1 , Devices D1
WHERE ( V1.dID = D1.dID )
GROUP BY V1.pCode
HAVING COUNT(DISTINCT D1.hID) >= 3

SELECT P.*
FROM three_in_program as tip, Programs as P
Where tip.pCode = P.pCode AND P.duration > ALL (SELECT P1.duration
                                                FROM three_in_program as tip1, Programs as P1
                                                WHERE P.genre = P1.genre)