from flask import Flask, request, jsonify, send_file, render_template 
import re 
from io import BytesIO
import nltk
import ssl
import traceback

# Fix SSL certificate issue for NLTK downloads
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download stopwords if not already downloaded
try:
    from nltk.corpus import stopwords
    STOPWORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    STOPWORDS = set(stopwords.words("english"))
from nltk.stem.porter import PorterStemmer
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import base64


    
app = Flask(__name__)

@app.route("/test", methods=["GET"])
def test():
    return "Test request received successfully. Service is running."

@app.route("/", methods=[ "GET", "POST"])
def home():
    return render_template("Landing.html")

@app.route("/predict", methods=[ "POST"])
def predict():
    # Select the predictor to be loaded from Models folder
    predictor = pickle.load(open(r"model_dt.pkl", "rb"))
    scaler = pickle.load(open(r"scaler.pkl", "rb"))
    cv = pickle.load(open (r"countVectorizer.pkl", "rb"))
    try:
        # Check if the request contains a file (for bulk prediction) or text input
        if "file" in request.files:
            # Bulk prediction from CSV file
            file = request. files["file"]
            data = pd.read_csv(file)
            
            predictions, graph = bulk_prediction(predictor, scaler, cv, data)
            response = send_file(
                predictions, 
                mimetype="text/csv",
                as_attachment=True,
                download_name="Predictions.csv",
            )
            
            response.headers ["X-Graph-Exists"] = "true"
            
            response. headers ["X-Graph-Data"] = base64.b64encode (
                graph. getbuffer ()
            ).decode( "ascii")
            
            return response
        elif request.is_json and "text" in request.json:
            # Single string prediction
            text_input = request.json[ "text"]
            predicted_sentiment = single_prediction(predictor, scaler, cv, text_input)
            return jsonify({"prediction": predicted_sentiment})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)})
    
def single_prediction (predictor, scaler, cv, text_input) :
    corpus = []
    stemmer = PorterStemmer()
    review = re.sub("[^a-zA-Z]", " ", text_input)
    review = review.lower().split()
    review = [stemmer.stem(word) for word in review if not word in STOPWORDS]
    review = " ".join(review)
    corpus.append (review)
    X_prediction = cv.transform (corpus).toarray ()
    X_prediction_scl = scaler.transform(X_prediction)
    y_predictions = predictor.predict_proba(X_prediction_scl)
    y_predictions = y_predictions.argmax(axis=1)[0]
    
    return "Positive" if y_predictions == 1 else "Negative"

def bulk_prediction (predictor, scaler, cv, data):
    corpus = []
    stemmer = PorterStemmer()
    for i in range(0, data.shape[0]):
        review = re.sub("[^a-zA-z]", " ", data.iloc[i][ "Sentence"])
        review = review.lower().split()
        review = [stemmer.stem(word) for word in review if not word in STOPWORDS]
        review = " ".join (review)
        corpus.append(review)
        
    X_prediction = cv. transform (corpus) .toarray()
    X_prediction_scl = scaler. transform(X_prediction)
    y_predictions = predictor. predict_proba(X_prediction_scl)
    y_predictions = y_predictions.argmax(axis=1)
    y_predictions = list(map(sentiment_mapping, y_predictions))
    
    data["Predicted sentiment"] = y_predictions
    predictions_csv = BytesIO()
    data.to_csv(predictions_csv, index=False)
    predictions_csv.seek(0)
    
    graph = get_distribution_graph(data)
    return predictions_csv, graph

def get_distribution_graph(data):
    fig = plt. figure(figsize=(5, 5))
    colors = ("green", "red")
    wp = {"Linewidth": 1, "edgecolor": "black"}
    tags = data[ "Predicted sentiment"]. value_counts()
    explode = (0.01, 0.01)
    tags.plot(
        kind="pie",
        autopct="%1.1f%%",
        shadow=True, 
        colors=colors,
        startangle=90,
        wedgeprops=wp,
        explode=explode, 
        title="Sentiment Distribution",
        xlabel="",
        ylabel="",
    )
    
    graph = BytesIO()
    plt.savefig(graph, format="png")
    plt.close()
    
    return graph

def sentiment_mapping(x):
    if x == 1:
        return "Positive"
    else:
        return "Negative"
    
if __name__ == "__main__":
    app.run(port=5001, debug=True)