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

        ]
}










