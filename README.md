# APPLIED DATABASES | 2022
### AUTHOR: ANTE DUJIC
<hr style="border:2px solid gray"> </hr>

This repository is created as a project for Applied Databases module on ATU, Ireland. There are three main folders in this repository:
1. MYSQL-Queries
2. Neo4j-Queries
3. PythonApp

    
### :file_folder: 1. MYSQL-Queries
<hr style="border:2px solid gray"> </hr>

This folder contains SQL Queries written to solve the problems given in *Questions.pdf*. Two examples are given below:

1. Show the Name and LifeExpectancy of all countries in “North America” where the country’s LifeExpectancy is the maximum LifeExpectancy for countries in “North America”.

```sql
SELECT Name, LifeExpectancy 
FROM country 
WHERE continent = "North America" 
AND LifeExpectancy = (
	SELECT MAX(LifeExpectancy)
	FROM country 
	WHERE continent = "North America") 
ORDER BY Name;
```


2. Show Name, Population and PersonName of all cities visited by people, where the city population is greater than the maximum population of “Polynesia”.

```sql
SELECT c.name, c.population, p.personname
FROM hasvisitedcity h
LEFT JOIN city c
ON h.cityid = c.id
LEFT JOIN person p
ON h.personid = p.personid
WHERE c.population > (
	SELECT MAX(population) 
	FROM country
	WHERE region = "Polynesia")
ORDER BY c.name;
```

### :file_folder: 2. Neo4j-Queries
<hr style="border:2px solid gray"> </hr>

This folder contains Neo4j Queries written to solve the problems given in *Questions.pdf*. Two examples are given below:

1. Return the names of instruments (as Instruments) people play, and the names of people (as Person) who play those instruments, only for people who play Midfield position in either Football or Soccer.
Results should be in alphabetical instrument name, and within that alphabetically by person name.

```sql
MATCH (s:Sport)<-[:PLAYS{position:"Midfield"}]-(p:Person)-[:PLAYS]->(i:Instrument)
WHERE s.name="Soccer" or s.name="Football"
RETURN i.name as Instruments, p.name as Person
ORDER BY Instruments, Person
```

2. Return the list of salaries of people who are less than 50,000 (as Salaries_LT_50k). The salaries should be rounded up or down to the nearest whole number. 

```sql
MATCH (p:Person)
WHERE p.salary < 50000
RETURN COLLECT(toInteger(ROUND(p.salary))) as Salaries_LT_50k
```

### :file_folder: 3. PythonApp
<hr style="border:2px solid gray"> </hr>

This folder contains an application written in Python that manipulates SQL and Neo4j databases. The application functionality is created based on the instructions from *Final Project Specification 2022.pdf*. Some examples are given below.

Python application displays a main menu as follows:

```console
Employees
---------

MENU
====
1 - View Employees & Departments
2 - View Salary Details
3 - View by Month of Birth
4 - Add New Employee
5 - View Departments managed by Employee
6 - Add Manager to Department
7 - View Departments
x - Exit application
Choice:   
```

1. Choice 1

The user is shown the list of Employee Names (in alphabetical order) and the Names of the Department each employee works in, in groups of 2. If the user presses any key except q the next 2 Employees and their Department are shown. And so on until the user presses q. Whenever the user presses q he/she is returned to the Main Menu.

2. Choice 6

The user is asked to enter an Employee ID and a Department ID.
When both are entered, the Neo4j database is updated to show that that employee now manages that department. If an Employee ID and/or Department ID is entered that does not exist in the MySQL database (employees), then an error message(s) is printed, and the user is prompted to enter a new Employee ID and Department ID. If a Department ID is entered that is already managed by another Employee, an error message should be shown. It is possible for an Employee to manage many Departments.

Menu functionalites are contained within *pythonApp.py* and all the SQL and Neo4j queries are contained withing the *choices.py* file. 