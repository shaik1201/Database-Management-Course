from django.shortcuts import render
from django.db import connection
from . import models

# Create your views here.

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def index(request):
    return render(request, 'index.html')

def Query_results(request):
    n_movies = 10000
    if request.POST and request.POST.get('n_movies'):
        n_movies = request.POST.get('n_movies')

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT M1.movieTitle, M1.genre, MAX(M1.gross) as Max_Gross_movie
            FROM Movies AS M1
            WHERE M1.genre IS NOT NULL AND M1.gross >= All (SELECT M2.gross
                                                           FROM Movies AS M2
                                                           WHERE M1.genre = M2.genre)
            GROUP BY M1.genre, M1.movieTitle
            ORDER BY M1.genre
            """
        )
        sql_res1 = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT M1.movieTitle AS movieTitle1,M1.genre
            FROM Movies AS M1
            WHERE M1.movieTitle in (
                SELECT top 1 M2.movieTitle
                FROM Movies AS M2
                WHERE M2.genre IS NOT NULL AND LEN(M2.movieTitle) >= All (SELECT MAX(LEN(M3.movieTitle))
                                                           FROM Movies AS M3
                                                           WHERE M2.genre = M3.genre
                                                           )
                AND M2.genre = M1.genre
                )
            GROUP BY  M1.genre, M1.movieTitle
            ORDER BY M1.genre
            """
        )
        sql_res2 = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT M2.genre, COUNT( DISTINCT YEAR(M2.releaseDate)) AS relevant_years
            FROM Movies as M2
            WHERE M2.genre IS NOT NULL AND YEAR(M2.releaseDate) in (SELECT YEAR(M1.releaseDate)
                                                FROM Movies as M1
                                                WHERE M1.genre = M2.genre
                                                GROUP BY genre, YEAR(releaseDate)
                                                HAVING COUNT(M1.releaseDate) > 1)
            GROUP BY M2.genre
            ORDER BY M2.genre
            """
        )
        sql_res3 = dictfetchall(cursor)

        for dict_sql_res2 in sql_res2:
            genre_sql_res2 = dict_sql_res2['genre']
            for dict_sql_res1 in sql_res1:
                genre_sql_res1 = dict_sql_res1['genre']
                if genre_sql_res1 == genre_sql_res2:
                    dict_sql_res1['greatest_length_movie'] = dict_sql_res2['movieTitle1']

        for dict_sql_res3 in sql_res3:
            genre_sql_res3 = dict_sql_res3['genre']
            for dict_sql_res1 in sql_res1:
                genre_sql_res1 = dict_sql_res1['genre']
                if genre_sql_res1 == genre_sql_res3:
                    dict_sql_res1['relevant_years'] = dict_sql_res3['relevant_years']



        cursor.execute(
            f"""
            SELECT DISTINCT AIM1.movie as movie4, AIM1.actor as actor4
            FROM ActorsInMovies AS AIM1, Movies AS M1
            WHERE AIM1.actor IN (SELECT AIM2.actor
                                    FROM ActorsInMovies AS AIM2
                                    GROUP BY AIM2.actor
                                    HAVING COUNT(DISTINCT AIM2.movie) > {n_movies})
            AND M1.movieTitle = AIM1.movie AND M1.releaseDate = (SELECT MIN(M4.releaseDate)
                                                                 FROM ActorsInMovies AS AIM4, Movies AS M4
                                                                 WHERE M4.movieTitle = AIM4.movie AND AIM4.actor = AIM1.actor)
            GROUP BY AIM1.movie, AIM1.actor, M1.releaseDate
            """
        )
        sql_res4 = dictfetchall(cursor)

        cursor.execute(
            f"""
                    SELECT TOP 5 AIM0.movie movie5, COUNT(DISTINCT AIM0.actor) AS Number_Of_Children_Only_Actors
                    FROM ActorsInMovies AIM0
                    WHERE AIM0.actor IN (
                        SELECT AIM.actor
                        FROM ActorsInMovies AIM
                        WHERE AIM.actor in (
                            SELECT AIM1.actor
                            FROM ActorsInMovies AIM1, Movies M1
                            WHERE AIM1.movie = M1.movieTitle AND M1.rating != 'R'
                            )
                        AND AIM.actor in (
                            SELECT AIM2.actor
                            FROM ActorsInMovies AIM2 INNER JOIN Movies M2 on M2.movieTitle = AIM2.movie
                            WHERE M2.rating = 'G'
                            GROUP BY AIM2.actor
                            HAVING count(DISTINCT AIM2.movie) >= 4
                            )
                        )
                    GROUP BY AIM0.movie
                    ORDER BY Number_Of_Children_Only_Actors DESC, AIM0.movie
                    """
        )
        sql_res5 = dictfetchall(cursor)



    return render(request, 'Query_results.html', {'sql_res1': sql_res1, 'sql_res4': sql_res4, 'sql_res5': sql_res5})

def add_movie(request):
    if request.method == 'POST' and request.POST:
        movie_title = request.POST['movie_title']
        release_date = request.POST['release_date']
        genre = request.POST['genre']
        rating = request.POST['rating']
        gross = request.POST['gross']
        new_content = models.Movies(movietitle=movie_title,
                             releasedate=release_date,
                             genre=genre,
                             rating=rating,
                             gross=gross)
        new_content.save()
    return render(request, 'add_movie.html')