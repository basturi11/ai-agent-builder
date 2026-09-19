import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "ISI_API_KEY_LU_DISINI")

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/api/agent', methods=['POST'])
def agent():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Ketik dulu perintahnya bro.'})
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4o-mini',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'Kamu adalah AI Agent yang bisa bikin website dan aplikasi. Kalau user minta bikin sesuatu, langsung kasih kode lengkap HTML/CSS/JS yang bisa langsung dipakai. Jangan banyak tanya, langsung kerjakan. Format kode pakai markdown code block.'
                    },
                    {
                        'role': 'user',
                        'content': user_message
                    }
                ],
                'max_tokens': 4000
            },
            timeout=60
        )
        
        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}. Cek API key lu.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
