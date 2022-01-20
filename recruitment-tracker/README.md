# **Recruitment Tracker**
This is an application built using FastAPI, Typer, SQLAlchemy's Query API, and Python to help recruiters keep a track of their applicants and the tasks assigned to said applicants. It offers a web user interface alongside a command line interface to make the task of managing applicants as easy as possible.

# **QuickStart**
To begin, you should navigate towards the recruitment-tracker directory using the following command:
```
cd [path-to-recruiting-assessment-tracker-directory]/recruitment-tracker
```
You can either create a [virtual environment](https://docs.python.org/3/library/venv.html) or you can globally install the dependencies for this application
```
pip install -r requirements.txt
```
And you're done!

# **Models**
The data is stored in a SQL database and this application stores information into 2 tables: **Applicant And AdditionalInfo**    
The ***Applicant*** table takes the following fields:  
```
1. netid -> Applicant's Unique Identifier (String, used as primary key in this table)
2. name -> Applicant's Name (String)
3. email -> Applicant's email (String
4. year -> Applicant's Educational Standing (Freshmen, Senior, etc.) (String)
5. major -> Applicant's Major (String)
6. smajor -> Applicant's Second Major (String, defaulted to an empty string)
7. teams -> The Team Being Applied To (String)
8. minor -> Applicant's Minor (String, defaulted to an empty string)
9. sminor -> Applicant's Second Minor (String, defaulted to empty string)
10. task_id -> The Assignment Assigned To This Applicant (Integer, foreign key)
11. selected -> Whether or Not the Applicant Has Been Selected (Boolean, defaulted to false)
12. comments -> Comments on The Applicant (String, defaulted to empty string)
```

The ***AdditionalInfo*** table takes the following fields:  
```
1. id -> Assignment ID (Integer, used as primary key in this table)
2. assignment_no -> Assignment Number (String)
3. team_assigned -> The Team This Assignment Corresponds To (String)
4. date_given -> The Date This Assignment Was Assigned (datetime.date Object)
5. date_due -> The Date This Assignment Is Due (datetime.date Object)
6. submitted -> Has This Task Been Turned In? (Boolean, defaulted to false)
7. assignment_comments -> Comment's on This Assignment (String, defaulted to empty string)
```

# **Usage**
You can use this application in either a web interface mode or command line mode
# Web Interface
Thanks to uvicorn, you can get a local webserver up and running using the following command:  
```
uvicorn [path-to-applicant-directory].main:app 
```
or if you've opened the `recruitment-tracker` directory in the terminal, you can just run the following command:  
```
uvicorn applicant.main:app
```
The server will start running on `http://127.0.0.1:8000`
To make it easier to access all endpoints, use the `http://127.0.0.1:8000/docs` address (FastAPI provides this documentation by default!)  
After that, you will be able to run the following endpoints: 
```
GET /applicant (returns all the applicants)

POST /applicant Create (creates an applicant)

GET /applicant/{netid} (returns applicant by netid)

PUT /applicant/{netid} (updates an applicant by their netid) (allows you to update everything about the applicant)

DELETE /applicant/{netid} (deletes an applicant by their netid)

POST /assignment (creates an assignment)

GET /assignment/{id} (get assignment by id)

PUT /assignment/{id} (updates an assignment by id) (allows you to update everything about the assignment)

GET /assignments/{no} (returns all assignments sharing the same assignment number)
```
***Make sure to first create an assignment to give to an applicant***

# Command Line Interface
Thanks to Typer, you can easily pass command line arguments. A general way to run the command is:  
```
python3 [path-to-cli.py] [OPTIONS] COMMAND [ARGS]....
```
if you've accessed the `recruitment-tracker` directory, then you can run:
```
python3 cli.py [OPTIONS] COMMAND [ARGS]....
```
###### Commands
`Usage: cli.py init [OPTIONS] FILE_ASSIGNMENT FILE_SUBMISSION`

Arguments:
  FILE_ASSIGNMENT  [required]
  FILE_SUBMISSION  [required]
  
`Example: python3 cli.py init example_assignment.csv example_submission.csv`  
Populates the tables depending on the passed csv files (Make sure to pass the assignments file first)  
***WARNING: This command overwrites the tables***  
  
`Usage: cli.py overview [OPTIONS]`

Options:
  --output-to-file / --no-output-to-file
                                  [default: no-output-to-file]

`Example: python3 cli.py overview --output-to-file` => returns applicants who have done the assignment, haven't done the assignment, are overdue on their assignment, and returns this all in an `output.txt` file if the optional parameter is passed

`Usage: cli.py search [OPTIONS] NETID`

Arguments:
  NETID  [required]
  
`Example: python3 cli.py search person0` => returns an applicant with the provided netid, if he/she exists

# Why FastAPI?
- It is a modern framework that allows developers to build API seamlessly without much effort and time. It is much faster than the traditional flask approach because it’s built over ASGI (Asynchronous Server Gateway Interface) instead of WSGI (Web Server Gateway Interface). You can get more information on ASGI vs WSGI [Here.](https://www.programmersought.com/article/60453596349/)
- While Flask and Django have limited async support, FastAPI has enabled asynchronous endpoint support by default.
- Uses SwaggerUI and ReDoc to automatically document endpoints. This allows developers to focus on the code instead of downloading a bunch of random tools.
- FastAPI makes use of Python 3.6 type declarations, this means that it uses a Python feature that allows you to specify the type of a variable, and this framework makes extensive use out of it - providing developers with great editor support. Autocompletion also works with VSCode!
- It also provides suport for OAuth2 (JWT Tokens), API Keys, headers and query parameters.
We've also used uvicorn here as uvicorn is a lightning-fast ASGI server implementation.

# Future Improvements
- Adding support for more commands
- Refactoring all applicant and assignment endpoints into API routers to make maintaining the code easier
- Adding some sort of functionality to automatically email selected applicants a message through the command line interface
- Create a frontend to make the interface more user friendly
- Expose this script as an API
- Adding multiple language support
- Creating a login system for both recruiters and applicants to facilitate better communication

***Thank You For Reading This Documentation! Please Feel Free to Message Me if You've Any Questions! :)***

# Resources
- [FastAPI](https://fastapi.tiangolo.com)
- [Uvicorn](https://www.uvicorn.org)
- [Python](https://docs.python.org/3/)
