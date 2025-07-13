# Sentiment Analysis Web App

A web application for sentiment analysis using machine learning models. Users can analyze the sentiment of single sentences or upload CSV files for bulk analysis. The app provides a modern, user-friendly interface and visualizes sentiment distribution for bulk predictions.

## Features

- Predict sentiment (Positive/Negative) for single sentences
- Bulk sentiment analysis via CSV upload
- Downloadable prediction results
- Sentiment distribution pie chart for bulk analysis
- Modern Bootstrap-based UI

## Tech Stack

- Python 3
- Flask
- scikit-learn, pandas, matplotlib, nltk
- Bootstrap 5 (frontend)

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Sentiment-Analysis
```

### 2. Install dependencies

It is recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install manually:

```bash
pip install flask pandas scikit-learn matplotlib nltk
```

### 3. Download NLTK stopwords

The app will attempt to download stopwords automatically. If you encounter SSL errors, run:

```python
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('stopwords')
```

### 4. Place Model Files

Ensure the following files are in the project root:

- `model_dt.pkl` (Decision Tree model)
- `model_xgb.pkl` (XGBoost model, if used)
- `scaler.pkl` (feature scaler)
- `countVectorizer.pkl` (CountVectorizer)

### 5. Run the App

```bash
python3 api.py
```

The app will run on [http://localhost:5001](http://localhost:5001)

### 6. Using the App

- Open your browser and go to [http://localhost:5001](http://localhost:5001)
- Enter a sentence or upload a CSV file for sentiment analysis

## File Structure

```
Sentiment Analysis/
├── api.py
├── app.py
├── model_dt.pkl
├── model_xgb.pkl
├── scaler.pkl
├── countVectorizer.pkl
├── amazon_alexa.tsv
├── Sentiment_Analysis.ipynb
├── templates/
│   └── Landing.html
```

## Notes

- For bulk analysis, your CSV must have a column named `Sentence`.
- This app is for educational/demo purposes. For production, use a WSGI server and secure your endpoints.

## License

MIT
