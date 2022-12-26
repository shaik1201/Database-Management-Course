VIEWS_DICT = {
    "Q3":
        ["""CREATE VIEW FamilySizeWealth
            AS
            SELECT H1.hID, D1.dID
            FROM Households AS H1, Devices as D1
            WHERE H1.size >= 3 AND H1.netWorth > 5 and H1.hID = D1.hID;""",
         """CREATE VIEW Reality
            AS
            SELECT DISTINCT D2.hID, D2.dID
            FROM Devices as D2, Programs as P2, Viewing as V2
            WHERE D2.dID = V2.dID and P2.pCode = V2.pCode and P2.genre = 'Reality';"""
        ]
    ,
    "Q4":
        [
        """CREATE VIEW AtLeast3Family
            AS
            SELECT V1.pCode
            FROM Devices as D1, Viewing as V1
            WHERE D1.dID = V1.dID
            GROUP BY V1.pCode
            HAVING COUNT(DISTINCT D1.hID) >= 3;""",
        """ CREATE VIEW LongestOrEqualDuration
            AS
            SELECT P1.pCode, P1.title, P1.duration, P1.genre
            FROM Programs AS P1
            WHERE P1.genre IS NOT NULL
                                EXCEPT
            SELECT P2.pCode,P2.title, P2.duration, P2.genre
            FROM Programs AS P2, Programs AS P3
            WHERE P2.duration < P3.duration AND P2.genre = P3.genre AND P2.genre IS NOT NULL;""",
        """ CREATE VIEW LongestDuration
            AS
            SELECT *
            FROM LongestOrEqualDuration AS P1
            WHERE P1.genre IN (SELECT P2.genre
                                  FROM LongestOrEqualDuration AS P2
                                  GROUP BY P2.genre
                                  HAVING COUNT(P2.genre) = 1);""",
        """ CREATE VIEW PopularProgram
            AS
            SELECT LD.pCode, LD.title, LD.duration, LD.genre
            FROM AtLeast3Family ATL INNER JOIN LongestDuration LD ON ATL.pCode = LD.pCode; """,
        """ CREATE VIEW ModernFamily
            AS
            SELECT DISTINCT D1.hID, D1.dID, V1.pCode, V1.eTime, PP1.title
            FROM Devices AS D1, Viewing AS V1, PopularProgram AS PP1
            WHERE D1.dID = V1.dID AND PP1.pCode = V1.pCode AND D1.hID IN (SELECT D2.hID
                                                                             FROM Devices AS D2, Viewing AS V2, PopularProgram AS PP2
                                                                             WHERE D2.dID = V2.dID and V2.pCode = PP2.pCode
                                                                             GROUP BY D2.hID
                                                                             HAVING (COUNT(DISTINCT PP2.pCode) >= 3));"""
            ]
}










