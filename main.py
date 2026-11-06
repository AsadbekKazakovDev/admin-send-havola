from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'maxfiy_kalit_soz_kiriting'  # Seans (session) xavfsizligi uchun

# Oddiy login va parol (buni o'zingiz o'zgartirishingiz mumkin)
USERNAME = "admin"
PASSWORD = "123"

# Havolalar tarixi uchun vaqtinchalik ro'yxat
link_history = []

# HTML Dizayn va Interfeys
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meeting Hub - Tezkor Ulanish</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f6f9; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h2 { color: #333; text-align: center; }
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
        button { background: #007bff; color: white; border: none; padding: 12px 20px; border-radius: 6px; font-size: 16px; cursor: pointer; width: 100%; }
        button:hover { background: #0056b3; }
        .logout { background: #dc3545; margin-top: 15px; }
        .logout:hover { background: #b02a37; }
        .history-item { background: #f8f9fa; padding: 10px; margin: 8px 0; border-left: 4px solid #007bff; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }
        .history-item a { color: #007bff; text-decoration: none; font-weight: bold; }
        .error { color: red; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        {% if not session.get('logged_in') %}
            <h2>Tizimga kirish</h2>
            {% if error %}<p class="error">{{ error }}</p>{% endif %}
            <form method="POST">
                <input type="text" name="username" placeholder="Login" required>
                <input type="password" name="password" placeholder="Parol" required>
                <button type="submit">Kirish</button>
            </form>
        {% else %}
            <h2>Meeting Dashboard</h2>
            <form method="POST" action="/connect">
                <input type="text" name="meeting_link" placeholder="Zoom yoki Google Meet havolasini shu yerga tashlang (Paste)..." required autofocus>
                <button type="submit">Ulanish va Ochish</button>
            </form>
            
            <h3>So'nggi havolalar</h3>
            {% if history %}
                {% for item in history %}
                    <div class="history-item">
                        <span>{{ loop.index }}. Havola</span>
                        <a href="{{ item }}" target="_blank">Ochish ↗</a>
                    </div>
                {% endfor %}
            {% else %}
                <p style="color: #666; text-align: center;">Hozircha havolalar yo'q.</p>
            {% endif %}

            <form action="/logout" method="POST">
                <button type="submit" class="logout">Tizimdan chiqish</button>
            </form>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = "Login yoki parol noto'g'ri!"
    return render_template_string(HTML_TEMPLATE, error=error)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template_string(HTML_TEMPLATE, history=link_history)

@app.route('/connect', methods=['POST'])
def connect():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    link = request.form.get('meeting_link')
    if link:
        # Agar havola ro'yxatda bo'lmasa yoki oxirgisi bo'lmasa, qo'shamiz
        if link not in link_history:
            link_history.insert(0, link)
            # Tarixni 10 tadan oshirmaymiz
            if len(link_history) > 10:
                link_history.pop()
        
        # Brauzerda havolani ochish uchun JavaScript orqali yo'naltirish
        return render_template_string("""
            <script>
                window.open("{{ link }}", "_blank");
                window.location.href = "/dashboard";
            </script>
        """, link=link)
    
    return redirect(url_for('dashboard'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Sensorli monitor va lokal tarmoqdan kirish uchun 0.0.0.0 da ishga tushiramiz
    app.run(host='0.0.0.0', port=5000, debug=True)