from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')  # Store key in environment variable

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '').strip()

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': f"Build a website structure and content for: {prompt}"}],
            max_tokens=1000
        )
        content = response['choices'][0]['message']['content']

        # For simplicity, structure response into a generic Home and About page
        pages = [
            {'title': 'Home', 'content': f'<h1>Home</h1><p>{content}</p>'},
            {'title': 'About', 'content': '<h2>About</h2><p>This website was generated with AI.</p>'}
        ]

        return jsonify({'pages': pages})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
