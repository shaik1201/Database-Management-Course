from django.shortcuts import render
from django.db import connection

from . import models

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

        # Query 2

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

        # Query 3

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

        cursor.execute(
            """
            DROP VIEW AtLeast3Kosher;
            DROP VIEW KosherRank;
            DROP VIEW LongestSHowPerGenre;
            DROP VIEW LSGNoDuplicate;
            DROP VIEW LuxuriousTvShow;
            DROP VIEW noChildren;
            DROP VIEW RecordReturnAtLeast10;
            DROP VIEW Temp;
            DROP VIEW Temp2;
            DROP VIEW Temp3;
            """
        )

        return render(request, 'Query_results.html', {'sql_res1': sql_res1, 'sql_res2': sql_res2, 'sql_res3': sql_res3})


def Records_management(request):
    if not request.POST:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                    SELECT Top 3 hID, COUNT(title) AS count
                    FROM
                    (
                        SELECT hID, title FROM RecordOrders
                        UNION
                        SELECT hID, title FROM RecordReturns
                    ) AS combined
                    GROUP BY hID
                    ORDER BY count DESC
                """
            )
            table = dictfetchall(cursor)
        return render(request, 'Records_management.html', {"table": table})

    else:
        with connection.cursor() as cursor:
            if request.POST and request.POST.get('hID_order') \
                    and request.POST.get('title_order'):
                title_order = request.POST.get('title_order')
                hID_order = request.POST.get('hID_order')

                # top 3 for the table
                cursor.execute(
                    f"""
                                    SELECT Top 3 hID, COUNT(title) AS count
                                    FROM
                                    (
                                        SELECT hID, title FROM RecordOrders
                                        UNION
                                        SELECT hID, title FROM RecordReturns
                                    ) AS combined
                                    GROUP BY hID
                                    ORDER BY count DESC
                                """
                )
                table = dictfetchall(cursor)

                # check if family exists
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

                # check orders number of a family
                cursor.execute(
                    f"""
                        SELECT COUNT(RO1.title) AS OrdersNumber
                        FROM RecordOrders AS RO1
                        WHERE RO1.hID = {hID_order}
                        GROUP BY RO1.hID
                    """
                )
                ordersNumber = dictfetchall(cursor)

                # check if a family order a movie and if yes return his hID
                cursor.execute(
                    f"""
                        SELECT RO1.hID
                        FROM RecordOrders AS RO1
                        WHERE RO1.title = '{title_order}'
                        """
                )
                hIDOwnsRecord = dictfetchall(cursor)

                # check if family already ordered the title
                cursor.execute(
                    f"""
                            SELECT RR1.hID
                            FROM RecordReturns AS RR1
                            WHERE RR1.title = '{title_order}' and RR1.hID = {hID_order}
                            """
                )
                hIDReturnsRecord = dictfetchall(cursor)

                # check if there is children in the family and genre of title
                cursor.execute(
                    f"""
                    SELECT H1.ChildrenNum, P1.genre
                    FROM Households AS H1, Programs AS P1
                    WHERE H1.hID = {hID_order} AND P1.title = '{title_order}'
                    """
                )
                childrenNumAndGenre = dictfetchall(cursor)
                if childrenNumAndGenre:
                    childrenNum = childrenNumAndGenre[0]['ChildrenNum']
                    titleGenre = childrenNumAndGenre[0]['genre']


                if not hIDOrder:
                    return render(request, 'Records_management.html', {'error': 'Family hID was not found', 'table': table})

                if not titleOrder:
                    return render(request, 'Records_management.html', {'error': 'Movie title was not found', 'table': table})

                if ordersNumber and ordersNumber[0]['OrdersNumber'] >= 3:
                    return render(request, 'Records_management.html', {'error': 'Family already has 3 records', 'table': table})

                if hIDOwnsRecord:
                    if str(hIDOwnsRecord[0]['hID']) == hID_order:
                        return render(request, 'Records_management.html', {'error': "Family already owns this record's title", 'table': table})
                    else:
                        return render(request, 'Records_management.html', {'error': "Another family already owns this record's title", 'table': table})

                if hIDReturnsRecord:
                    return render(request, 'Records_management.html', {'error': "Family already ordered this record's title before", 'table': table})

                if childrenNumAndGenre and childrenNum > 0 and (titleGenre == 'Reality' or titleGenre == 'Adults only'):
                    return render(request, 'Records_management.html', {'error': "Family has kids therefore the genre is inappropriate", 'table': table})

                # add the record to RecordOrders
                cursor.execute(
                    f"""
                        INSERT INTO RecordOrders (hID, title) VALUES ({hID_order}, '{title_order}');
                    """
                )

                cursor.execute(
                    f"""
                         SELECT Top 3 hID, COUNT(title) AS count
                         FROM
                         (
                             SELECT hID, title FROM RecordOrders
                             UNION
                             SELECT hID, title FROM RecordReturns
                         ) AS combined
                         GROUP BY hID
                         ORDER BY count DESC
                     """
                )
                table = dictfetchall(cursor)

                return render(request, 'Records_management.html', {'success': 'Order successfully added!', 'table': table})

            if request.POST and request.POST.get('hID_return') \
                    and request.POST.get('title_return'):
                title_return = request.POST.get('title_return')
                hID_return = request.POST.get('hID_return')

                # top 3 table
                cursor.execute(
                    f"""
                                                 SELECT Top 3 hID, COUNT(title) AS count
                                                 FROM
                                                 (
                                                     SELECT hID, title FROM RecordOrders
                                                     UNION
                                                     SELECT hID, title FROM RecordReturns
                                                 ) AS combined
                                                 GROUP BY hID
                                                 ORDER BY count DESC
                                             """
                )
                table = dictfetchall(cursor)

                # check if family exists
                cursor.execute(
                    f"""
                                        SELECT H.hID
                                        FROM Households H
                                        WHERE H.hID = {hID_return}
                                    """
                )
                hIDReturn = dictfetchall(cursor)

                # check if title exists
                cursor.execute(
                    f"""
                                        SELECT P.title
                                        FROM Programs P
                                        WHERE P.title = '{title_return}'
                                            """
                )
                titleReturn = dictfetchall(cursor)

                # check if a family order a movie and if yes return his hID
                cursor.execute(
                    f"""
                                        SELECT RO1.hID
                                        FROM RecordOrders AS RO1
                                        WHERE RO1.title = '{title_return}'
                                        """
                )
                hIDOwnsRecordReturn = dictfetchall(cursor)

                if not hIDReturn:
                    return render(request, 'Records_management.html', {'error_return': 'Family hID was not found', 'table': table})

                if not titleReturn:
                    return render(request, 'Records_management.html', {'error_return': 'Movie title was not found', 'table': table})

                if hIDOwnsRecordReturn != hIDReturn:
                    return render(request, 'Records_management.html', {'error_return': 'You can not return a movie another family owns!', 'table': table})

                # delete the record from RecordOrders
                cursor.execute(
                    f"""
                    DELETE FROM RecordOrders WHERE hID = {hID_return} and title = '{title_return}';
                    """
                )

                # add the record to RecordReturns
                cursor.execute(
                    f"""
                        INSERT INTO RecordReturns (hID, title) VALUES ({hID_return}, '{title_return}');
                    """
                )

                cursor.execute(
                    f"""
                                 SELECT Top 3 hID, COUNT(title) AS count
                                 FROM
                                 (
                                     SELECT hID, title FROM RecordOrders
                                     UNION
                                     SELECT hID, title FROM RecordReturns
                                 ) AS combined
                                 GROUP BY hID
                                 ORDER BY count DESC
                             """
                )
                table = dictfetchall(cursor)

                return render(request, 'Records_management.html', {'success_return': 'Order successfully returned!', 'table': table})


def Rankings(request):
    if not request.POST:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT genre
                FROM Programs AS P1
                GROUP BY genre
                HAVING COUNT(P1.title) >= 5
                """
            )
            genre = dictfetchall(cursor)
            flag = True
            cursor.execute(
                """
                    SELECT H1.hID
                    FROM Households AS H1
                """
            )
            allhID = dictfetchall(cursor)

            cursor.execute(
                """
                    SELECT P1.title
                    FROM Programs AS P1
                """
            )
            allTitle = dictfetchall(cursor)

            return render(request, 'Rankings.html', {'genre': genre, 'flag': flag, 'allhID':allhID, 'allTitle': allTitle})

    else:
        with connection.cursor() as cursor:
            if request.POST and request.POST.get('hID_selected') \
                    and request.POST.get('title_selected') \
                    and request.POST.get('rank_selected') :
                title_selected = request.POST.get('title_selected')
                hID_selected = request.POST.get('hID_selected')
                rank_selected = request.POST.get('rank_selected')

                cursor.execute(
                    f"""
                        SELECT PR1.rank
                        FROM ProgramRanks AS PR1
                        WHERE PR1.hID = {hID_selected} and PR1.title = '{title_selected}'
                    """
                )
                hIDOrder = dictfetchall(cursor)

                if not hIDOrder:
                    cursor.execute(
                        f"""
                            INSERT INTO ProgramRanks (title, hID, rank) VALUES ('{title_selected}', {hID_selected}, {rank_selected});
                        """
                    )
                else:
                    cursor.execute(
                        f"""
                        UPDATE ProgramRanks
                        SET rank = {rank_selected}
                        WHERE hID = {hID_selected} AND title = '{title_selected}';
                        """
                    )
                flag = True
                cursor.execute(
                    """
                        SELECT H1.hID
                        FROM Households AS H1
                    """
                )
                allhID = dictfetchall(cursor)

                cursor.execute(
                    """
                        SELECT P1.title
                        FROM Programs AS P1
                    """
                )
                allTitle = dictfetchall(cursor)

                cursor.execute(
                    f"""
                    SELECT genre
                    FROM Programs AS P1
                    GROUP BY genre
                    HAVING COUNT(P1.title) >= 5
                    """
                )
                genre = dictfetchall(cursor)
                return render(request, 'Rankings.html', {'flag': flag,'allhID': allhID, 'allTitle': allTitle, 'genre': genre})


            if request.POST and request.POST.get('genre_selected') and request.POST.get('min_rank'):
                genre_selected = request.POST.get('genre_selected')
                min_rank = request.POST.get('min_rank')

                cursor.execute(
                    f"""
                    create view SpokenShows1
                    as
                    SELECT top 5 PR1.title, CAST(AVG(Cast(PR1.rank AS DECIMAL(10,2))) AS DECIMAL(10,2)) AS AverageRank
                    FROM ProgramRanks AS PR1, Programs P
                    WHERE PR1.title = P.title AND P.genre = '{genre_selected}'
                    GROUP BY PR1.title
                    HAVING COUNT(*) >= {min_rank}
                    ORDER BY AverageRank DESC, title"""
                    )

                cursor.execute(
                    f"""SELECT TOP 5 P2.title, ISNULL(SS.AverageRank, 0) AS Average
                    FROM Programs AS P2 left outer join SpokenShows1 SS on P2.title = SS.title
                    WHERE P2.genre = '{genre_selected}'
                    GROUP BY P2.title, SS.AverageRank
                    ORDER BY Average DESC, title
                    """
                )
                spoken_shows = dictfetchall(cursor)

                cursor.execute(
                    f"""
                     DROP VIEW SpokenShows1
                    """
                )

                cursor.execute(
                    f"""
                                            SELECT genre
                                            FROM Programs AS P1
                                            GROUP BY genre
                                            HAVING COUNT(P1.title) >= 5
                                            """
                )
                genre = dictfetchall(cursor)

                cursor.execute(
                    """
                        SELECT H1.hID
                        FROM Households AS H1
                    """
                )
                allhID = dictfetchall(cursor)

                cursor.execute(
                    """
                        SELECT P1.title
                        FROM Programs AS P1
                    """
                )
                allTitle = dictfetchall(cursor)
                flag = False
                return render(request, 'Rankings.html', {'spoken_shows': spoken_shows, 'genre': genre, 'flag': flag, 'allhID': allhID, 'allTitle': allTitle})




