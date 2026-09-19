import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ganti ini pake API key OpenRouter lu
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "sk-or-v1-ISI_API_KEY_LU_DISINI")

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/api/agent', methods=['POST'])
def agent():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Ketik dulu perintahnya bro.'})
    
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY.startswith('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'):
        return jsonify({'response': 'Error: API key belum di-set. Ganti OPENROUTER_API_KEY di app.py atau set environment variable.'})
    
    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'http://localhost:5000',
                'X-Title': 'My AI Agent'
            },
            json={
                'model': 'meta-llama/llama-3.3-70b-instruct:free',
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
        
        if 'error' in result:
            error_msg = result['error'].get('message', 'Unknown error')
            return jsonify({'response': f'OpenRouter Error: {error_msg}'})
        
        ai_response = result['choices'][0]['message']['content']
        
        return jsonify({'response': ai_response})
        
    except requests.exceptions.Timeout:
        return jsonify({'response': 'Error: OpenRouter timeout. Coba lagi.'})
    except requests.exceptions.RequestException as e:
        return jsonify({'response': f'Network Error: {str(e)}'})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
