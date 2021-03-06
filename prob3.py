import psycopg2

def proba(cur):
    print("\nResults for 3a")
    cur.execute("select count(SID) from student;")
    total_students = cur.fetchone()[0]
    for i in range(20):
        unit_compare = str(i+1)
        cur.execute("""
            SELECT unitSum, COUNT(distinct SID) countSID FROM (
                SELECT (SUM(units)) unitSum, SID, Term
                FROM enrollment NATURAL JOIN Course
                WHERE Subject IN ('ABC','DEF')
                GROUP BY (Term, SID)
                HAVING SUM(units) = %s
            ) StudentUnitSum
            GROUP BY unitSum
            ;""" %unit_compare)
        unit, count = cur.fetchone()
        print(unit_compare + ": " + str(round(count * 100 / total_students, 4)) + "%")

        
def probb(cur):
    print("\nResults for 3b")
    min_query = """
    SELECT Instructor, avgGrade
    FROM (SELECT Instructor, AVG(Number) avgGrade
        FROM Meeting NATURAL JOIN (Enrollment INNER JOIN NumGrade on Enrollment.grade = NumGrade.letter)
        GROUP BY Instructor) GradeInstr
    WHERE avgGrade = (SELECT MIN(avgGrade) FROM 
        (SELECT Instructor, AVG(Number) avgGrade
        FROM Meeting NATURAL JOIN (Enrollment INNER JOIN NumGrade on Enrollment.grade = NumGrade.letter)
        GROUP BY Instructor) g2)
    ;
    """
    
    cur.execute(min_query)
    x = cur.fetchall()
    print("Hardest professor: ")
    for entry in x:
        print(entry)
    
    max_query = """
    SELECT Instructor, avgGrade
    FROM 
        (SELECT AVG(Number) avgGrade, Instructor
        FROM Meeting NATURAL JOIN (Enrollment INNER JOIN NumGrade on Enrollment.grade = NumGrade.letter)
        GROUP BY Instructor) GradeInstr
    WHERE avgGrade = (SELECT MAX(avgGrade) FROM 
        (SELECT Instructor, AVG(Number) avgGrade
        FROM Meeting NATURAL JOIN (Enrollment INNER JOIN NumGrade on Enrollment.grade = NumGrade.letter)
        GROUP BY Instructor) g2)
    ;
    """    
    
    cur.execute(max_query)
    y = cur.fetchall()
    print("\nEasiest professor: ")
    for entry in y:
        print(entry)
    
def probc(cur):
    print
    print("Results for 3c")
    for i in range(20):
        q = """
        SELECT sumUnits, (SUM(GPA * sumUnits) / SUM(sumUnits)) weighedGPA
        FROM
            (SELECT SID, TERM, SUM(UNITS) sumUnits, GPA
            FROM ENROLLMENT NATURAL LEFT JOIN NUMGRADE
            GROUP BY SID, TERM, GPA) StudentGPA
        WHERE sumUnits > 0
        GROUP BY sumUnits
        HAVING sumUnits = %s
        ;
        """ %(str(i+1))
                                              
        cur.execute(q)
        _, x = cur.fetchone()
        print(str(i+1) + ": " + str(round(x, 2)))

            
