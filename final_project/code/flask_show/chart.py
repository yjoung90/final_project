from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True,
)

models = {}
def init():
    with open("C:/Users/yjoun/Desktop/datascience/final_project/final_project/code/flask_show/models/classification.plk","rb") as f:
        models["classification"] = pickle.load(f)
init()

@app.route("/")
def index():
    return render_template("index.html")


# API
@app.route("/predict/", methods=["POST"])
def predict():

    classification_list = ["패션의류","패션잡화","화장품/미용","디지털/가전","가구/인테리어","출산/육아", "스포츠/레저", "식품", "생활/건강"]
    model = models["classification"]

    if request.method == 'POST':
        sentence = request.values.get("sentence")

        predict_data = model.predict_proba([sentence])[0]

        result = {"status":200, "result":list(predict_data),
            "category":classification_list}
    else:
        result = {"status":201}

    return jsonify(result)

if __name__ == "__main__":
    app.run()

# $ python chart.py
# 127.0.0.1:5000
