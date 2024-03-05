import string
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api", methods = ['GET'])

def returnascii():
    d = {}
    inputchr = str(request.args['query'])
    answer = str(ord(inputchr))
    d['output'] = answer
    return d
    
@app.route('/api/data', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        # Assuming the client sends JSON data in the request body
        try:
            data = request.get_json()
            # Process the received data
            result = process_data(data)
            return jsonify({'success': True, 'result': result})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    else:
        return jsonify({'success': False, 'error': 'Only POST requests are allowed'})

def process_data(data):
    # Your logic to process the received data goes here
    # For example, you might store it in a database or perform some computation
    return {'processed_data': data}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)