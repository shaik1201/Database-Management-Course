from django.shortcuts import render
from django.db import connection

flag1 = False
flag2 = False
flag3 = False

# Create your views here.
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]



def index(request):
    return render(request, 'index.html')

def Query_results(request):
    with connection.cursor() as cursor:
        # Query 1
        global flag1
        global flag2
        global flag3

        if not flag1:
            cursor.execute(
                """
                Create VIEW noChildren
                AS
                SELECT RR1.title, COUNT(H1.hID) as NumberProgReturnedPerHID
                FROM RecordReturns as RR1, Households as H1
                WHERE RR1.hID = H1.hID and H1.ChildrenNum = 0
                GROUP BY RR1.title
                HAVING COUNT(H1.hID) >= 1
                """
            )

            cursor.execute(
                """
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
                """
            )

            cursor.execute(
                """
               CREATE VIEW LSGNoDuplicate
                AS
                SELECT *
                FROM LongestSHowPerGenre as LSG1
                WHERE LSG1.title IN (
                        SELECT top 1 LSG2.title
                        FROM LongestSHowPerGenre AS LSG2
                        WHERE LSG1.genre = LSG2.genre
                    )
                """
            )

        cursor.execute(
            """
           SELECT LSG1.genre, LSG1.title, LSG1.duration
            FROM noChildren as NC1, LSGNoDuplicate as LSG1
            WHERE NC1.title = LSG1.title
            ORDER BY LSG1.genre
            """
        )

        sql_res1 = dictfetchall(cursor)
        flag1 = True

        # Query 2

        if not flag2:
            cursor.execute(
                """
               CREATE VIEW KosherRank
                AS
                SELECT DISTINCT PR1.*
                FROM RecordOrders AS RO1, ProgramRanks AS PR1
                WHERE (RO1.title = PR1.title AND RO1.hID = PR1.hID)
                UNION
                SELECT DISTINCT PR1.*
                FROM RecordReturns AS RR1, ProgramRanks AS PR1
                WHERE (RR1.title = PR1.title AND RR1.hID = PR1.hID)
                """
            )

            cursor.execute(
                """
               CREATE VIEW AtLeast3Kosher
                AS
                SELECT KR1.title
                FROM KosherRank AS KR1
                WHERE KR1.title IN (SELECT KR2.title
                                    FROM KosherRank AS KR2
                                    GROUP BY KR2.title
                                    HAVING COUNT(KR2.rank) >= 3)
                GROUP BY KR1.title
                """
            )

        cursor.execute(
            """
          SELECT KR1.title, CAST(AVG(Cast(PR1.rank AS DECIMAL(10,2))) AS DECIMAL(10,2)) AS AverageRank
            FROM AtLeast3Kosher AS KR1, ProgramRanks AS PR1
            WHERE KR1.title = PR1.title
            GROUP BY KR1.title
            ORDER BY AverageRank DESC, title
            """
        )
        sql_res2 = dictfetchall(cursor)
        flag2 = True

        # Query 3

        if not flag3:

            cursor.execute(
                """
              CREATE VIEW RecordReturnAtLeast10
                AS
                SELECT RR1.title, RR1.hID, H1.netWorth
                FROM RecordReturns AS RR1, Households as H1
                WHERE RR1.title IN (SELECT RR2.title
                                    FROM RecordReturns AS RR2
                                    GROUP BY RR2.title
                                    HAVING COUNT(DISTINCT RR2.hID) >= 10)
                AND RR1.hID = H1.hID
                """
            )

            cursor.execute(
                """
              CREATE VIEW Temp
                AS
                SELECT RR1.title, COUNT(RR1.hID)/2 as CountFamily
                FROM RecordReturnAtLeast10 AS RR1
                GROUP BY RR1.title
                """
            )

            cursor.execute(
                """
                CREATE VIEW Temp2
                AS
                SELECT RR1.title, COUNT(RR1.hID) as CountFamily
                FROM RecordReturnAtLeast10 AS RR1
                WHERE RR1.netWorth >= 8
                GROUP BY RR1.title
                """
            )

            cursor.execute(
                """
              CREATE VIEW LuxuriousTvShow
                AS
                SELECT T1.title
                FROM Temp AS T1, Temp2 AS T2
                WHERE T1.title = T2.title and T2.CountFamily > T1.CountFamily
                GROUP BY T1.title
                """
            )



            cursor.execute(
                """
              CREATE VIEW Temp3
                AS
                SELECT PR1.*
                FROM ProgramRanks as PR1, LuxuriousTvShow as LTS1
                WHERE PR1.title = LTS1.title and PR1.rank < 2
                """
            )

        cursor.execute(
            """
          SELECT *
            FROM LuxuriousTvShow as LTS1
            WHERE LTS1.title NOT IN (SELECT T3.title
                                     FROM Temp3 as T3)
            """
        )

        sql_res3 = dictfetchall(cursor)
        flag3 = True

        return render(request, 'Query_results.html', {'sql_res1': sql_res1, 'sql_res2': sql_res2, 'sql_res3': sql_res3})


def Records_management(request):
    # hID_order = 999999999
    # title_order = 'aaaaaaaaa'



    # check if family exists
    with connection.cursor() as cursor:
        if request.POST and request.POST.get('hID_order') \
                and request.POST.get('title_order'):
            title_order = request.POST.get('title_order')
            hID_order = request.POST.get('hID_order')

            cursor.execute(
                f"""
                    SELECT H.hID
                    FROM Households H
                    WHERE H.hID = {hID_order}
                """
            )
            hIDOrder = dictfetchall(cursor)

        # check if title exists
            cursor.execute(
                f"""
                    SELECT P.title
                    FROM Programs P
                    WHERE P.title = '{title_order}'
                        """
            )
            titleOrder = dictfetchall(cursor)

            # # check orders number of a family
            # cursor.execute(
            #     f"""
            #         SELECT COUNT(RO1.title) AS OrdersNumber
            #         FROM RecordOrders AS RO1
            #         WHERE RO1.hID = {hID_order}
            #         GROUP BY RO1.hID
            #     """
            # )
            # ordersNumber = dictfetchall(cursor)
            #
            # # check if a family order a movie and if yes return his hID
            # cursor.execute(
            #     f"""
            #         SELECT RO1.hID
            #         FROM RecordOrders AS RO1
            #         WHERE RO1.title = {title_order}
            #         """
            # )
            # hIDOwnsRecord = dictfetchall(cursor)
            #
            #
            # # check if family already ordered the title
            # cursor.execute(
            #     f"""
            #             SELECT RR1.hID
            #             FROM RecordReturns AS RR1
            #             WHERE RR1.title = {title_order} and RR1.hID = {hID_order}
            #             """
            # )
            # hIDReturnsRecord = dictfetchall(cursor)
            #
            # # check if there is children in the family and genre of title
            # cursor.execute(
            #     f"""
            #     SELECT H1.ChildrenNum, P1.genre
            #     FROM Households AS H1, Programs AS P1
            #     WHERE H1.hID = {hID_order} AND P1.title = {title_order}
            #     """
            # )
            # childrenNumAndGenre = dictfetchall(cursor)
            # # childrenNum = childrenNumAndGenre[0]['ChildrenNum']
            # # titleGenre = childrenNumAndGenre[0]['genre']


            return render(request, 'Records_management.html', {'titleOrder': titleOrder})
    return render(request, 'Records_management.html', {"x":'a'})









def Rankings(request):
    return render(request, 'Rankings.html')


