from flask import Flask, render_template, request, jsonify

from chat import get_response

from flask_cors import CORS 



app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.get("/")
def index_get():
    text = request.get_json().get("message")
    #TODO: check if text is valid
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

    return render_template('base.html')

# @app.post('/predict')
# def predict():
    
if __name__ == '__main__':
    app.run(debug = True),


from flask import Flask, render_template, request, jsonify
from chat import get_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# GET / → serves the HTML page
@app.get("/")
def index():
    return render_template('base.html')

# POST /predict → handles chat requests
@app.post("/predict")
def predict():
    data = request.get_json()
    text = data.get("message") if data else None

    if not text:
        return jsonify({"error": "No message provided"}), 400

    response = get_response(text)
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(debug=True)