def probd(cur):
    print
    print("Results for 3d")
    query1 ="""
    SELECT PassRate, Subject, CRSE FROM (
        SELECT ((PassS * 100.0)/ totalS) AS PassRate, Subject, CRSE FROM (
            (
            SELECT COUNT(SID) totalS, Subject, CRSE
            FROM Enrollment NATURAL JOIN Course
            WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P', 'S',       'F', 'U', 'NS', 'NP')
            GROUP BY (Subject, CRSE)
            ) Total
        NATURAL JOIN
            (
            SELECT COUNT(SID) PassS, Subject, CRSE
            FROM Enrollment NATURAL JOIN Course
            WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P')
            GROUP BY (Subject, CRSE)
            ) Pass
        ) Rate
        ORDER BY PassRate DESC
    ) N
    WHERE PassRate = (SELECT MIN(PassRate) FROM
    (
        SELECT ((PassS * 100.0)/ totalS) AS PassRate, Subject, CRSE FROM (
            (
            SELECT COUNT(SID) totalS, Subject, CRSE
            FROM Enrollment NATURAL JOIN Course
            WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P', 'S',       'F', 'U', 'NS', 'NP')
            GROUP BY (Subject, CRSE)
            ) Total
        NATURAL JOIN
            (
            SELECT COUNT(SID) PassS, Subject, CRSE
            FROM Enrollment NATURAL JOIN Course
            WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P')
            GROUP BY (Subject, CRSE)
            ) Pass
        ) Rate
    ) X
    )
    ;
    """
    query2 = """
    SELECT PassRate, Subject, CRSE FROM (
        SELECT ((PassS * 100.0)/ totalS) AS PassRate, Subject, CRSE FROM (
            (
            SELECT COUNT(SID) totalS, Subject, CRSE
            FROM Enrollment NATURAL JOIN Course
            WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P', 'S',       'F', 'U', 'NS', 'NP')
            GROUP BY (Subject, CRSE)
            ) Total
        NATURAL JOIN
            (
            SELECT COUNT(SID) PassS, Subject, CRSE
            FROM Enrollment NATURAL JOIN Course
            WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P', 'S')
            GROUP BY (Subject, CRSE)
            ) Pass
        ) Rate
        ORDER BY PassRate DESC
    ) N
    WHERE PassRate = (SELECT MAX(PassRate) FROM
    (
        SELECT ((PassS * 100.0)/ totalS) AS PassRate, Subject, CRSE FROM (
            (
            SELECT COUNT(SID) totalS, Subject, CRSE
            FROM Enrollment NATURAL JOIN Course
            WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P', 'S',       'F', 'U', 'NS', 'NP')
            GROUP BY (Subject, CRSE)
            ) Total
        NATURAL JOIN
            (
            SELECT COUNT(SID) PassS, Subject, CRSE
            FROM Enrollment NATURAL JOIN Course
            WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P', 'S')
            GROUP BY (Subject, CRSE)
            ) Pass
        ) Rate
    ) X
    )
    ;
    """    
    cur.execute(query1)
    
    y = cur.fetchall()
    
    for row in y:
        (rate, subject, num) = row
        print(str(subject) + str(num) + ": " + str(round(rate, 2)) + "%")
    print("\nHighest Pass Rate: ")
    cur.execute(query2)
    z = cur.fetchall()
    for row in z:
        (_, subject, num) = row
        print(str(subject) + str(num) + ": " + str(round(rate, 2)) + "%") 
    print("\n")
        #print(str(subject) + str(num) + ": " + str(round(rate, 2)) + "%") 

        
def probe(cur):
    print
    print("Results for 3e")
    q = """
    SELECT DISTINCT(Meet1.Subject, Meet1.CRSE), 
        Meet2.Subject, Meet2.CRSE
    FROM (Meeting NATURAL JOIN Course) Meet1, 
        (Meeting NATURAL JOIN Course) Meet2
    WHERE Meet1.Term::text NOT LIKE '%03'
        AND Meet2.Term::text NOT LIKE '%03' 
        AND Meet1.Time NOT LIKE '%NA%' AND Meet2.Time NOT LIKE '%NA%'
        AND Meet1.Days NOT LIKE '%NA%' AND Meet2.Days NOT LIKE '%NA%'
        AND Meet1.Building NOT LIKE '%NA%' AND Meet2.Building NOT LIKE '%NA%'
        AND Meet1.Room NOT LIKE '%NA%' AND Meet2.Room NOT LIKE '%NA%'
        AND Meet1.CRSE < Meet2.CRSE
        AND Meet1.Time = Meet2.Time
        AND Meet1.Term = Meet2.Term
        AND Meet1.Days = Meet2.Days
        AND Meet1.Room = Meet2.Room 
        AND Meet1.Building = Meet2.Building
        AND Meet1.Instructor = Meet2.Instructor
    ORDER BY (Meet1.Subject, Meet1.CRSE)
    ;
    """
                                              
    cur.execute(q)
    x = cur.fetchall()
    for i in x:
        print(i)

