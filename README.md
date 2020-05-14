# MSiA423 Customer Churn Prediction - Project Repository

<!-- toc -->

### Developer: Siqi Li

### QA: Luping(Rachel) Zhao


<!-- toc -->

## Repo structure

<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Build the Docker image for executing the pipeline](#1-Build-the-Docker-image-for-executing-the-pipeline)
  * [2. Download data from Kaggle](#2-Download-data-from-Kaggle)
  * [3. Upload data to a S3 bucket](#3-Upload-data-to-a-S3-bucket)
  * [4. Initialize the database to store user input](#4-Initialize-the-database-to-store-user-input)
    + [SQLite database](#(a)-Set-up-SQLite-database-locally)
    + [Amazon AWS RDS](#(b)-Set-up-Amazon-AWS-RDS)
- [Project Charter](#project-charter)

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
│   ├── logging/                      <- Configuration of python loggers
│   ├── .awsconfig                    <- Configurations for AWS
│   ├── .mysqlconfig                  <- Configurations for Amazon AWS RDS
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. 
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
├── src/                              <- Source code for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app

### 1. Build the Docker image for executing the pipeline

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run:

```bash
docker build -f app/Dockerfile -t customer_churn .
```

### 2. Download data from Kaggle 

The data can be directly downloaded from `https://www.kaggle.com/blastchar/telco-customer-churn`. The downloaded dataset
`raw_data.csv` is located in the `data` folder.

### 3. Upload data to a S3 bucket

To upload the raw data to a S3 bucket of your choice, you first need to update the AWS credentials `AWS_ACCESS_KEY_ID` 
and `AWS_SECRET_ACCESS_KEY` in `config/.awsconfig`, and then run:

```bash
docker build -f app/Dockerfile -t customer_churn .
docker run --env-file=config/.awsconfig customer_churn run.py upload_data --bucket_name=<YOUR_BUCKET_NAME>
```
    
By default, it will upload `data/raw_data.csv` to `<YOUR_BUCKET_NAME>`

### 4. Initialize the database to store user input

#### (a) Set up SQLite database locally

To create the database locally using SQLite, please edit the `config/flaskconfig.py` file if you want to make change to 
the engine string, the host or the port number. Otherwise, it will use the default Configurations:

* `PORT = 5000`
* `HOST = "0.0.0.0"`
* `LOCAL_ENGINE_STRING = 'sqlite:///data/customer.db'`

After updating the configurations, run: 
    
```bash
docker build -f app/Dockerfile -t customer_churn .
docker run --mount type=bind,source="$(pwd)"/data,target=/app/data customer_churn run.py create_db --rds=False
```

By default, this will set up a table `customer` in the SQLite database instance `data/customer.db` .

#### (b) Set up Amazon AWS RDS 

To create the database in Amazon AWS RDS, please first update the following credentials:

* in `config/.awsconfig`: 
    * `AWS_ACCESS_KEY_ID` 
    * `AWS_SECRET_ACCESS_KEY` 
* in `config/.mysqlconfig`:
    * `MYSQL_USER` 
    * `MYSQL_PASSWORD` 

The default MYSQL database configurations are: 
* `MYSQL_HOST=msia423-siqi-li-project.ct7mjfzo5pv8.us-east-1.rds.amazonaws.com`
* `MYSQL_PORT=3306`
* `DATABASE_NAME=msia423_project_db`

After finishing updating the `config/.mysqlconfig`, run:

```bash
docker build -f app/Dockerfile -t customer_churn .
docker run --env-file=config/.mysqlconfig --env-file=config/.awsconfig customer_churn run.py create_db --rds=True
```
    
By default, this will create a table named `customer` within the `msia423_project_db` database in RDS.


## Project Charter 

**Vision**:

Customer attrition refers to the loss of customers by a business. No matter whether a customer is a one-time purchaser or a loyal program member, customers will eventually churn and not remain active indefinitely. The loss of customers is undesirable, as in most of the cases, the cost to retain a customer is lower than that to acquire a new customer. Companies in various industries such as telecom companies, insurance companies and restaurants often analyze customer attrition to get a deeper insight into the churn. This project specifically aims to help a telecom company make reliable predictions for customer churn so that the company can implement remedial actions for customer retention.


**Mission**:

This project uses the *Telco customer churn data* compiled by BlastChar on Kaggle.com (https://www.kaggle.com/blastchar/telco-customer-churn). This data set contains information about a telecom company which provides services to 7,043 customers in California. For each customer, it has the binary indicator of whether a customer has churned, along with several demographic predictors such as gender and service predictors such as the monthly payment. The dimension of the dataset is 7,043 rows by 21 columns.

This project enables business stakeholders at the telecom company to predict whether a given customer will churn and get the associated predicted probability of churn by entering parameters such as the customer’s gender, contract term, and monthly charge. Based on the predicted results, business stakeholders can then implement plans to retain customers who are likely to churn. The prediction is based on a supervised machine learning model trained and validated on historical customer attrition data.

**Success criteria**:

- Model performance metric: 80% cross-validated correct classification accuracy on the training data 
- Business outcome metrics: 10% decrease in customer attrition rate in the month following the deployment of the project 


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
    *	Train random forest models with grid search to figure out the optimal parameter combination (4 points)
    *	Train XGBoost models with grid search to figure out the optimal parameter combination (4 points)
    *	Export variable importance and derive useful insights if any (2 points)
2.	Model evaluation
    *	Apply 10-fold cross-validation to evaluate the model performance (random forest vs. XGBoost) based on metrics such as correct classification rate and F-1 score. (2 points)
    *	Pick the best model based on performance metrics (0 points)

**Initiative 3: Product Development**

1.	Product building
    *	Construct data pipeline (2 points)
        *	Use a S3 bucket to store the raw source data
    *	Web app (Flask) Development (8 points - needs to be broken down more when it comes to execution)
        *	Design and build user interface
        *	Achieve all desired functionalities
2.	Product testing and refinement
    *	Conduct unit tests to evaluate each functionality and fix bugs (8 points - needs to be broken down more when it comes to execution)
    *	Enhance functionality and refine user interface if time allows (4 points)
3.	Final roll-out (2 points)

**Icebox**:
1.	Upload raw data to a S3 bucket
2.	Deploy model with Flask
3.	Design interactive user interface
*	Basically, need to learn more about RD3, S3, Docker and Flask (what they are, how they work together, and how to use them) in order to success complete the project and achieve the desired outcome; but as the quarter progresses, these road blocker will be tackled one by one.



