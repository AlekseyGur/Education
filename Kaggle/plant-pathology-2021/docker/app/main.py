from os import makedirs, remove
from os.path import exists, splitext, join as path_join
from flask import Flask, jsonify, abort, make_response, request, redirect, url_for
from flask import render_template
from waitress import serve
from lib.model import Model  # предсказания модели
from lib.image import validate_image
from lib.tools import randomword

if not exists('models/'):  # папка с моделями. Если её нет, то создайте хотя бы одну модель!
    makedirs('models/')

models = Model().get_list()
assert len(models) > 0, 'Нет ни одной модели! Сначала создайте хотя бы одну модель.' \
                   ' По соглашению с Kaggle.com публиковать модель нельзя, поэтому' \
                   ' придётся создать модель самостоятельно, используя метод fit_check_save,' \
                   ' предварительно загрузив изображения, по которым делается обучение модели.'

app = Flask(__name__)
api_base_url = '/api/v1.0'

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 15  # загружаемые на сервер файлы не должны превышать лимит
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg']  # ограничение на расширения загружаемых файлов


@app.route('/', methods=['GET'])
def get_index():
    return render_template("index.html",
        api_base_url = api_base_url,
        models = [(d['date'], d['accuracy'], d['predicted_amount']) for d in models]
    )

@app.route(api_base_url + '/predict', methods=['GET', 'POST'])  # предсказание по модели
def predict():
    uploaded_file = request.files['file']
    file_path = uploaded_file.filename
    if file_path != '':
        file_ext = splitext(file_path)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
           file_ext != validate_image(uploaded_file.stream):
            abort(400)

        res = []
        try:
            filename_to_save = f'{randomword(30)}{file_ext}'
            path_to_save = path_join('/tmp', filename_to_save)
            uploaded_file.save(path_to_save)

            model = Model(
                VERBOSE=False,  # подробный вовод процесса работы скрипта
                CSV_PATH=path_to_save,  # CSV файл с данными
                ONLY_CPU=True,  # Использовать только CPU.
                MEMORY_LIMIT=None,  # Ограничение на использование ОЗУ в GPU (в МБ).
                MEMORY_GROWTH=False,  # В положении "True" заставляет tensorflow занимать ОЗУ в GPU по мере необходимости.
            )
            res = model.predict_file(path_to_save)

            if exists(path_to_save):
                remove(path_to_save)

        except Exception as e:
            res['error'] = 1

        res['status'] = 0 if 'error' in res else 1
        return jsonify(res)

    return abort(400)

@app.errorhandler(400)
def not_found(error):
    print(error)
    return make_response(jsonify({'error': 'Error 400'}), 400)

if __name__ == '__main__':
    # serve(app, host='127.0.0.1', port=5000)
    serve(app, host='0.0.0.0', port=5000)
    # app.run(debug=True, host='0.0.0.0', port=5000)
