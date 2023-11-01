# Web scraping
from Web_scraping import web_scrapper
web_scrapper()
#from flask import Flask, render_template, request, jsonify
import sqlite3
from flask import Flask, render_template


#flask code
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("Home.html")
    #return "hello"

@app.route('/get_population', methods=['GET'])
def get_population():
    # Connect to the SQLite database
    connection = sqlite3.connect('population.db')
    cursor = connection.cursor()

    # Retrieve the total population from the 'total_population' table
    cursor.execute("SELECT * FROM total_population")
    total_population = cursor.fetchall()

    connection.close()

    # Render the population data as a table using the HTML template
    return render_template('population_table.html', population=total_population)

@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/data_description')
def data_description():
    return render_template("data_description.html")

if __name__ == '__main__':
    app.run(debug=True,port=8080)
