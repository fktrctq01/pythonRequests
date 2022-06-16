# mock_run.py
from flask import Flask
from mock.blueprints.basic_endpoints import blueprint as basic_endpoint
from mock.blueprints.documented_endpoints import blueprint as documented_endpoint


app = Flask(__name__)

app.register_blueprint(basic_endpoint)
app.register_blueprint(documented_endpoint)


@app.route('/')
def root():
    return """
    <h1>Mock for orderbook service</h1>
    💡 <a href="http://localhost:5000/mock/">documentation</a><p>
    🗑 <a href="http://localhost:5000/mock/api/order/clean">[get] /api/order/clean</a><p>
    🗳 <a href="http://localhost:5000/mock/api/marketdata">[get] /api/marketdata</a>
    """


if __name__ == "__main__":
    app.run()
