from flask import Flask, request, jsonify
import pandas as pd
import json
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
from dotenv import dotenv_values

app = Flask(__name__)
config = dotenv_values(".env")


@app.route("/")
def status():
    data = {
        'message': 'Hello World!'
    }
    return jsonify(data), 200


@app.route("/verification", methods=['POST'])
def verify():
    rows = []
    if request.is_json:
        data = request.json
        try:
            input_data = data["input"]
            input_data["job_id"] = data["job_id"]
            for modified_classification in data['modified_classifications']:
                classification_data = data["modified_classifications"][modified_classification]
                classification_data["modified_classification"] = modified_classification
                rows.append(dict(input_data, **classification_data))
        except:
            return jsonify({"error": "JSON body not correctly formatted"}), 400
        df = pd.DataFrame.from_dict(rows)
        df.columns = map(str.upper, df.columns)
        cnx = snowflake.connector.connect(
            user=config["SNOWFLAKE_USER"],
            password=config["SNOWFLAKE_PASSWORD"],
            account=config["SNOWFLAKE_ACCOUNT"],
            warehouse=config["SNOWFLAKE_WAREHOUSE"],
            database=config["SNOWFLAKE_DATABASE"],
            schema=config["SNOWFLAKE_SCHEMA"],
            role=config["SNOWFLAKE_ROLE"]
        )
        success, nchunks, nrows, _ = write_pandas(cnx, df, "VERIFICATION_RESULTS")
        return jsonify({"message": "data received"}), 200
    else:
        return jsonify({"error": "Request body is not in JSON format"}), 400
