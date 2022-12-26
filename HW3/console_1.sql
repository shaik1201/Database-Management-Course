-- a) 1 + 2
SELECT M1.movieTitle, M1.genre, MAX(M1.gross) as Max_Gosse_movie
FROM Movies AS M1
WHERE M1.genre IS NOT NULL AND M1.gross >= All (SELECT M2.gross
                                               FROM Movies AS M2
                                               WHERE M1.genre = M2.genre)
GROUP BY M1.genre, M1.movieTitle
ORDER BY M1.genre



-- a) 3
SELECT M1.movieTitle,M1.genre
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




-- a) 4
SELECT M2.genre, COUNT( DISTINCT YEAR(M2.releaseDate)) AS relevant_years
FROM Movies as M2
WHERE M2.genre IS NOT NULL AND YEAR(M2.releaseDate) in (SELECT YEAR(M1.releaseDate)
                                    FROM Movies as M1
                                    WHERE M1.genre = M2.genre
                                    GROUP BY genre, YEAR(releaseDate)
                                    HAVING COUNT(M1.releaseDate) > 1)
GROUP BY M2.genre
ORDER BY M2.genre



-- b)
SELECT DISTINCT AIM1.movie, AIM1.actor
FROM ActorsInMovies AS AIM1, Movies AS M1
WHERE AIM1.actor IN (SELECT AIM2.actor
                        FROM ActorsInMovies AS AIM2
                        GROUP BY AIM2.actor
                        HAVING COUNT(DISTINCT AIM2.movie) > 3)
AND M1.movieTitle = AIM1.movie AND M1.releaseDate = (SELECT MIN(M4.releaseDate)
                                                     FROM ActorsInMovies AS AIM4, Movies AS M4
                                                     WHERE M4.movieTitle = AIM4.movie AND AIM4.actor = AIM1.actor)
GROUP BY AIM1.movie, AIM1.actor, M1.releaseDate


-- c)

SELECT TOP 5 AIM0.movie, COUNT(DISTINCT AIM0.actor) AS Number_Of_Children_Only_Actors
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