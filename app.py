from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from joblib import load
import mysql.connector 

app = Flask(__name__)
CORS(app)
model = load('/Users/sofiagonzalez/Desktop/InnovationEngineering/my_trained_model.joblib')

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user = "exoplanet_user",
        password = "Sofimessi13!",
        database = "exoplanet_explorer"
    )


@app.route('/')
def home():
    """Serve the home page."""
    return render_template('home.html')

@app.route('/learn')
def learn():
    """Serve the learn more about exoplanets page."""
    return render_template('learn.html')

@app.route('/contact')
def contact():
    """Serve the Contact Us page."""""
    return render_template('contact.html')

@app.route('/how-to-use')
def how_to_use():
    """Serve the Know How to Use page."""""
    return render_template('how-to-use.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Serve the exoplanet predictor page and handle predictions."""
    if request.method == 'POST':
        data = request.get_json()
        features = data['features']
        probabilities = model.predict_proba([features])
        probability_of_exoplanet = 1 - probabilities[0][1]  
        prediction = 1 if probability_of_exoplanet > 0.5 else 0
        return jsonify({'prediction': probability_of_exoplanet})
    return render_template('predict.html')

@app.route('/articles')
def articles():
    """Serve the articles listing page."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('articles.html', articles=articles)

@app.route('/articles/new', methods=['GET', 'POST'])
def new_article():
    """Serve the page to create a new article."""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO articles (title, content, author) VALUES (%s, %s, %s)", (title, content, author))
        db.commit()
        cursor.close()
        db.close()
        
        return redirect(url_for('articles'))
    return render_template('new_article.html')

@app.route('/articles/<int:id>/edit', methods=['GET', 'POST'])
def edit_article(id):
    """Serve the page to edit an existing article."""
    db = get_db_connection()
    cursor = db.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        
        cursor.execute("UPDATE articles SET title = %s, content = %s, author = %s WHERE id = %s", (title, content, author, id))
        db.commit()
        cursor.close()
        db.close()
        
        return redirect(url_for('articles'))
    
    cursor.execute("SELECT * FROM articles WHERE id = %s", (id,))
    article = cursor.fetchone()
    cursor.close()
    db.close()
    
    return render_template('edit_article.html', article=article)

@app.route('/articles/<int:id>/delete', methods=['POST'])
def delete_article(id):
    """Handle deleting an article."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM articles WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    db.close()
    
    return redirect(url_for('articles'))


if __name__ == '__main__':
    app.run(debug=True)
