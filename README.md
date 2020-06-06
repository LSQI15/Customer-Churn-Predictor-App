# MSiA423 Customer Churn Prediction - Project Repository

<!-- toc -->

### Developer: Siqi Li

### QA: Luping(Rachel) Zhao


<!-- toc -->

## Repo structure

<!-- toc -->

- [Directory Structure](#directory-structure)
- [Clone the Repository](#clone-the-repository)
- [Random Forest Model Pipeline](#random-forest-model-pipeline)
    * [1. Set Up Pipeline Configurations](#1-set-up-pipeline-configurations)
        + [AWS credential](#a-aws-credential)
        + [Model Pipeline File Path](#b-model-pipeline-file-path)
    * [2. Build the Docker Image for Executing Model pipeline](#2-build-the-docker-image-for-executing-model-pipeline)
    * [3. Execute the Entire Model Pipeline](#3-execute-the-entire-model-pipeline)
    * [4. Execute model pipeline step by step](#4-execute-model-pipeline-step-by-step)
        + [4.1 Clean the working directory](#41-clean-the-working-directory)
        + [4.2 Download Raw Data from S3 Bucket](#42-download-raw-data-from-s3-bucket)
        + [4.3 Preprocess Raw Data](#43-preprocess-raw-data)
        + [4.4 Featurize Preprocessed Data](#44-featurize-preprocessed-data)
        + [4.5 Conduct Exploratory Data Analysis (EDA)](#45-conduct-exploratory-data-analysis-eda)
        + [4.6 Train a Random Forest Model](#46-train-a-random-forest-model)
        + [4.7 Evaluate Model Performance](#47-evaluate-model-performance)
    * [5. Testing](#5-testing)
        + [5.1 Reproducibility tests](#51-reproducibility-tests)
        + [5.2 Unit tests](#52-unit-tests) 
- [Customer Churn Predictor App](#Customer-Churn-Predictor-App)
    * [1. Set Up App Configurations](#1-set-up-app-configurations)
        + [Flask App Configurations](#a-flask-app-configurations)
        + [AWS RDS Configurations](#b-aws-rds-configurations)
    * [2. Build the Docker Image for Running the App](#2-build-the-docker-image-for-running-the-app)
    * [3. Initialize database](#3-initialize-database)
    * [4. Running the App](#4-running-the-app)
    * [5. Remove Docker Container](#5-remove-docker-container)
- [Project Charter](#Project-Charter)


<!-- tocstop -->

## Directory structure 

```
├── README.md                              <- You are here
├── app
│   ├── templates/                         <- HTML files that is templated and changes based on a set of inputs
│   ├── Dockerfile_App                     <- Dockerfile for building image to run app 
│   ├── Dockerfile_Pipeline                <- Dockerfile for building image to run the random forest model pipeline  
│
├── config                                 <- Directory for configuration files 
│   ├── logging/                           <- Configuration of python loggers
│   ├── .aws                               <- Configurations for AWS and RDS
│   ├── flaskconfig.py                     <- Configurations for Flask API
│   ├── config.yml                         <- Configurations for developing and evaluating the model
│   ├── reproducibility_test_config.yml    <- Configurations for reproducibility tests
│
├── data                                   <- Folder that contains data used or generated. 
│
├── deliverables/                          <- Presentation Slide
│
├── eda/                                   <- Folder that contains exploratory data analysis outputs
│
├── models/                                <- Trained model objects, model predictions, feature importance and model evaluations
│
├── src/                                   <- Source code for the project 
│
├── test/                                  <- Files necessary for running unit tests and reproducibility tests
│   ├── reproducibility_true/              <- expected files for reproduciblity tests
│   ├── unit_test_true                     <- input and expect files for unit tests
│
├── app.py                                 <- Flask wrapper for running the model 
├── run.py                                 <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                       <- Python package dependencies 
```


## Clone the Repository

In order to run the app, you first need to clone the repo to your local machine by running the following bash command.

```shell script
# clone the development branch of the repo 
git clone -b development git@github.com:LSQI15/2020-msia423-Li-Siqi.git

# update  working directory
cd 2020-msia423-Li-Siqi
```

## Random Forest Model Pipeline

### 1. Set Up Pipeline Configurations

#### (a) AWS credential

Step 1 of the model pipeline will require AWS credentials in order to download the raw data from a s3 bucket, As the
result, you need to update the AWS credentials `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in `config/.aws` by 
running the following bash command:

```shell script
vi config/.aws
```

Note: type `i` to enter the insert mode to make changes to the file. After finishing editing, press `ESC` to exit and 
type `:wq` to save the change.

### (b) Model Pipeline File Path

By default:
* all data-related files (raw data, preprocessed data, and featurized data) will be saved in the `data` folder
* all EDA-related files (histograms, correlation heatmap and summary statistics table) will be saved in the `eda` folder
* all model-related files (train/test data, random forest model, predictions, feature importance, and model evaluations) 
will be saved in the `models` folder

To make change to the file paths (eg. store data-related files to `data2`), edit `DATA_PATH`, `EDA_PATH`, and `MODEL_PATH` 
variables on top of the `Makefile` by running the following bash command:

```shell script
vi Makefile
```
Note: type `i` to enter the insert mode to make changes to the file. After finishing editing, press `ESC` to exit and 
type `:wq` to save the change.

If you change default file path configurations, please also update all `test_dir` in `config/reproducibility_test_config.yml` 
accordingly so that the reproducibility tests can run as expected.

 ```shell script
vi config/reproducibility_test_config.yml
```

Note: type `i` to enter the insert mode to make changes to the file. After finishing editing, press `ESC` to exit and 
type `:wq` to save the change.

### 2. Build the Docker Image for Executing Model pipeline

The Dockerfile for running the model pipeline is in the `app/` folder. To build the image, run:

```shell script
docker build -f app/Dockerfile_Pipeline -t customer_churn .
```

### 3. Execute the Entire Model Pipeline

To run the entire model pipeline (clean working directory, download data, preprocess data, create features, conducting 
exploratory data analysis, training a random_forest model, and evaluate model performance) using default configurations,
run:

```shell script
docker run --env-file=config/.aws --mount type=bind,source="$(pwd)",target=/app/ customer_churn all_pipeline
```

As indicated in section 1(b), after running the above command, by default, all data-related files (raw data, preprocessed 
data, and featurized data) will be store in `data/`. All models related files such as EDA graphs, training set, test set
, random forest model, and model evaluations will can be found in `models/`.

### 4. Execute model pipeline step by step

#### 4.1 Clean the working directory

The first step in the model pipeline is to clean the working directory. The following command will remove any existing 
files in `data` ,`eda`, and `model` folders so that you can have a fresh working directory to execute the model pipeline.

```shell script
docker run --mount type=bind,source="$(pwd)",target=/app/ customer_churn clean
```

#### 4.2 Download Raw Data from S3 Bucket

To download the raw data from the default S3 bucket, run the following bash command. Unless you specified another directory
in the Makefile, the raw data will be downloaded to the `data` folder by default.

```shell script
docker run --env-file=config/.aws --mount type=bind,source="$(pwd)",target=/app/ customer_churn download
```

#### 4.3 Preprocess Raw Data

The following command will preprocess the raw data. Specifically, it will 
* process TotalCharges column - convert spaces to NaN and drop 11 missing values
* process SeniorCitizen column - convert from binary 1/0 to Yes/No
* replace 'No internet service' to 'No' for the following 6 columns 'OnlineSecurity', 'OnlineBackup','DeviceProtection',
 'TechSupport', 'StreamingTV', 'StreamingMovies'
* drop the drop the customerID column

By default, the preprocessed file will also be saved to the `data` folder.

```shell script
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn preprocess
```

#### 4.4 Featurize Preprocessed Data

The following bash command will featurize the preprocessed data and save the featurized data in the `data` folder by 
default. 

* encode binary response variable and binary feature
* one-hot encode multi-category features

```shell script
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn feature
```

#### 4.5 Conduct Exploratory Data Analysis (EDA)

The following command will conduct exploratory data analysis including:
* correlation heatmap among variables
* summary statistics for each variable
* histograms of predictors colored by the whether the customer is churned or not

By default, EDA results will be saved in the `models` folder.

```shell script
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn eda
```

#### 4.6 Train a Random Forest Model

The next step in the model pipeline is to train a random forest model using the featurized data. The following command 
will conduct 
* train-test split
* build a random forest model on the training set
* make predictions on the test set
* calculate and visualize feature importance. 

By default, all these output files will be saved in the `models` folder.

```shell script
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn random_forest
```

#### 4.7 Evaluate Model Performance

The final step in the model pipeline is to evaluate model performance. The following bash command will 
* calculate the AUC and Accuracy
* create a confusion matrix
* generate classification report

By default, all these model evaluation metrics will be saved in the `models` folder.

```shell script
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn evaluate
```

### 5. Testing

#### 5.1 Reproducibility tests

To conduct reproducibility test, run the following bash command. The reproducibility test will test output files generated
during each stage the of model development against the expected output saved at `test/reproducibility_true/`.

```shell script
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn reproducibility_test
```

Note: if you made changes to the default file path `DATA_PATH`, `EDA_PATH`, and `MODEL_PATH` in the Makefile, please make
sure you also updated all `test_dir` in `config/reproducibility_test_config.yml` accordingly. If not, please edit them and
then rebuild the Docker image before running the above command.

 ```shell script
vi config/reproducibility_test_config.yml
docker build -f app/Dockerfile_Pipeline -t customer_churn .
```

#### 5.2 Unit tests

The unit testing module test 5 functions to clean features and select the response variable. Each function will be tested
twice - once with valid input and once with invalid input. This leads to a total of 10 tests. To conduct the unit tests,
run the following bash command.

```shell script
docker run  --mount type=bind,source="$(pwd)",target=/app/ customer_churn unit_test
```

## Customer Churn Predictor App

### 1. Set Up App Configurations

#### (a) Flask App Configurations

Please edit the `config/flaskconfig.py` file if you want to make change to the SQLite database name, the host, or the 
port number. Otherwise, the flask app will use the following default configurations:

* `PORT = 5000`
* `HOST = "0.0.0.0"`
* `LOCAL_DATABASE="customer.db"`

#### (b) AWS RDS Configurations
To run the customer churn predictor app, you need to create either a local SQLite database or an AWS RDS database
in order to store user inputs. If you choose to use AWS RDS database, please enter your AWS credentials 
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` and RDS configurations `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, 
`MYSQL_PORT`, and `DATABASE_NAME` in `config/.aws`, by running the following bash command:

```shell script
vi config/.aws
```

Note: type `i` to enter the insert mode to make changes to the file. After finishing editing, press `ESC` to exit and 
type `:wq` to save the change.

### 2. Build the Docker Image for Running the App

The Dockerfile for running the model pipeline is in the `app/` folder. To build the image, run:

```shell script
docker build -f app/Dockerfile_App -t predictor_app .
```

### 3. Initialize database

To store user inputs and their corresponding predictions, you can use either a local SQLite database or an AWS RDS 
database. By default, the following command will create a table named `customer` in the database of your choice. You can 
also conduct an initial ingestion of 5 records if you would like to do so.

```shell script
########################
# Local SQLite Database
########################
# create local SQLite database
docker run --mount type=bind,source="$(pwd)",target=/app/ predictor_app run.py create_db
# optional: conduct an initial ingestion
docker run --mount type=bind,source="$(pwd)",target=/app/ predictor_app run.py initial_ingest


########################
# AWS RDS Database
########################
# create AWS RDS database
docker run --env-file=config/.aws --mount type=bind,source="$(pwd)",target=/app/ predictor_app run.py create_db
# optional: conduct an initial ingestion
docker run --env-file=config/.aws --mount type=bind,source="$(pwd)",target=/app/ predictor_app run.py initial_ingest
```

### 4. Running the App

After initializing the databse, to run the customer churn predictor app, enter:

```shell script
# Local SQLite Database
docker run --mount type=bind,source="$(pwd)",target=/app/ -p 5000:5000 --name myapp predictor_app app.py

# AWS RDS Database
docker run --env-file=config/.aws -p 5000:5000 --name myapp predictor_app app.py
```

The app will be running on a local host at `http://0.0.0.0:5000/`. You can press `CTRL+C` at any time to quit.


### 5. Remove Docker Container

After using the app, please enter the following bash command to remove the Docker container

```shell script
docker rm myapp
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



