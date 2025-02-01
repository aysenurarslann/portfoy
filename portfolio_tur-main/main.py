from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 📌 SQLite veritabanını bağlama
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 📌 SQLAlchemy ile veritabanını oluşturma
db = SQLAlchemy(app)

# 📌 Feedback tablosunu oluşturma
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Feedback {self.id}, {self.email}>"

# 📌 Veritabanını oluştur (sadece ilk çalıştırmada)
with app.app_context():
    db.create_all()

# 📌 Ana sayfa
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        button_python = request.form.get('button_python')
        button_discord = request.form.get('button_discord')
        button_db = request.form.get('button_db')
        return render_template('index.html', button_python=button_python, button_discord=button_discord, button_db=button_db)

    feedbacks = Feedback.query.all()  # Veritabanındaki tüm geri bildirimleri çek
    return render_template('index.html', feedbacks=feedbacks)
# 📌 Form verilerini işleme ve veritabanına kaydetme
@app.route('/submit', methods=['POST'])
def form():
    email = request.form['email']
    text = request.form['text']

    # 📌 Yeni geri bildirim ekleme
    new_feedback = Feedback(email=email, text=text)
    db.session.add(new_feedback)
    db.session.commit()

    return render_template('index.html', email=email, text=text)

if __name__ == "__main__":
    app.run(debug=True)
