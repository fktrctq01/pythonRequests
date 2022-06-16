# mock_run.py
from flask import Flask
from mock.blueprints.basic_endpoints import blueprint as basic_endpoint

app = Flask(__name__)

app.register_blueprint(basic_endpoint)


@app.route('/')
def root():
    return "💡 Mock for orderbook service"


if __name__ == "__main__":
    app.run()
