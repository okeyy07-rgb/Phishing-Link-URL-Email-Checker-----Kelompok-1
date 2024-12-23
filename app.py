from flask import Flask, request, jsonify, render_template
import requests
import validators
import base64

app = Flask(__name__)

API_KEY = '7534c65ca1b5107b0294f82a81bc6fda602853aadfeadad0814e92a5455c2f07'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_link', methods=['POST'])
def check_link():
    data = request.get_json()
    url = data['url']
    
    # Validasi URL
    if not validators.url(url):
        return jsonify({'error': 'Invalid URL'}), 400

    # Encode URL menjadi base64 (sesuai dengan persyaratan VirusTotal API)
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip('=')
    
    # Logika pemeriksaan phishing menggunakan VirusTotal API
    headers = {
        'x-apikey': API_KEY
    }
    response = requests.get(f'https://www.virustotal.com/api/v3/urls/{url_id}', headers=headers)
    result = response.json()
    print(result)  # Tambahkan log untuk memeriksa respons API
    
    # Memeriksa hasil dari API
    if 'data' in result and result['data']['attributes']['last_analysis_stats']['malicious'] > 0:
        print("Link berpotensi phishing")  # Log tambahan
        return jsonify({'safe': False, 'message': 'Link berpotensi phishing'})
    else:
        print("Link aman")  # Log tambahan
        return jsonify({'safe': True, 'message': 'Link aman'})

if __name__ == '__main__':
    app.run(debug=True)
