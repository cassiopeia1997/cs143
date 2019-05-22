#!/usr/bin/python3

import psycopg2
import re
import string
import sys

_PUNCTUATION = frozenset(string.punctuation)

def _remove_punc(token):
    """Removes punctuation from start/end of token."""
    i = 0
    j = len(token) - 1
    idone = False
    jdone = False
    while i <= j and not (idone and jdone):
        if token[i] in _PUNCTUATION and not idone:
            i += 1
        else:
            idone = True
        if token[j] in _PUNCTUATION and not jdone:
            j -= 1
        else:
            jdone = True
    return "" if i > j else token[i:(j+1)]

def _get_tokens(query):
    rewritten_query = []
    tokens = re.split('[ \n\r]+', query)
    for token in tokens:
        cleaned_token = _remove_punc(token)
        if cleaned_token:
            if "'" in cleaned_token:
                cleaned_token = cleaned_token.replace("'", "''")
            rewritten_query.append(cleaned_token)
    return rewritten_query



def search(query, query_type,page_num,page_button):

    
    rewritten_query = _get_tokens(query)
    t=tuple(rewritten_query)

    """TODO
    Your code will go here. Refer to the specification for projects 1A and 1B.
    But your code should do the following:
    1. Connect to the Postgres database.
    2. Graciously handle any errors that may occur (look into try/except/finally).
    3. Close any database connections when you're done.
    4. Write queries so that they are not vulnerable to SQL injections.
    5. The parameters passed to the search function may need to be changed for 1B. 
    """
    #print(rewritten_query)
    
    connection=None
    rows=[]
    page_num = int(page_num)
    try:
        connection =psycopg2.connect(
                                     user="cs143",
                                     password="cs143",
                                     host="localhost",
                                     database="cs143")
        cursor=connection.cursor()
        
        connection_data =psycopg2.connect(
                                     user="cs143",
                                     password="cs143",
                                     host="localhost",
                                     database="cs143")
        cursor_data = connection_data.cursor()
        if (page_button =='init'):

            if(query_type=="and"):
            
                db_query="""
                    
                    DROP MATERIALIZED VIEW IF EXISTS page;
                    CREATE MATERIALIZED VIEW page AS
                    SELECT C.song_name AS song_name,artist.artist_name AS artist_name , C.page_link AS page_link, C.total AS total
                    FROM
                    artist
                    INNER JOIN
                    (SELECT song.artist_id AS artist_id, song.song_name AS song_name, song.page_link AS page_link,B.total AS total
                    FROM song
                    INNER JOIN
                    (SELECT tfidf.song_id AS song_id, SUM(tfidf.score) AS total
                    FROM tfidf
                    INNER JOIN (
                    SELECT song_id
                    FROM token
                    WHERE token IN %s
                    GROUP BY song_id
                    HAVING COUNT(token)=%s) A
                    ON tfidf.song_id=A.song_id
                    WHERE tfidf.token IN %s
                    GROUP BY tfidf.song_id) B
                    ON song.song_id=B.song_id) C
                    ON artist.artist_id=C.artist_id
                    ORDER BY total DESC;
                """

                #print(db_query)
                cursor.execute(db_query,((t,len(rewritten_query),t)))
                connection.commit()
                
            if(query_type=="or"):
            
                db_query="""

                    DROP MATERIALIZED VIEW IF EXISTS page;
                    CREATE MATERIALIZED VIEW page AS
                    SELECT C.song_name AS song_name,artist.artist_name AS artist_name , C.page_link AS page_link, C.total AS total
                    FROM
                    artist
                    INNER JOIN
                    (SELECT song.artist_id AS artist_id, song.song_name AS song_name, song.page_link AS page_link,B.total AS total
                    FROM song
                    INNER JOIN
                    (SELECT tfidf.song_id AS song_id, MAX(tfidf.score) AS total
                    FROM tfidf
                    INNER JOIN (
                    SELECT song_id
                    FROM token
                    WHERE token IN %s
                    GROUP BY song_id) A
                    ON tfidf.song_id=A.song_id
                    WHERE tfidf.token IN %s
                    GROUP BY tfidf.song_id) B
                    ON song.song_id=B.song_id) C
                    ON artist.artist_id=C.artist_id
                    ORDER BY total DESC;
                    """
                
                #print(db_query)
                cursor.execute(db_query,(t,t))
                connection.commit()

        data_query = """

            SELECT * FROM page LIMIT 20 OFFSET %s;
            """
        cursor_data.execute(data_query,(20*(page_num-1),))
        rows=cursor_data.fetchall()
        print(rows)


    except(Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL",error)
    finally:
        if connection is not None:
            cursor.close()
            cursor_data.close()
            connection.close()
            connection_data.close()

        #print("connection is closed")
    
#print(rows)
    return rows

if __name__ == "__main__":
    if len(sys.argv) > 2:
        result = search(' '.join(sys.argv[2:]), sys.argv[1].lower())
    else:
        print("USAGE: python3 search.py [or|and] term1 term2 ...")

