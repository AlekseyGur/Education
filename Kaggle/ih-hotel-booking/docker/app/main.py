from flask import Flask, jsonify, abort, make_response, request
from flask import render_template
from waitress import serve
from model import Model  # предсказания модели

model = Model()
reqired_params = model.params_reqired()  # обязательные параметры для предскзаний

app = Flask(__name__)
api_base_url = '/api/v1.0'

@app.route('/', methods=['GET'])
def get_index():
    return render_template("index.html",
        api_base_url = api_base_url,
        models = [(d['date_time'], d['accuracy']) for d in model.get_list()],
        params = [(i, v['type'], v['descr']) for i, v in reqired_params.items()]
    )

@app.route(api_base_url + '/predict', methods=['GET'])  # предсказние по модели
def predict():
    get_params = {}
    for param in reqired_params:
        val = request.args.get(param)
        if not val:
            abort(400)

        get_params.update({param: val})

    res = model.predict(get_params)  # очистка значений проходит внутри функции

    res['status'] = 1
    if 'error' in res:
        res['status'] = 0

    return jsonify(res)

@app.route(api_base_url + '/create', methods=['GET'])  # пересоздание модели
def create():
    res = model.create()

    res['status'] = 1
    if 'error' in res:
        res['status'] = 0

    return jsonify(res)

@app.errorhandler(400)
def not_found(error):
    print(error)
    return make_response(jsonify({'error': 'Not enough GET params'}), 400)

if __name__ == '__main__':
    # serve(app, host='127.0.0.1', port=5000)
    serve(app, host='0.0.0.0', port=5000)
    # app.run(debug=True, host='0.0.0.0', port=5000)
