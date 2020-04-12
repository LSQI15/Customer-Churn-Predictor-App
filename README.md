# MSiA423 Customer Churn Prediction - Project Repository

<!-- toc -->

### Developer: Siqi Li

### QA: Luping Zhao

## Project Charter 

**Vision**:

Customer attrition refers to the loss of customers by a business. No matter whether a customer is a one-time purchaser or a loyal program member, customers will eventually churn and not remain active indefinitely. The loss of customers is undesirable, as in most of the cases, the cost to retain a customer is lower than that to acquire a new customer. Companies in various industries such as telecom companies, insurance companies and restaurants often analyze customer attrition to get a deeper insight into the churn. This project specifically aims to help businesses make reliable predictions for customer churn so that business can implement remedial actions for customer retention.

**Mission**:

This project uses the *Telco customer churn data* compiled by BlastChar on Kaggle.com (https://www.kaggle.com/blastchar/telco-customer-churn). This data set contains information about a telecom company which provides services to 7,043 customers in California. For each customer, it has the binary indicator of whether a customer has churned, along with several demographic predictors such as gender and service attributes such as the monthly payment. The dimension of the dataset is 7,043 rows and 21 columns.

This project enables business stakeholders to predict whether a given customer will churn and get the associated predicted probability of churn by entering parameters such as that customer’s gender, contract term, and monthly charge. Based on the predicted results, business stakeholders can then implement plans to retain customers who are likely to churn. The prediction is based on a supervised machine learning model trained and validated on historical customer attrition data.

**Success criteria**:

- Model performance metric: 80% cross-validated correct classification accuracy on the training data 
- Business outcome metrics: 10% decrease in customer attrition rate resulted from the deployment of the project 


## Backlog

**Main Initiative**:

Deploy a machine learning model to help business stakeholders identify customers who are likely to churn. By applying this model, business stakeholders can take remedial actions for customer retention in advance and ultimately decrease the customer attrition rate.

**Initiative 1: Data Manipulation & Exploratory Data Analysis**

1.	Data overview and descriptive summary statistics (1 point)
2.	Explore each individual variable (4 points)
    *	check the distribution and examine outliers, missing values, etc
    *	clean the data and generate new features if necessary
3.	Assess the relationship between each predictor and the response variable (1 point)
    *	visualize through a matrix of scatterplots
4.	Assess the interaction among variables (1 point)
    *	visualize the correlation matrix
5.	Based on EDA, derive useful insights into customer churn, if any (1 point)

**Initiative 2: Model Development**

1.	Model building 
    *	Split data into the training set and the test set (0 points)
    *	Build a logistic regression model as the baseline model (1 point)
    *	Train a random forest model with grid search to figure out the optimal parameter combination (4 points)
    *	Train an XGBoost model with grid search to figure out the optimal parameter combination (4 points)
    *	Export variable importance and derive useful insights if any (2 points)
2.	Model evaluation
    *	Apply 10-fold cross-validation to evaluate the model performance based on metrics such as correct classification rate and F-1 score. (2 points)
    *	Pick the best model based on performance metrics (0 points)

**Initiative 3: Product Development**

1.	Product building
    *	Construct data pipeline
        *	Use a S3 bucket to store the raw source data
    *	Web app (Flask) Development
        *	Design and build user interface
        *	Achieve all desired functionalities
2.	Product testing and refinement
    *	Conduct unit test to evaluate each functionality and fix bugs
    *	Enhance functionality and refine user interface if time allows
3.	Final roll-out

**Icebox**:
1.	Upload raw data to a S3 bucket
2.	Deploy model with Flask
3.	Design interactive user interface
*	Basically, need to learn more about RD3, S3, Docker and Flask (what they are, how they work together, and how to use them) in order to success complete the project and achieve the desired outcome; but as the quarter progresses, these road blocker will be tackled one by one.


<!-- toc -->

## Repo structure

<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)

<!-- tocstop -->

## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app
### 1. Initialize the database 

#### Create the database with a single song 
To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create_db --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py create_db` creates a database at `sqlite:///data/tracks.db` with the initial song *Radar* by Britney spears. 
#### Adding additional songs 
To add an additional song:

`python run.py ingest --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py ingest` adds *Minor Cause* by Emancipator to the SQLite database located in `sqlite:///data/tracks.db`.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on 
##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/tracks.db'

```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/cmawer/Repos/2020-MSIA423-template-repository/data/tracks.db'
```


### 2. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "penny-lane"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 3. Run the Flask app 

To run the Flask app, run: 

```bash
python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.
