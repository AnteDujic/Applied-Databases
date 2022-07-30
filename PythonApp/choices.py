import pymysql
from neo4j import GraphDatabase

conn = pymysql.connect(host="localhost", 
                        user="root", password="root", 
                        db="employees", 
                        cursorclass=pymysql.cursors.DictCursor)

uri = "neo4j://localhost:7687"

# Option One
def one(offset):
    query = """ SELECT e.name, d.name FROM employee e 
            INNER JOIN dept d ON e.did = d.did 
            ORDER BY e.name LIMIT 2 OFFSET %s """

    cursor = conn.cursor()
    cursor.execute(query, (offset))
    x = cursor.fetchall()
    return (x)
    conn.close()

# Option Two
def two(eid):
    query = """ SELECT s.eid, e.name, ROUND(MIN(s.salary),2) AS Minimum, 
            ROUND(AVG(s.salary),2) AS Avarage, 
            ROUND(MAX(s.salary),2) AS Maximum FROM employee e
            LEFT JOIN salary s ON e.eid = s.eid WHERE s.eid = %s """
    cursor = conn.cursor()
    cursor.execute(query, (eid))
    x = cursor.fetchall()
    return (x)
    conn.close()

# Option Three
def three(month):
    query = """ SELECT eid, name, dob
                from employee
                WHERE LEFT(MONTHNAME(DOB),3) = %s
                OR MONTH(DOB) = %s """

    cursor = conn.cursor()
    cursor.execute(query, (month, month))
    x = cursor.fetchall()
    return (x)
    conn.close()

# Option Four
def four(eid, name, dob, did):
    query = """ INSERT INTO employee (eid, name, dob, did) 
                VALUES (%s, %s, %s, %s) """

    cursor = conn.cursor()
    cursor.execute(query, (eid, name, dob, did))
    print("Employee succesfuly added")
    
    conn.commit()
    conn.close()

# Option Five
def get_department(tx, empID):
    query = """match(e:Employee{eid:$employeeId})-[:MANAGES]->(d:Department)
            return d.did"""
    names = []
    results = tx.run(query, employeeId = empID)
    for result in results:
        names.append(result["d.did"])
    return names

def five():
    driver = GraphDatabase.driver(uri, auth=("neo4j","neo4j"), max_connection_lifetime=1000)
    empID = (input ("Enter EID: ")).upper()
    with driver.session() as session:
        values = session.read_transaction(get_department, empID)
        return values
        
def fiveSQL(n):
    query = """ SELECT did, budget
                FROM dept
                WHERE did = %s """

    cursor = conn.cursor()
    cursor.execute(query, (n))
    x = cursor.fetchall()
    return (x)
    conn.close()

# Option Six
def sqlEID(n):
    query = """ SELECT * FROM EMPLOYEE
                WHERE eid = %s """

    cursor = conn.cursor()
    cursor.execute(query, (n))
    x = cursor.fetchall()
    return (x)
    conn.close()

def sqlDID(n):
    query = """ SELECT * FROM DEPT
                WHERE did = %s """

    cursor = conn.cursor()
    cursor.execute(query, (n))
    x = cursor.fetchall()
    return (x)
    conn.close()

def constraints(tx):
    query = """CREATE CONSTRAINT uniqueDID 
                IF NOT EXISTS FOR (d:Department) 
                REQUIRE d.did IS UNIQUE"""
    tx.run(query)

def NeoConst():
    driver = GraphDatabase.driver(uri, auth=("neo4j","neo4j"), max_connection_lifetime=1000)
    with driver.session() as session:
        constr = session.write_transaction(constraints)

def manage(tx, emID, depID):
    query = """MERGE (e:Employee{eid:$eid})
            CREATE (d:Department{did:$did})
            MERGE (e)-[m:MANAGES]->(d)"""
    tx.run(query, eid = emID, did = depID )

def six(eidNeo,didNeo):
    driver = GraphDatabase.driver(uri, auth=("neo4j","neo4j"), max_connection_lifetime=1000)
    with driver.session() as session:
        constr = session.write_transaction(manage, eidNeo, didNeo)

def alreadyManaged(tx, deID):
    query = """ MATCH (e:Employee)-[]-(d:Department{did:$did})
                RETURN e.eid"""
    
    employee = tx.run(query, did = deID)
    for result in employee:
        emp = (result["e.eid"])
    return emp

def exception(did):
    driver = GraphDatabase.driver(uri, auth=("neo4j","neo4j"), max_connection_lifetime=1000)
    with driver.session() as session:
        values = session.read_transaction(alreadyManaged, did)
        return values

# Option Seven
def seven():
    query = """ SELECT * FROM dept"""

    cursor = conn.cursor()
    cursor.execute(query)
    x = cursor.fetchall()
    return (x)
    conn.close()
