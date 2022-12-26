QUERY_ANSWERS = {
    "Q3":
        """ SELECT FSW.hID, COUNT(*) As DevicesNum
            FROM FamilySizeWealth as FSW
            WHERE FSW.hID NOT IN (SELECT R1.hID
                                  FROM Reality as R1)
            GROUP BY FSW.hID
            ORDER BY FSW.hID; """
    ,
    "Q4":
        """ SELECT MF1.hID, MF1.title, MF1.eTime AS eventTime
            FROM ModernFamily AS MF1
                    EXCEPT
            SELECT MF2.hID, MF2.title, MF2.eTime
            FROM ModernFamily AS MF2,ModernFamily AS MF3
            WHERE MF2.eTime > MF3.eTime AND MF2.hID = MF3.hID
            ORDER BY eventTime, hID; """
}
