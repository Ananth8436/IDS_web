from flask import Flask, render_template, request, redirect, url_for, flash
import pywhatkit as kit
from datetime import datetime

app = Flask(__name__)
app.secret_key = "1234"

service_requests = []
service_links = {
    "Network Monitoring Tool": "https://drive.google.com/file/d/1-9A1khEj33QqBxNS8iU44k5nSqwWnxnr/view?usp=sharing",
    "Intrusion Detection System (IDS)": "https://drive.google.com/file/d/1CkpKG0Ccl48PYxvT-186gAddjL-2oc1v/view?usp=sharing",
    "Firewall Configuration Tool": "https://drive.google.com/file/d/1CkpKG0Ccl48PYxvT-186gAddjL-2oc1v/view?usp=sharing",
    "File Tracking": "https://www.virustotal.com/gui/home/url",
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == "host":
        return redirect(url_for('host_dashboard'))
    elif username == "manager":
        return redirect(url_for('manager_dashboard'))
    else:
        return render_template('dashboard.html', username=username)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/request_service')
def request_service():
    return render_template('service_request.html')

@app.route('/submit_request', methods=['POST'])
def submit_request():
    org_name = request.form['org_name']
    cust_name = request.form['cust_name']
    role = request.form['role']
    service_needed = request.form['service_needed']
    problem_desc = request.form['problem_desc']
    phone = request.form['phone']

    service_requests.append({
        'org_name': org_name,
        'cust_name': cust_name,
        'role': role,
        'service_needed': service_needed,
        'problem_desc': problem_desc,
        'phone': phone,
        'status': 'Pending',
        'assigned_software': None
    })

    return render_template('submission_success.html')

@app.route('/host_dashboard')
def host_dashboard():
    return render_template('host_dashboard.html', service_requests=service_requests)

@app.route('/update_status', methods=['POST'])
def update_status():
    org_name = request.form['org_name']
    action = request.form['action']

    for req in service_requests:
        if req['org_name'] == org_name:
            req['status'] = 'Accepted' if action == 'accept' else 'Rejected'
            break

    return redirect(url_for('host_dashboard'))

@app.route('/manager_dashboard')
def manager_dashboard():
    return render_template('manager_dashboard.html', service_requests=service_requests)

@app.route('/assign_software', methods=['POST'])
def assign_software():
    org_name = request.form['org_name']
    software = request.form['software']

    drive_link = service_links.get(software, "No Link Available")

    for req in service_requests:
        if req['org_name'] == org_name and req['status'] == 'Accepted':
            req['assigned_software'] = software
            req['drive_link'] = drive_link
            req['status'] = 'Software Assigned'

            send_whatsapp_message(req['phone'], org_name, software, drive_link)

            flash(f"Software assigned and WhatsApp message sent to {req['phone']}", 'success')
            break

    return redirect(url_for('manager_dashboard'))


def send_whatsapp_message(client_number, org_name=None, software=None, drive_link=None):
    # Remove any spaces and ensure the number is clean
    client_number = client_number.strip().replace(" ", "")

    # Add +91 only if not already present
    if not client_number.startswith("+"):
        client_number = "+91" + client_number

    message = f"Hello, {org_name}! Software '{software}' has been assigned to you.\nDownload Link: {drive_link}\nPlease check your email for installation steps."

    try:
        kit.sendwhatmsg_instantly(
            client_number,
            message,
            wait_time=30,
            tab_close=True,
            close_time=120
        )
        print(f"WhatsApp message sent to {client_number}")
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")





if __name__ == '__main__':
    app.run(debug=True)
