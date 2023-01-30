# APPLIED DATABASES | 2022
### AUTHOR: ANTE DUJIC
<hr style="border:2px solid gray"> </hr>

This repository is created as a project for Applied Databases module on ATU, Ireland. There are three main folders in this repository:
1. MYSQL-Queries
2. Neo4j-Queries
3. PythonApp

    
### :file_folder: 1. MYSQL-Queries
<hr style="border:2px solid gray"> </hr>

This folder contains SQL Queries written to solve the problems given in *Final Project Specification 2022.pdf". Two examples are given below:

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

### :file_folder: 2. Neo4j-Queries
<hr style="border:2px solid gray"> </hr>


### :file_folder: 3. PythonApp
<hr style="border:2px solid gray"> </hr>
