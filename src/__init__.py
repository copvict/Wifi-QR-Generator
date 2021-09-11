from flask import Flask, redirect, url_for, render_template, request, send_file, flash, get_flashed_messages
from io  import BytesIO
import pyqrcode
import base64

app = Flask(__name__)
app.secret_key = "secret"

@app.route('/', methods = ['GET', 'POST'])
def generate_qr():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        form_ssid = request.form['ssid']
        form_auth = request.form['network']
        form_pass = request.form['password']
        form_hide = request.form['hidden']

        if form_ssid == "":
            flash("SSID is required.", 'form_error')
            flash("<script>document.getElementById('ssid').classList.add('is-error');</script>", 'script')
            return render_template('index.html')
        else:
            if len(form_ssid) > 32:
                flash("SSID can't be of more than 32 characters.", 'form_error')
                flash("<script>document.getElementById('ssid').classList.add('is-warning');</script>", 'script')
                return render_template('index.html')

        if form_auth == "WEP" or form_auth == "WPA/WPA2":
            flash("<script>document.getElementById('ssid').classList.add('is-success'); document.getElementById('ssid').value='" + form_ssid + "';</script>", 'script')
            flash("<script>document.getElementById('auth').classList.add('is-warning');</script>", 'script')
            if form_auth == "WEP":
                flash("<script>document.getElementById('authop').selectedIndex="+ str(1) +"</script>", 'script')
                if len(form_pass) < 5:
                    flash("Password for WEP encryption can't be of less than 5 characters.", 'form_error')
                    flash("Minimum of 5 characters for 40-bit, 13 for 128-bit WEP encryption.", 'warning')
                    flash("Use a mix of alphabets, symbols and number for atleast 14 charecters.", 'recommend')
                    flash("<script>document.getElementById('pass').classList.add('is-error');</script>", 'script')
                    return render_template('index.html')
                if len(form_pass) > 16:
                    flash("Password for WEP encryption can't be of more than 16 characters.", 'form_error')
                    flash("<script>document.getElementById('pass').classList.add('is-error');</script>", 'script')
                    return render_template('index.html')
            else:
                flash("<script>document.getElementById('authop').selectedIndex="+ str(2) +"</script>", 'script')
                if len(form_pass) < 8:
                    flash("Password for WPA/WPA2 encryption can't be of less than 8 characters.", 'form_error')
                    flash("Password with less than 14 characters are most vulnerable to brute force attacks.", "warning")
                    flash("Use a mix of alphabets, symbols and number for atleast 14 charecters.", 'recommend')
                    flash("<script>document.getElementById('pass').classList.add('is-error');</script>", 'script')
                    return render_template('index.html')
                if len(form_pass) > 63:
                    flash("Password for WPA/WPA2 encryption can't be of more than 63 characters.", 'form_error')
                    flash("<script>document.getElementById('pass').classList.add('is-error');</script>", 'script')
                    return render_template('index.html')

        if form_hide != 'True':
            wifi = pyqrcode.create('WIFI:T:' + form_auth + ';S:' + form_ssid + ';P:' + form_pass + ';;', version=8)
        else:
            wifi = pyqrcode.create('WIFI:T:' + form_auth + ';S:' + form_ssid + ';P:' + form_pass + ';H:true;;', version=8)
        return render_template('index.html', img = wifi.png_as_base64_str(scale=5))

@app.route('/qr/download/', methods = ['POST','GET'])
def download_qr():
    if request.method == 'POST':
        qr = request.form['qr64']
        qr_file = BytesIO(base64.b64decode(qr))
        return send_file(qr_file, attachment_filename='generated_qr.png', as_attachment=True)
    return redirect(url_for('generate_qr'))

@app.errorhandler(404)
def error_404(e):
    return redirect(url_for('generate_qr'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)