def probf(cur):	
    print
    print("Results for 3f")
    query1 = """SELECT Major, AvgGrade FROM
    (
        SELECT Major, AVG(GPA) AvgGrade FROM
        (
            SELECT Major, Subject, CRSE, Grade, GPA
            FROM NumGrade NATURAL JOIN
            (
                SELECT Major, Subject, CRSE, Grade
                FROM Enrollment NATURAL JOIN Course
                WHERE Subject = 'ABC'
            ) EnCr
            WHERE Letter = Grade
        ) EnCrGr
        GROUP BY Major
        ORDER BY AvgGrade
    ) EnCrGrSelect
    WHERE AvgGrade = (SELECT MAX(AvgGrade) FROM	
    (
        SELECT Major, AVG(GPA) AvgGrade FROM
        (
            SELECT Major, Subject, CRSE, Grade, GPA
            FROM NumGrade NATURAL JOIN
            (
                SELECT Major, Subject, CRSE, Grade
                FROM Enrollment NATURAL JOIN Course
                WHERE Subject = 'ABC'
            ) EnCr
            WHERE Letter = Grade
        ) EnCrGr
        GROUP BY Major
        ORDER BY AvgGrade
    ) EnCrGrSelect
    )
    ;
    """
    query2 = """SELECT Major, AvgGrade FROM
    (
        SELECT Major, AVG(GPA) AvgGrade FROM
        (
            SELECT Major, Subject, CRSE, Grade, GPA
            FROM NumGrade NATURAL JOIN
            (
                SELECT Major, Subject, CRSE, Grade
                FROM Enrollment NATURAL JOIN Course
                WHERE Subject = 'ABC'
            ) EnCr
            WHERE Letter = Grade
        ) EnCrGr
        GROUP BY Major
        ORDER BY AvgGrade
    ) EnCrGrSelect
    WHERE AvgGrade = (SELECT MIN(AvgGrade) FROM
    (
        SELECT Major, AVG(GPA) AvgGrade FROM
        (
            SELECT Major, Subject, CRSE, Grade, GPA
            FROM NumGrade NATURAL JOIN
            (
                SELECT Major, Subject, CRSE, Grade
                FROM Enrollment NATURAL JOIN Course
                WHERE Subject = 'ABC'
            ) EnCr
            WHERE Letter = Grade
        ) EnCrGr
        GROUP BY Major
        ORDER BY AvgGrade
    ) EnCrGrSelect
    )
    ;
    """
    query3 = """SELECT Major, AvgGrade FROM
    (
        SELECT Major, AVG(GPA) AvgGrade FROM
        (
            SELECT Major, Subject, CRSE, Grade, GPA
            FROM NumGrade NATURAL JOIN
            (
                SELECT Major, Subject, CRSE, Grade
                FROM Enrollment NATURAL JOIN Course
                WHERE Subject = 'DEF'
            ) EnCr
            WHERE Letter = Grade
        ) EnCrGr
        GROUP BY Major
        ORDER BY AvgGrade
    ) EnCrGrSelect
    WHERE AvgGrade = (SELECT MAX(AvgGrade) FROM
    (
        SELECT Major, AVG(GPA) AvgGrade FROM
        (
            SELECT Major, Subject, CRSE, Grade, GPA
            FROM NumGrade NATURAL JOIN
            (
                SELECT Major, Subject, CRSE, Grade
                FROM Enrollment NATURAL JOIN Course
                WHERE Subject = 'DEF'
            ) EnCr
            WHERE Letter = Grade
        ) EnCrGr
        GROUP BY Major
        ORDER BY AvgGrade
    ) EnCrGrSelect
    )
    ;
    """
    query4 = """SELECT Major, AvgGrade FROM
    (
        SELECT Major, AVG(GPA) AvgGrade FROM
        (
            SELECT Major, Subject, CRSE, Grade, GPA
            FROM NumGrade NATURAL JOIN
            (
                SELECT Major, Subject, CRSE, Grade
                FROM Enrollment NATURAL JOIN Course
                WHERE Subject = 'DEF'
            ) EnCr
            WHERE Letter = Grade
        ) EnCrGr
        GROUP BY Major
        ORDER BY AvgGrade
    ) EnCrGrSelect
    WHERE AvgGrade = (SELECT MIN(AvgGrade) FROM	
    (
        SELECT Major, AVG(GPA) AvgGrade FROM
        (
            SELECT Major, Subject, CRSE, Grade, GPA
            FROM NumGrade NATURAL JOIN
            (
                SELECT Major, Subject, CRSE, Grade
                FROM Enrollment NATURAL JOIN Course
                WHERE Subject = 'DEF'
            ) EnCr
            WHERE Letter = Grade
        ) EnCrGr
        GROUP BY Major
        ORDER BY AvgGrade
    ) EnCrGrSelect
    )
    ;
    """
    print("Best Majors in ABC Courses")
    cur.execute(query1)
    y = cur.fetchall()
    for row in y:
        major, grade = row
        print("Major: " + str(major) + "\tGrade: " + str(grade))
        
    print("Worst Majors in ABC Courses")
    cur.execute(query2)
    y = cur.fetchall()
    for row in y:
        major, grade = row
        print("Major: " + str(major) + "\tGrade: " + str(grade))
        
    print("Best Majors in DEF Courses")
    cur.execute(query3)
    y = cur.fetchall()
    for row in y:
        major, grade = row
        print("Major: " + str(major) + "\tGrade: " + str(grade))
    print("Worst Majors in DEF Courses")
    cur.execute(query4)
    y = cur.fetchall()
    for row in y:
        major, grade = row
        print("Major: " + str(major) + "\tGrade: " + str(grade))
		
