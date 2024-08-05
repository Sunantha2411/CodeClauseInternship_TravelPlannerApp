from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('travel_planner.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                activities TEXT
            )
        ''')
        conn.commit()

init_db()

@app.route('/')
def index():
    with sqlite3.connect('travel_planner.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM trips')
        trips = c.fetchall()
    return render_template('index.html', trips=trips)

@app.route('/add', methods=['POST'])
def add_trip():
    destination = request.form['destination']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    activities = request.form.get('activities', '')

    with sqlite3.connect('travel_planner.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO trips (destination, start_date, end_date, activities) VALUES (?, ?, ?, ?)',
                  (destination, start_date, end_date, activities))
        conn.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:trip_id>', methods=['POST'])
def delete_trip(trip_id):
    with sqlite3.connect('travel_planner.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM trips WHERE id = ?', (trip_id,))
        conn.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
