from flask import Flask, render_template, request, redirect, session, url_for, flash
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'argi_smart_secret_key'

ADMIN_PHONE = '9035033443'
ADMIN_OTP = '123456'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATA_FILE = 'data.json'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'photos': [], 'videos': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def home():
    data = load_data()
    return render_template('index.html', photos=data['photos'], videos=data['videos'])

@app.route('/purpose')
def purpose():
    return render_template('purpose.html')

@app.route('/program')
def program():
    return render_template('program.html')

@app.route('/partner')
def partner():
    return render_template('partner.html')

@app.route('/tourism')
def tourism():
    return render_template('tourism.html')

@app.route('/festival')
def festival():
    return render_template('festival.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Validate message word count
        word_count = len(message.split())
        if word_count > 30:
            flash('Message must be 30 words or less!', 'error')
            return redirect('/#contact')
        
        # Save message to file
        data = load_data()
        if 'messages' not in data:
            data['messages'] = []
        
        data['messages'].append({
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        save_data(data)
        
        flash('Message sent successfully!', 'success')
        return redirect('/#contact')
    
    return render_template('contact.html')

@app.route('/photos')
def photos():
    data = load_data()
    return render_template('photos.html', photos=data['photos'])

@app.route('/videos')
def videos():
    data = load_data()
    return render_template('videos.html', videos=data['videos'])

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        otp = request.form.get('otp')
        if phone == ADMIN_PHONE and otp == ADMIN_OTP:
            session['admin'] = True
            return redirect('/admin/dashboard')
        else:
            flash('Invalid phone number or OTP!', 'error')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin/login')
    data = load_data()
    messages = data.get('messages', [])
    return render_template('admin_dashboard.html', photos=data['photos'], videos=data['videos'], messages=messages)

@app.route('/admin/add_photo', methods=['POST'])
def add_photo():
    if not session.get('admin'):
        return redirect('/admin/login')
    
    if 'file' not in request.files:
        return redirect('/admin/dashboard')
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect('/admin/dashboard')
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    data = load_data()
    photo = {
        'url': f'/static/uploads/{filename}',
        'title': request.form.get('title'),
        'description': request.form.get('description')
    }
    data['photos'].append(photo)
    save_data(data)
    return redirect('/admin/dashboard')

@app.route('/admin/add_video', methods=['POST'])
def add_video():
    if not session.get('admin'):
        return redirect('/admin/login')
    
    if 'file' not in request.files:
        return redirect('/admin/dashboard')
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect('/admin/dashboard')
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    data = load_data()
    video = {
        'url': f'/static/uploads/{filename}',
        'title': request.form.get('title'),
        'description': request.form.get('description')
    }
    data['videos'].append(video)
    save_data(data)
    return redirect('/admin/dashboard')

@app.route('/admin/delete_photo/<int:index>')
def delete_photo(index):
    if not session.get('admin'):
        return redirect('/admin/login')
    data = load_data()
    if 0 <= index < len(data['photos']):
        data['photos'].pop(index)
        save_data(data)
    return redirect('/admin/dashboard')

@app.route('/admin/delete_video/<int:index>')
def delete_video(index):
    if not session.get('admin'):
        return redirect('/admin/login')
    data = load_data()
    if 0 <= index < len(data['videos']):
        data['videos'].pop(index)
        save_data(data)
    return redirect('/admin/dashboard')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=8001)
