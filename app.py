from flask import Flask, render_template, render_template_string, request, redirect, url_for, session
import sqlite3, os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = "dani_secret_key_123"
DB_NAME = "clients.db"

# --------------------------
# 1️⃣ Inițializare baza de date
# --------------------------
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE clients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT,
                        age INTEGER,
                        weight REAL,
                        height REAL,
                        goal TEXT,
                        notes TEXT
                    )''')
        conn.commit()
        conn.close()

# --------------------------
# 2️⃣ Pagina principală
# --------------------------
@app.route('/')
@app.route('/')
def home():    return render_template("index.html")
# --------------------------
# 3️⃣ Formular evaluare
# --------------------------
@app.route('/evaluare', methods=['GET', 'POST'])
def evaluare():
    if request.method == 'POST':
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO clients (name,email,age,weight,height,goal,notes) VALUES (?,?,?,?,?,?,?)",
                  (request.form['name'], request.form['email'], request.form['age'],
                   request.form['weight'], request.form['height'], request.form['goal'], request.form['notes']))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))

    html = '''
    <script src="https://cdn.tailwindcss.com"></script>
    <div class="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <div class="bg-white p-8 rounded-2xl shadow w-full max-w-lg">
        <h2 class="text-2xl font-bold mb-6 text-center">📝 Evaluare inițială</h2>
        <form method="POST" class="space-y-4">
          <input class="w-full p-3 border rounded-xl" name="name" placeholder="Nume complet" required>
          <input class="w-full p-3 border rounded-xl" type="email" name="email" placeholder="Email" required>
          <div class="grid grid-cols-3 gap-3">
            <input class="p-3 border rounded-xl" type="number" name="age" placeholder="Vârstă">
            <input class="p-3 border rounded-xl" type="number" name="weight" placeholder="Greutate (kg)">
            <input class="p-3 border rounded-xl" type="number" name="height" placeholder="Înălțime (cm)">
          </div>
          <select class="w-full p-3 border rounded-xl" name="goal">
            <option>Slăbire</option>
            <option>Masa musculară</option>
            <option>Rezistență / Performanță</option>
            <option>Recuperare / Tonifiere</option>
          </select>
          <textarea class="w-full p-3 border rounded-xl" rows="4" name="notes" placeholder="Accidentări, restricții alimentare..."></textarea>
          <button class="w-full py-3 bg-black text-white rounded-xl hover:bg-gray-800">Trimite evaluarea</button>
        </form>
      </div>
    </div>
    '''
    return render_template_string(html)

@app.route('/success')
def success():
    return '''
    <script src="https://cdn.tailwindcss.com"></script>
    <div class="min-h-screen flex flex-col items-center justify-center bg-green-50 text-center">
      <h3 class="text-2xl font-bold text-green-700 mb-3">✅ Formular trimis cu succes!</h3>
      <p>Mulțumesc! Te voi contacta în 24–48h cu planul personalizat.</p>
      <a href="/" class="mt-5 inline-block px-5 py-3 bg-black text-white rounded-xl hover:bg-gray-800">Înapoi la început</a>
    </div>
    '''

# --------------------------
# 4️⃣ Login admin
# --------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == "admin" and request.form.get('password') == "1234":
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        return '<p class="text-center text-red-600 mt-10">❌ Login greșit!</p><a href="/login">Înapoi</a>'
    
    html = '''
    <script src="https://cdn.tailwindcss.com"></script>
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
      <div class="bg-white p-8 rounded-2xl shadow w-full max-w-sm">
        <h2 class="text-2xl font-bold mb-6 text-center">🔐 Login Admin</h2>
        <form method="POST" class="space-y-4">
          <input class="w-full p-3 border rounded-xl" name="username" placeholder="Utilizator">
          <input class="w-full p-3 border rounded-xl" name="password" type="password" placeholder="Parolă">
          <button class="w-full py-3 bg-black text-white rounded-xl hover:bg-gray-800">Autentificare</button>
        </form>
      </div>
    </div>
    '''
    return render_template_string(html)

# --------------------------
# 5️⃣ Panou Admin
# --------------------------
@app.route('/admin')
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM clients ORDER BY id DESC")
    data = c.fetchall()
    conn.close()

    html = '''
    <script src="https://cdn.tailwindcss.com"></script>
    <div class="min-h-screen bg-gray-50 p-8">
      <div class="max-w-6xl mx-auto bg-white rounded-2xl shadow p-6">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold">📋 Panou Admin – Clienți</h2>
          <a href="/logout" class="px-4 py-2 bg-red-500 text-white rounded-xl hover:bg-red-600">Logout</a>
        </div>
        <table class="min-w-full border-collapse border border-gray-300 text-sm">
          <thead class="bg-gray-200">
            <tr>
              <th class="border p-2">ID</th>
              <th class="border p-2">Nume</th>
              <th class="border p-2">Email</th>
              <th class="border p-2">Obiectiv</th>
              <th class="border p-2">Greutate</th>
              <th class="border p-2">Înălțime</th>
              <th class="border p-2">Note</th>
            </tr>
          </thead>
          <tbody>
            {% for row in data %}
            <tr class="hover:bg-gray-100">
              <td class="border p-2">{{ row[0] }}</td>
              <td class="border p-2 font-semibold">{{ row[1] }}</td>
              <td class="border p-2">{{ row[2] }}</td>
              <td class="border p-2">{{ row[6] }}</td>
              <td class="border p-2">{{ row[4] }}</td>
              <td class="border p-2">{{ row[5] }}</td>
              <td class="border p-2 text-gray-600">{{ row[7] }}</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
    '''
    return render_template_string(html, data=data)

# --------------------------
# 6️⃣ Logout
# --------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# --------------------------
# 7️⃣ Pornire aplicație
# --------------------------
if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000)