def probg(cur):
    print("\nResults for 3g")   
    query1= """ SELECT COUNT(OldMajor) AS CtMajor, OldMajor FROM
    (
        SELECT N.SID, N.Term, N.Major AS OldMajor, M.Term, M.Major AS NewMajor FROM 
            (
                (SELECT RN, SID, Major, Term FROM Enrollment GROUP BY (RN, SID, Term, Major)) N
                CROSS JOIN
                (SELECT RN, SID, Major, Term FROM Enrollment GROUP BY (RN, SID, Term, Major)) M
            )
        WHERE (N.RN < M.RN AND N.SID = M.SID AND N.Term = M.Term AND N.Major != M.Major)
        OR (N.SID = M.SID AND N.Term < M.Term AND (M.Term - N.Term) <= 4 AND N.Major != M.Major)
    ) F
    WHERE NewMajor LIKE ('ABC%') AND OldMajor NOT LIKE ('ABC%')
    GROUP BY (OldMajor)
    ORDER BY CtMajor DESC
    LIMIT 5;
    """
    query2= """ SELECT OldMajor, (CtMajor * 100.0 /
        ( SELECT COUNT(SID) FROM
        (SELECT N.SID AS SID, N.Term, N.Major AS OldMajor, M.Term, M.Major AS NewMajor FROM 
                (
                    (SELECT RN, SID, Major, Term FROM Enrollment GROUP BY (RN, SID, Term, Major)) N
                    CROSS JOIN
                    (SELECT RN, SID, Major, Term FROM Enrollment GROUP BY (RN, SID, Term, Major)) M
                )
            WHERE (N.RN < M.RN AND N.SID = M.SID AND N.Term = M.Term AND N.Major != M.Major)
            OR (N.SID = M.SID AND N.Term < M.Term AND (M.Term - N.Term) <= 4 AND N.Major != M.Major)
        )X
        WHERE NewMajor LIKE ('ABC%') AND OldMajor NOT LIKE ('ABC%')
        )       
    ) AS Percentage FROM
    (SELECT COUNT(OldMajor) AS CtMajor, OldMajor FROM
    (
        SELECT N.SID, N.Term, N.Major AS OldMajor, M.Term, M.Major AS NewMajor FROM 
            (
                (SELECT RN, SID, Major, Term FROM Enrollment GROUP BY (RN, SID, Term, Major)) N
                CROSS JOIN
                (SELECT RN, SID, Major, Term FROM Enrollment GROUP BY (RN, SID, Term, Major)) M
            )
        WHERE (N.RN < M.RN AND N.SID = M.SID AND N.Term = M.Term AND N.Major != M.Major)
        OR (N.SID = M.SID AND N.Term < M.Term AND (M.Term - N.Term) <= 4 AND N.Major != M.Major)
    ) F
    WHERE NewMajor LIKE ('ABC%') AND OldMajor NOT LIKE ('ABC%')
    GROUP BY (OldMajor)
    ORDER BY CtMajor DESC
    LIMIT 5
    ) FX
    ;
    """
    
    print("The top 5 majors to transfer into ABC")
    cur.execute(query1)
    y = cur.fetchall()
    for row in y:
        ctmajor, oldmajor = row
        print("Major: " + str(oldmajor) + "\tNumber: " + str(ctmajor))
    print("The top 5 majors to transfer into ABC by percentage")
    cur.execute(query2)
    y = cur.fetchall()
    for row in y:
        oldmajor, percentage = row
        print("Major: " + str(oldmajor) + "\tPercentage: " + str(percentage)[:6] + "%")
        
