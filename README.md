# Amazon Review Analyzer

## Business Problem Statement
Understanding customer sentiment is crucial for e-commerce success. This project analyzes Amazon product reviews to automatically classify them as positive or negative. The insights derived from this sentiment analysis can help businesses understand customer satisfaction, identify areas for product improvement, and make data-driven decisions to enhance the overall customer experience.

## Economic Concepts Applied
* **Demand-Supply:** Positive sentiment can signal high demand and satisfaction, while negative sentiment could indicate issues affecting product demand.
* **Revenue Optimization:** By addressing common complaints found in negative reviews, companies can improve their products, leading to higher customer retention and increased long-term revenue.
* **Pricing Strategy:** Products with consistently high positive sentiment might support premium pricing strategies.
* **Risk Analysis:** Identifying sudden spikes in negative reviews allows for rapid risk mitigation, avoiding brand damage and potential financial losses.

## AI Techniques Used
* **Machine Learning:**
  * **Logistic Regression:** Used as a strong supervised baseline model for binary classification, trained on TF-IDF word embeddings.
  * **K-Means Clustering:** An unsupervised learning algorithm used to explore natural groupings and segment the text data.
* **Natural Language Processing (NLP):** Techniques such as text cleaning (removing HTML, non-alphabetic characters), tokenization, padding, and Term Frequency-Inverse Document Frequency (TF-IDF) feature extraction.
* **Word Embeddings:** Converting words into dense vectors to capture semantic meanings.

## Dataset Link
[Amazon Review Polarity Dataset](https://www.kaggle.com/datasets/kritanjalijain/amazon-reviews)

## Execution Guide
To properly run this project locally or on a remote server, simply follow these steps:

1. **Run the First Cell**:
   - Open `sentiment-analysis-amazon-reviews.ipynb` in VS Code or Jupyter Lab.
   - Run the very first cell to ensure all required libraries (`pandas`, `scikit-learn`, `kagglehub`, etc.) are installed on your environment or server.

2. **Automatic Data Download**:
   - The notebook is intentionally configured to automatically securely download the 3.6GB `amazon-reviews` dataset via the Kaggle API (`kagglehub`) directly into your server's cache when you run the data-loading cell.
   - You **do not** need to manually download or move any files. 

3. **Run All**:
   - Click **"Run All"** to execute the notebook from top to bottom.
   - The script will automatically sample 50,000 rows (to avoid memory crashes on most standard machines) to train the K-Means Sentiment Clusters and the Review-Sales Linear Regression model.
