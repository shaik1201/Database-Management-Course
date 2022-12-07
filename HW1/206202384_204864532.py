QUERIES_ANSWER = {
    "Q2":
        """
        SELECT WOP.compID, WOP.depName, COUNT(DISTINCT eID) AS Employees_Count
        FROM WorkOnProject WOP
        WHERE EXISTS (
            SELECT WOP2.eID, WOP2.pID
            FROM WorkOnProject WOP2
            WHERE WOP2.eID = WOP.eID
        GROUP BY WOP2.eID, WOP2.pID
        HAVING COUNT(WOP2.wDate) > 5)
        GROUP BY WOP.depName, WOP.compID
        ORDER BY WOP.depName ASC;
        """
    ,

    "Q3":
        """
        SELECT P.compID, AVG(P.budget) as Avg_Budget
        FROM Project P
        WHERE P.compID Not In (SELECT P1.compID
                                FROM WorkOnProject WOP, Employee E, Project P1
                                WHERE P1.compID = E.compID and P1.depName = E.depName and
                                      P1.pID = WOP.pID and E.eID = WOP.eID
                                GROUP BY P1.compID, P1.budget, P1.depName
                                HAVING SUM(E.hourlyWage * WOP.hours) > P1.budget)
        GROUP BY P.compID
        ORDER BY Avg_Budget DESC
        """
    ,

    "Q4":
        """
        SELECT DISTINCT E.compID
        FROM Employee E
        WHERE NOT EXISTS(
                        SELECT P.pID
                        FROM Project P
                        WHERE P.compID = E.compID and
                              P.depName = E.depName

                        EXCEPT (
                            SELECT WOP.pID
                            FROM WorkOnProject WOP
                            WHERE WOP.eID = E.eID and
                                  WOP.depName = E.depName and
                                  WOP.compID = E.compID))
        and E.hourlyWage >= all (
                    SELECT E3.hourlyWage
                    FROM Employee E3
                    WHERE E3.depName = E.depName and E3.compID = E.compID)
        """

}
