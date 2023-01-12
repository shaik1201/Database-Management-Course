-- First Query
Create VIEW noChildren
AS
SELECT RR1.title, COUNT(H1.hID) as NumberProgReturnedPerHID
FROM RecordReturns as RR1, Households as H1
WHERE RR1.hID = H1.hID and H1.ChildrenNum = 0
GROUP BY RR1.title
HAVING COUNT(H1.hID) >= 1


CREATE VIEW LongestSHowPerGenre
AS
SELECT *
FROM Programs as P1
WHERE P1.duration >= ALL (SELECT P2.duration
                         FROM Programs as P2
                         WHERE P1.genre = P2.genre
                         )
                    AND P1.genre LIKE 'A%'
GROUP BY P1.genre, title, duration


CREATE VIEW LSGNoDuplicate
AS
SELECT *
FROM LongestSHowPerGenre as LSG1
WHERE LSG1.title IN (
        SELECT top 1 LSG2.title
        FROM LongestSHowPerGenre AS LSG2
        WHERE LSG1.genre = LSG2.genre
    )


SELECT LSG1.genre, LSG1.title, LSG1.duration
FROM noChildren as NC1, LSGNoDuplicate as LSG1
WHERE NC1.title = LSG1.title
ORDER BY LSG1.genre



-- Second Query

CREATE VIEW KosherRank
AS
SELECT DISTINCT PR1.*
FROM RecordOrders AS RO1, ProgramRanks AS PR1
WHERE (RO1.title = PR1.title AND RO1.hID = PR1.hID)
UNION
SELECT DISTINCT PR1.*
FROM RecordReturns AS RR1, ProgramRanks AS PR1
WHERE (RR1.title = PR1.title AND RR1.hID = PR1.hID)



CREATE VIEW AtLeast3Kosher
AS
SELECT KR1.title
FROM KosherRank AS KR1
WHERE KR1.title IN (SELECT KR2.title
                    FROM KosherRank AS KR2
                    GROUP BY KR2.title
                    HAVING COUNT(KR2.rank) >= 3)
GROUP BY KR1.title


-- CREATE VIEW Temp
-- AS
SELECT KR1.title, CAST(AVG(Cast(PR1.rank AS DECIMAL(10,2))) AS DECIMAL(10,2)) AS AverageRank
FROM AtLeast3Kosher AS KR1, ProgramRanks AS PR1
WHERE KR1.title = PR1.title
GROUP BY KR1.title
ORDER BY AverageRank DESC, title



-- Third Query
CREATE VIEW RecordReturnAtLeast10
AS
SELECT RR1.title, RR1.hID, H1.netWorth
FROM RecordReturns AS RR1, Households as H1
WHERE RR1.title IN (SELECT RR2.title
                    FROM RecordReturns AS RR2
                    GROUP BY RR2.title
                    HAVING COUNT(DISTINCT RR2.hID) >= 10)
AND RR1.hID = H1.hID


CREATE VIEW Temp
AS
SELECT RR1.title, COUNT(RR1.hID)/2 as CountFamily
FROM RecordReturnAtLeast10 AS RR1
GROUP BY RR1.title

CREATE VIEW Temp2
AS
SELECT RR1.title, COUNT(RR1.hID) as CountFamily
FROM RecordReturnAtLeast10 AS RR1
WHERE RR1.netWorth >= 8
GROUP BY RR1.title

CREATE VIEW LuxuriousTvShow
AS
SELECT T1.title
FROM Temp AS T1, Temp2 AS T2
WHERE T1.title = T2.title and T2.CountFamily > T1.CountFamily
GROUP BY T1.title


CREATE VIEW Temp3
AS
SELECT PR1.*
FROM ProgramRanks as PR1, LuxuriousTvShow as LTS1
WHERE PR1.title = LTS1.title and PR1.rank < 2

SELECT *
FROM LuxuriousTvShow as LTS1
WHERE LTS1.title NOT IN (SELECT T3.title
                         FROM Temp3 as T3)