import logging
import pyodbc
import json
import os
import time
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    sqlConnectionString = os.environ["SQLCONNSTR_SQLConnectionString"]
    turkeySize = ''
    messages = []
    statusCode = 200
    ingredients = []

    try:
        turkeySize = req.params.get('turkey')
        logging.info(turkeySize)
        turkeySize1 = req.params.get('turkey1')
        logging.info(turkeySize1)		
    except:
        messages.append('Use the query string "turkey" to send a turkey weight in lbs.')
        return generateHttpResponse(ingredients, messages, 400)

    sqlConnection = getSqlConnection(sqlConnectionString)
    ingredients = getIngredients(sqlConnection, turkeySize)
    ingredients1 = getIngredients1(sqlConnection, turkeySize1)
	
    return generateHttpResponse1(ingredients, ingredients1, statusCode)

def generateHttpResponse(ingredients, messages, statusCode):
    return func.HttpResponse(
        json.dumps({"Messages": messages, "Ingredients": ingredients}, sort_keys=True, indent=4),
        status_code=statusCode
    )

def generateHttpResponse1(ingredients, ingredients1, statusCode):
    return func.HttpResponse(
        json.dumps({"Messages": ingredients1, "Ingredients": ingredients}, sort_keys=True, indent=4),
        status_code=statusCode
    )
	
def getSqlConnection(sqlConnectionString):
    i = 0
    while i < 6:
        logging.info('contacting DB')
        try:
            sqlConnection = pyodbc.connect(sqlConnectionString)
        except:
            time.sleep(10) # wait 10s before retry
            i+=1
        else:
            return sqlConnection

def getIngredients(sqlConnection, turkeySize):
    logging.info('getting iotdata1')
    results = []
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute('EXEC iotdata1 '+turkeySize)
    results = json.loads(sqlCursor.fetchone()[0])
    sqlCursor.commit()
    sqlCursor.close()
    return results
def getIngredients1(sqlConnection, turkeySize):
    logging.info('getting plugname1')
    results = []
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute('EXEC plugname1 '+turkeySize)
    results = json.loads(sqlCursor.fetchone()[0])
    sqlCursor.commit()
    sqlCursor.close()
    return results	