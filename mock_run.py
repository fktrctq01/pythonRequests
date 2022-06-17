# mock_run.py
from flask import Flask, redirect
from mock.blueprints.basic_endpoints import blueprint as basic_endpoint
from mock.blueprints.documented_endpoints import blueprint as documented_endpoint


app = Flask(__name__)

app.register_blueprint(basic_endpoint)
app.register_blueprint(documented_endpoint)


@app.route('/')
def root():
    return redirect("/mock")


if __name__ == "__main__":
    app.run()
