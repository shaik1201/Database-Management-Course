QUERY_ANSWERS = {
    "Q3":
        """
        SELECT FSW.hID, COUNT(*) As DevicesNum
        FROM FamilySizeWealth as FSW
        WHERE FSW.hID NOT IN (SELECT R1.hID
                              FROM Reality as R1)
        GROUP BY FSW.hID
        ORDER BY FSW.hID
        """
    ,
    "Q4":
        """

        """
}
