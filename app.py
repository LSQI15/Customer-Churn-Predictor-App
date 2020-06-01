import logging.config
import pandas as pd
import pickle
import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from src.customer_db import Customer
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="app/templates")
rf = pickle.load(open('models/rf.pkl', 'rb'))

from src.helper import make_ingest_df
from src.customer_db import ingest_db

app.config.from_pyfile('config/flaskconfig.py')
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/database')
def database():
    """Main view that lists customers and their predicted outcome of churning in the database.
    Create view into index page that uses data queried from Customer database and
    inserts it into the app/templates/index.html template.
    Returns: rendered html template
    """
    try:
        customers = db.session.query(Customer).limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("databse page accessed")
        return render_template('show_db.html', customers=customers)
    except:
        traceback.print_exc()
        logger.warning("Not able to display customers, error page returned")
        return render_template('error.html')


@app.route('/predict', methods=['POST'])
def predict():
    # get user inputs for binary features
    SeniorCitizen = 'No'
    if 'SeniorCitizen' in request.form:
        SeniorCitizen = 'Yes'
    logger.info('SeniorCitizen: ' + SeniorCitizen)

    Partner = 'No'
    if 'Partner' in request.form:
        Partner = 'Yes'
    logger.info('Partner: ' + Partner)

    Dependents = 'No'
    if 'Dependents' in request.form:
        Dependents = 'Yes'
    logger.info('Dependents: ' + Dependents)

    PhoneService = 'No'
    if 'PhoneService' in request.form:
        PhoneService = 'Yes'
    logger.info('PhoneService: ' + PhoneService)

    OnlineSecurity = 'No'
    if 'OnlineSecurity' in request.form:
        OnlineSecurity = 'Yes'
    logger.info('OnlineSecurity: ' + OnlineSecurity)

    OnlineBackup = 'No'
    if 'OnlineBackup' in request.form:
        OnlineBackup = 'Yes'
    logger.info('OnlineBackup: ' + OnlineBackup)

    DeviceProtection = 'No'
    if 'DeviceProtection' in request.form:
        DeviceProtection = 'Yes'
    logger.info('DeviceProtection: ' + DeviceProtection)

    TechSupport = 'No'
    if 'TechSupport' in request.form:
        TechSupport = 'Yes'
    logger.info('TechSupport: ' + TechSupport)

    StreamingTV = 'No'
    if 'StreamingTV' in request.form:
        StreamingTV = 'Yes'
    logger.info('StreamingTV: ' + StreamingTV)

    StreamingMovies = 'No'
    if 'StreamingMovies' in request.form:
        StreamingMovies = 'Yes'
    logger.info('StreamingMovies: ' + StreamingMovies)

    PaperlessBilling = 'No'
    if 'PaperlessBilling' in request.form:
        PaperlessBilling = 'Yes'
    logger.info('PaperlessBilling: ' + PaperlessBilling)

    # get user inputs for numeric features
    Tenure = float(request.form["Tenure"])
    logger.info('Tenure: ' + str(Tenure))
    MonthlyCharges = float(request.form["MonthlyCharges"])
    logger.info('MonthlyCharges: ' + str(MonthlyCharges))
    TotalCharges = float(request.form["TotalCharges"])
    logger.info('TotalCharges: ' + str(TotalCharges))

    # get user inputs for multi-category features
    Gender = 'Female'
    if request.form["Gender"] == '1':
        Gender = 'Male'
    logger.info('Gender: ' + Gender)

    MultipleLines = 'No'
    if request.form["MultipleLines"] == '1':
        MultipleLines = 'Yes'
    elif request.form["MultipleLines"] == '2':
        MultipleLines = 'No phone service'
    logger.info('MultipleLines: ' + MultipleLines)

    InternetService = 'No'
    if request.form["InternetService"] == '1':
        InternetService = 'DSL'
    elif request.form["InternetService"] == '2':
        InternetService = 'Fiber optic'
    logger.info('InternetService: ' + InternetService)

    Contract = 'Month-to-month'
    if request.form["Contract"] == '1':
        Contract = 'One year'
    elif request.form["Contract"] == '2':
        Contract = 'Two year'
    logger.info('contact: ' + Contract)

    PaymentMethod = 'Electronic check'
    if request.form["PaymentMethod"] == '1':
        PaymentMethod = 'Mailed check'
    elif request.form["PaymentMethod"] == '2':
        PaymentMethod = 'Bank transfer (automatic)'
    elif request.form["PaymentMethod"] == '3':
        PaymentMethod = 'Credit card (automatic)'
    logger.info('PaymentMethod: ' + PaymentMethod)

    # combine user inputs into a pandas dataframe for
    values = [Gender, SeniorCitizen, Partner, Dependents, Tenure, PhoneService, OnlineSecurity, OnlineBackup,
              DeviceProtection, TechSupport, StreamingTV, StreamingMovies, PaperlessBilling, MonthlyCharges,
              TotalCharges, MultipleLines, InternetService, Contract, PaymentMethod]
    cols = ['Gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Tenure', 'PhoneService', 'OnlineSecurity',
            'OnlineBackup',
            'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'PaperlessBilling', 'MonthlyCharges',
            'TotalCharges', 'MultipleLines', 'InternetService', 'Contract', 'PaymentMethod']

    # combine user inputs to a data frame
    preprocessed_df = pd.DataFrame(data=[values], columns=cols)
    logger.info('User input has been retrieved.')

    # use random forest model to make prediction
    ingest_df = make_ingest_df(rf, preprocessed_df)
    output = ingest_df.PredProbability[0]
    logger.info('The predicted probability of churn for the given customer is: ' + str(output))

    # ingest this record to the customer database
    ingest_db(ingest_df, db.get_engine())
    logger.info('User input and the corresponding predictions haven been added to the database.')

    user_input_str = preprocessed_df.T.reset_index().rename(columns={'index': 'Features', 0: 'Values'}).to_html()

    if output > 0.75:
        recommendation = 'This customer has a high risk of churning. The recommended offer is to lower fees for 6 months.'
    elif output > 0.50:
        recommendation = 'This customer has a moderate risk of churning. The recommended offer is to lower fees for 3 months.'
    elif output > 0.25:
        recommendation = 'This customer has a low risk of churning. The recommended offer is to lower fees for 1 month.'
    else:
        recommendation = 'This customer is not at risk. No action is needed.'

    return render_template('index.html', tables=user_input_str, rec=recommendation,
                           prediction_text='Based on the following input values, the probability that this customer will churn is: {}'.format(
                               round(output, 5)))


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
