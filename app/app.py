from flask import Flask, render_template_string, request
import sqlite3

app = Flask(__name__)

# Create a simple database
def init_db():
    conn = sqlite3.connect('mydata.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

# HTML form template
HTML = '''
<!DOCTYPE html>
<html>
<body>
  <h2>Add Item</h2>
  <form method="post">
    <input type="text" name="item" required>
    <button type="submit">Submit</button>
  </form>
  <h3>Saved Items:</h3>
  <ul>
    {% for item in items %}
    <li>{{ item }}</li>
    {% endfor %}
  </ul>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    init_db()
    if request.method == 'POST':
        # Save submitted data
        conn = sqlite3.connect('mydata.db')
        c = conn.cursor()
        c.execute("INSERT INTO items (name) VALUES (?)", 
                 (request.form['item'],))
        conn.commit()
        conn.close()
    
    # Show all saved items
    conn = sqlite3.connect('mydata.db')
    c = conn.cursor()
    items = [row[1] for row in c.execute("SELECT * FROM items")]
    conn.close()
    
    return render_template_string(HTML, items=items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