def probh(cur):
    print("\nResults for 3h")   
    query1= """ SELECT COUNT(NewMajor) AS CtMajor, NewMajor FROM
    (
        SELECT N.SID, N.Term, N.Major AS OldMajor, M.Term, M.Major AS NewMajor FROM 
            (
                (SELECT RN, SID, Major, Term FROM Enrollment GROUP BY (RN, SID, Term, Major)) N
                CROSS JOIN
                (SELECT RN, SID, Major, Term FROM Enrollment GROUP BY (RN, SID, Term, Major)) M
            )
        WHERE (N.RN < M.RN AND N.SID = M.SID AND N.Term = M.Term AND N.Major != M.Major)
        OR (N.SID = M.SID AND N.Term < M.Term AND (M.Term - N.Term) <= 4 AND N.Major != M.Major)
    ) F
    WHERE OldMajor LIKE ('ABC%') AND NewMajor NOT LIKE ('ABC%')
    GROUP BY (NewMajor)
    ORDER BY CtMajor DESC
    LIMIT 5;
    """
    query2= """ SELECT (CtMajor * 100.0 /
        ( SELECT COUNT(SID) FROM
        (SELECT N.SID AS SID, N.Term, N.Major AS OldMajor, M.Term, M.Major AS NewMajor FROM 
                (
                    (SELECT RN, SID, Major, Term FROM Enrollment GROUP BY (RN, SID, Term, Major)) N
                    CROSS JOIN
                    (SELECT RN, SID, Major, Term FROM Enrollment GROUP BY (RN, SID, Term, Major)) M
                )
            WHERE (N.RN < M.RN AND N.SID = M.SID AND N.Term = M.Term AND N.Major != M.Major)
            OR (N.SID = M.SID AND N.Term < M.Term AND (M.Term - N.Term) <= 4 AND N.Major != M.Major)
        )X
        WHERE OldMajor LIKE ('ABC%') AND NewMajor NOT LIKE ('ABC%')
        )       
    ) AS Percentage, NewMajor FROM
    (SELECT COUNT(NewMajor) AS CtMajor, NewMajor FROM
    (
        SELECT N.SID, N.Term, N.Major AS OldMajor, M.Term, M.Major AS NewMajor FROM 
            (
                (SELECT RN, SID, Major, Term FROM Enrollment GROUP BY (RN, SID, Term, Major)) N
                CROSS JOIN
                (SELECT RN, SID, Major, Term FROM Enrollment GROUP BY (RN, SID, Term, Major)) M
            )
        WHERE (N.RN < M.RN AND N.SID = M.SID AND N.Term = M.Term AND N.Major != M.Major)
        OR (N.SID = M.SID AND N.Term < M.Term AND (M.Term - N.Term) <= 4 AND N.Major != M.Major)
    ) F
    WHERE OldMajor LIKE ('ABC%') AND NewMajor NOT LIKE ('ABC%')
    GROUP BY (NewMajor)
    ORDER BY CtMajor DESC
    LIMIT 5
    ) FX
    ;
    """
    print("The top 5 majors to transfer out of ABC")
    cur.execute(query1)
    y = cur.fetchall()
    for row in y:
        ctmajor, newmajor = row
        print("Major: " + str(newmajor) + "\tNumber: " + str(ctmajor))
    print("The top 5 majors to transfer out of ABC by percentage")
    cur.execute(query2)
    y = cur.fetchall()
    for row in y:
        percentage, newmajor = row
        print("Major: " + str(newmajor) + "\tPercentage: " + str(percentage)[:6] + "%")

conn = psycopg2.connect("dbname=FakeUData")
cur = conn.cursor()

proba(cur)
probb(cur)
probc(cur)
probd(cur)
probe(cur)
probf(cur)
probg(cur)
probh(cur)

cur.close()
conn.close()

