from flask import Flask, render_template, request, redirect, url_for, flash
import os
import threading
import time
import urllib.error
import urllib.request
import webbrowser

app = Flask(__name__)
app.secret_key = 'saitama_regional_help_secret_key'

# 1. ログイン選択画面（トップページ）
@app.route('/')
def index():
    return render_template('index.html')

# はじめての方へ（使い方ガイド）
@app.route('/guide')
def guide():
    return render_template('guide.html')

# よくある質問（FAQ）
@app.route('/faq')
def faq():
    return render_template('faq.html')

# 市民新規登録画面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        password = request.form.get('password', '')
        
        # パスワード文字数チェック（8文字未満はエラー）
        if len(password) < 8:
            flash('パスワードは8文字以上で入力してください。', 'danger')
            return render_template('register.html')
            
        # 登録処理（成功時はログイン画面へ）
        flash('アカウントの作成が完了しました。ログインしてください。', 'success')
        return redirect(url_for('login_citizen'))
        
    return render_template('register.html')

# 2. 市民ログイン
@app.route('/login/citizen', methods=['GET', 'POST'])
def login_citizen():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # エラー例のテスト用: emailに'error'が含まれる場合は6のエラー例を表示
        if 'error' in email:
            return render_template('login_citizen.html', error="メールアドレスまたはパスワードが正しくありません。")
        return redirect(url_for('citizen_mypage'))
    return render_template('login_citizen.html')

# 3. 行政職員ログイン
@app.route('/login/staff', methods=['GET', 'POST'])
def login_staff():
    if request.method == 'POST':
        return redirect(url_for('staff_dashboard'))
    return render_template('login_staff.html')

# 管理者ログイン
@app.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        return redirect(url_for('admin_portal'))
    return render_template('login_admin.html')

# 4. 市民マイページ
@app.route('/citizen/mypage')
def citizen_mypage():
    return render_template('citizen_mypage.html')

# 市民新規報告画面
@app.route('/citizen/report', methods=['GET', 'POST'])
def citizen_report():
    if request.method == 'POST':
        flash('困りごとの報告を送信しました。AIによる分類・緊急度判定を開始します。', 'success')
        return redirect(url_for('citizen_mypage'))
    return render_template('citizen_report.html')

# 5. 行政職員ダッシュボード
@app.route('/staff/dashboard')
def staff_dashboard():
    return render_template('staff_dashboard.html')

# 管理者ポータル
@app.route('/admin/portal')
def admin_portal():
    return render_template('admin_portal.html')

if __name__ == '__main__':
    def open_browser_when_ready():
        url = 'http://127.0.0.1:5000'
        for _ in range(50):
            try:
                with urllib.request.urlopen(url, timeout=1):
                    pass
            except (urllib.error.URLError, OSError):
                time.sleep(0.2)
            else:
                webbrowser.open(url)
                return

    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        threading.Thread(target=open_browser_when_ready, daemon=True).start()
    app.run(debug=True, port=5000)
