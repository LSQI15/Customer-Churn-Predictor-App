# MSiA423 Customer Churn Prediction - Project Repository

<!-- toc -->

### Developer: Siqi Li

### QA: Luping(Rachel) Zhao


<!-- toc -->

## Repo structure

<!-- toc -->

- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Clone the Repository](#1-Clone-the-Repository)
  * [2. Set up configurations](#2-Set-up-configurations)
  * [3. Build the Docker image for executing the pipeline](#3-Build-the-Docker-image-for-executing-the-pipeline)
  * [4. Download data from Kaggle](#4-Download-data-from-Kaggle)
  * [5. Upload data to a S3 bucket](#5-Upload-data-to-a-S3-bucket)
  * [6. Initialize the database to store user input](#6-Initialize-the-database-to-store-user-input)
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

### 1. Clone the Repository

In order to run the app, you first need to clone the repo to your local machine by running the following bash command.

```bash
# clone the development branch of the repo 
git clone -b development git@github.com:LSQI15/2020-msia423-Li-Siqi.git

# update  working directory
cd 2020-msia423-Li-Siqi
```

### 2. Set up configurations

#### (a) Flask app configurations

Please edit the `config/flaskconfig.py` file if you want to make change to the SQLite database name, the host, or the 
port number. Otherwise, the flask app will use the default configurations:

* `PORT = 5000`
* `HOST = "0.0.0.0"`
* `LOCAL_DATABASE="customer.db"`

#### (b) AWS credential & RDS configurations

Step 1 of the model pipeline will require AWS credentials in order to download the raw data from a s3 bucket, As a 
result, you need to update the AWS credentials `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in `config/.aws` by 
running the following bash command:

```bash
vi config/.aws
```

Note: type `i` to enter the insert mode to make changes to the file. After finishing editing, press `ESC` to exit and 
type `:wq` to save the change.

### 3. Build the Docker image for executing the pipeline

The Dockerfile for running the model pipeline is in the `app/` folder. To build the image, run:

```bash
docker build -f app/Dockerfile -t customer_churn .
```

### 4. Execute the entire model pipeline

To run the entire model pipeline (clean working directory, download data, preprocess data, create feature, doing 
exploratory data analysis, training a random_forest model, and evaluate model performance), run:

```bash
docker run --env-file=config/.aws --mount type=bind,source="$(pwd)",target=/app/ customer_churn all_pipeline
```

After running the above command, all data-related files (raw data, preprocessed data, and featurized data) will be store
in `data/`. All models related files such as EDA graphs, training set, test set, random forest model, and model evaluations
will can be found in `models/`.

### 5. Execute model pipeline step by step

#### 5.1 Clean the working directory

The first step in the model pipeline is to clean the working directory. The following command will remove any existing 
files in `data` and `model` folders so that you can have a fresh working directory to execute the model pipeline.

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ customer_churn clean
```

#### 5.2 Download raw data from S3 bucket

To download the raw data from the default S3 bucket, run the following bash command. By default, the raw data will be 
downloaded to the `data` folder.

```bash
docker run --env-file=config/.aws --mount type=bind,source="$(pwd)",target=/app/ customer_churn download
```

#### 5.3 Preprocess the raw data

The following command will preprocess the raw data. Specifically, it will 
* process TotalCharges column - convert spaces to NaN and drop 11 missing values
* process SeniorCitizen column - convert from binary 1/0 to Yes/No
* replace 'No internet service' to 'No' for the following 6 columns 'OnlineSecurity', 'OnlineBackup','DeviceProtection',
 'TechSupport', 'StreamingTV', 'StreamingMovies'
* drop the drop the customerID column

By default, the preprocessed file will also be saved to the `data` folder.

```bash
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn preprocess
```

#### 5.4 Featurize the preprocessed data

The following bash command will featurize the preprocessed data and save the featurized data in the `data` folder by default. 

* encode binary response variable and binary feature
* one-hot encode multi-category features

```bash
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn feature
```

#### 5.5 Conduct Exploratory Data Analysis (EDA)

The following command will conduct exploratory data analysis including:
* correlation heatmap among variables
* summary statistics for each variable
* histograms of predictors colored by the whether the customer is churned or not

By default, EDA results will be saved in the `models` folder.

```bash
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn eda
```

#### 5.6 Train a random forest model

The next step in the model pipeline is to train a random forest model using the featurized data. The following command 
will conduct 
* train-test split
* build a random forest model on the training set
* make predictions on the test set
* calculate and visualize feature importance. 

By default, all these output files will be saved in the `models` folder.

```bash
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn random_forest
```

#### 5.6 Evaluate model performance

The final step in the model pipeline is to evaluate model performance. The following bash command will 
* calculate the AUC and Accuracy
* create a confusion matrix
* generate classification report

By default, all these model evaluation metrics will be saved in the `models` folder.

```bash
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn evaluate
```

### 6 Testing

#### 6.1 Reproducibility tests

To conduct reproducibility test, run the following bash command. The reproducibility test will test output files generated
during each stage the of model development against the expected output saved at `test/reproducibility_true/`.

```bash
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn reproducibility_test
```

#### 6.2 Unit tests

The unit testing module test 5 functions to clean features and select the response variable. Each function will be tested
twice - once with valid input and once with invalid input. This leads to a total of 10 tests. To conduct the unit tests,
run the following bash command.

```bash
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn unit_test
```

### 7. Running the customer churn predictor app

To run the customer churn predictor app, you need to create either a local SQLite database or an AWS RDS database
in order to store user inputs. 

If you choose to use AWS RDS database, please enter your AWS credentials `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` 
and RDS configurations `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT`, and `DATABASE_NAME` in `config/.aws`,
by running the following bash command:

```bash
vi config/.aws
```

Note: type `i` to enter the insert mode to make changes to the file. After finishing editing, press `ESC` to exit and 
type `:wq` to save the change.

To run the app, enter the following bash command.

```bash
source config/.aws # only if you want to use AWS RDS databse
sh app/boot.sh
```

By default, a table named customer will be created in the database of your choice and  will be initially ingested with 5 
records. The app will be running on a local host at http://0.0.0.0:5000/. You can press CTRL+C at any time to quit.


### 8 Terminate Docker Container

After using the app, please enter the following bash command to stop the Docker container

```bash
docker kill customer_churn
docker rm customer_churn
```



####################################################################


### 5. Upload data to a S3 bucket

To upload the raw data to a S3 bucket of your choice, run:

```bash
docker run --env-file=config/.awsconfig customer_churn run.py upload_data --bucket_name=<YOUR_BUCKET_NAME>
```
    
By default, it will upload `data/raw_data.csv` to the `data` folder in `<YOUR_BUCKET_NAME>`

### 6. Initialize the database to store user input

#### (c) Access the default RDS database

To access the default RDS database, please enter the following bash commands in your terminal:

```bash
source config/.defaultRDS
sh src/run_mysql_client.sh
```
 
After that, run the following MYSQL commands:

```mysql
use msia423_project_db;
describe customer;
```

## Project Charter 

**Vision**:

Customer attrition refers to the loss of customers by a business. No matter whether a customer is a one-time purchaser 
or a loyal program member, customers will eventually churn and not remain active indefinitely. The loss of customers is 
undesirable, as in most of the cases, the cost to retain a customer is lower than that to acquire a new customer. 
Companies in various industries such as telecom companies, insurance companies and restaurants often analyze customer 
attrition to get a deeper insight into the churn. This project specifically aims to help a telecom company make reliable
 predictions for customer churn so that the company can implement remedial actions for customer retention.


**Mission**:

This project uses the *Telco customer churn data* compiled by BlastChar on Kaggle.com (https://www.kaggle.com/blastchar/telco-customer-churn). 
This data set contains information about a telecom company which provides services to 7,043 customers in California. 
For each customer, it has the binary indicator of whether a customer has churned, along with several demographic 
predictors such as gender and service predictors such as the monthly payment. The dimension of the dataset is 7,043 
rows by 21 columns.

This project enables business stakeholders at the telecom company to predict whether a given customer will churn and get
 the associated predicted probability of churn by entering parameters such as the customer’s gender, contract term, and 
 monthly charge. Based on the predicted results, business stakeholders can then implement plans to retain customers who 
 are likely to churn. The prediction is based on a supervised machine learning model trained and validated on historical
  customer attrition data.

**Success criteria**:

- Model performance metric: 80% cross-validated correct classification accuracy on the training data 
- Business outcome metrics: 10% decrease in customer attrition rate in the month following the deployment of the project 


## Backlog

**Main Initiative**:

Deploy a machine learning model to help business stakeholders identify customers who are likely to churn. By applying 
this model, business stakeholders can take remedial actions for customer retention in advance and ultimately decrease 
the customer attrition rate.

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
    *	Train random forest models (4 points)
    *	Export variable importance and derive useful insights if any (2 points)
2.	Model evaluation
    *	Evaluate the model performance based on metrics such as correct classification rate and F-1 score. (2 points)
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
*	Basically, need to learn more about RD3, S3, Docker and Flask (what they are, how they work together, and how to use
 them) in order to success complete the project and achieve the desired outcome; but as the quarter progresses, these 
 road blocker will be tackled one by one.



