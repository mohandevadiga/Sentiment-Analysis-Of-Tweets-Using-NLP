from flask import Flask, request, render_template_string
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# --- 1. SETUP ---

# Initialize Flask app
app = Flask(__name__)

# Initialize NLTK's VADER Sentiment Analyzer
# Note: You need to have run nltk.download('vader_lexicon') once before
try:
    sia = SentimentIntensityAnalyzer()
except LookupError:
    print("VADER lexicon not found. Please run this in your Python interpreter:")
    print("import nltk")
    print("nltk.download('vader_lexicon')")
    exit()

# --- 2. FRONTEND (HTML/CSS/JS) ---
# We embed the HTML directly in our Python file.
# This makes it a single-file application.

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tweet Sentiment Analysis</title>
    <style>
    body {
        font-family: 'Roboto', sans-serif;
        background-color:skyblue;
        background-size: cover;
        color: #333;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }


        .container {
            background-color: #ffffff;
            padding: 2rem 3rem;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 90%;
            max-width: 600px;
        }

        h1 {
            color:green; /* Twitter Blue */
            margin-bottom: 1.5rem;
        }

        textarea {
            width: 100%;
            padding: 0.8rem;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 1rem;
            margin-bottom: 1rem;
            resize: vertical;
            min-height: 80px;
            box-sizing: border-box;
        }

        button {
            background-color: #1DA1F2;
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            border-radius: 25px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #0c85d0;
        }

        .result {
            margin-top: 2rem;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: left;
            display: none; /* Hidden by default */
        }

        .result.positive {
            background-color: #e0f8e9;
            border-left: 5px solid #34a853; /* Green */
        }

        .result.negative {
            background-color: #fce8e6;
            border-left: 5px solid #ea4335; /* Red */
        }

        .result.neutral {
            background-color: #fef0e0;
            border-left: 5px solid #fbbc05; /* Yellow */
        }
        
        .result h2 {
            margin-top: 0;
            font-size: 1.5rem;
        }

        .result p {
            margin: 0.5rem 0;
            font-size: 1.1rem;
        }

        .result .scores {
            margin-top: 1rem;
            font-size: 0.9rem;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1> Sentiment Analysis Of Tweets (NLP) </h1>
        <form method="post">
            <textarea name="tweet_text" placeholder="Enter a tweet or any text here..." required>{{ user_text }}</textarea>
            <button type="submit">Analyze Sentiment</button>
        </form>

        {% if result %}
        <div class="result {{ result.sentiment_class }}" style="display: block;">
            <h2>{{ result.sentiment }}</h2>
            <p>The overall sentiment of the text is considered <strong>{{ result.sentiment_label }}</strong>.</p>
            <div class="scores">
                <strong>Detailed Scores:</strong><br>
                Positive: {{ "%.2f"|format(result.scores.pos * 100) }}%<br>
                Neutral: {{ "%.2f"|format(result.scores.neu * 100) }}%<br>
                Negative: {{ "%.2f"|format(result.scores.neg * 100) }}%<br>
                <br>
                <strong>Compound Score:</strong> {{ result.scores.compound }} (This score summarizes the sentiment)
            </div>
        </div>
        {% endif %}

    </div>
</body>
</html>
"""

# --- 3. BACKEND LOGIC ---

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    user_text = ""
    if request.method == 'POST':
        user_text = request.form.get('tweet_text', '')
        if user_text:
            # Get sentiment scores
            scores = sia.polarity_scores(user_text)
            
            # Determine sentiment based on the compound score
            compound_score = scores['compound']
            if compound_score >= 0.05:
                sentiment = "Positive "
                sentiment_class = "positive"
                sentiment_label = "Positive"
            elif compound_score <= -0.05:
                sentiment = "Negative "
                sentiment_class = "negative"
                sentiment_label = "Negative"
            else:
                sentiment = "Neutral "
                sentiment_class = "neutral"
                sentiment_label = "Neutral"

            result = {
                "sentiment": sentiment,
                "sentiment_class": sentiment_class,
                "sentiment_label": sentiment_label,
                "scores": scores,
            }
            
    # Render the HTML template, passing the result to it
    return render_template_string(HTML_TEMPLATE, result=result, user_text=user_text)

# --- 4. RUN THE APP ---

if __name__ == '__main__':
    # The 'debug=True' option makes the server auto-reload on code changes
    # and provides helpful error messages.
    # For production, this should be set to False.
    
    app.run(debug=True, use_reloader=False)
