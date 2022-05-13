from flask import Flask, jsonify, abort, make_response, request
from waitress import serve
from tools import clear_pos_int, clear_bool, clear_text, validate_clear


app = Flask(__name__)

elements = {
    1: {  # - это первичный ключ
        'title': u'Выучить Flask',
        'description': u'До конца разобраться с работой фреймвокра Flask',
        'done': False
    },
    2: {
        'title': u'Упаковать в Docker',
        'description': u'Поместить приложение на Flask в Docker контейнер',
        'done': False
    }
}

api_base_url = '/api/v1.0/elements'

@app.route('/', methods=['GET'])
def get_index():
    return f'''<h1>Простейший REST API</h1>
    <table>
        <tr>
            <th>HTTP Method</th>
            <th>URI</th>
            <th>Action</th>
        </tr>
        <tr>
            <td>GET</td>
            <td>{api_base_url}</td>
            <td>Retrieve list of elements</td>
        </tr>
        <tr>
            <td>GET</td>
            <td>{api_base_url}/[element_id]</td>
            <td>Retrieve an element</td>
        </tr>
        <tr>
            <td>POST</td>
            <td>{api_base_url}</td>
            <td>Create a new element</td>
        </tr>
        <tr>
            <td>PUT</td>
            <td>{api_base_url}/[element_id]</td>
            <td>Update an existing element</td>
        </tr>
        <tr>
            <td>DELETE</td>
            <td>{api_base_url}/[element_id]</td>
            <td>Delete an element</td>
        </tr>
    </table>

    <a href="{api_base_url}">Список дел</a><br>
    <a href="{api_base_url}/1">Первое дело</a>
    <hr>
    <h2>Тест системы</h2>
    {'Статус валидаторов: ОК' if validate_clear() else 'Не работает валидатор'}
    '''

@app.route(api_base_url, methods=['GET'])
def get_elements():
    return jsonify({'elements': elements})

@app.route(api_base_url + '/<int:element_id>', methods=['GET'])
def get_element(element_id):
    element_id = clear_pos_int(element_id)
    if element_id not in elements:
        abort(404)
    return jsonify({'element': elements[element_id]})

@app.route(api_base_url, methods=['POST'])
def create_element():
    # curl -i -H "Content-Type: application/json" -X POST -d \
    #               '{"title":"Read"}' /api/v1.0/elements
    if not request.json or not 'title' in request.json:
        abort(400)

    id = max(elements) + 1
    elements[id] = {
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'done': False
    }
    return jsonify({'id': id}), 201  # 201 - Created

@app.route(api_base_url + '/<int:element_id>', methods=['PUT'])
def update_element(element_id):
    element_id = clear_pos_int(element_id)
    if element_id not in elements:
        abort(404)
    if not request.json:
        abort(400)
    # if 'title' in request.json and type(request.json['title']) is not unicode:
    #     abort(400)
    # if 'description' in request.json and type(request.json['description']) is not unicode:
    #     abort(400)
    # if 'done' in request.json and type(request.json['done']) is not bool:
    #     abort(400)

    title = clear_text(request.json.get('title'))
    description = clear_text(request.json.get('description'))
    done = clear_text(request.json.get('done'))

    el = elements[element_id]
    el['title'] = title or el['title']
    el['description'] = description or el['description']
    el['done'] = done or el['description']

    return jsonify({'element': el})

@app.route(api_base_url + '/<int:element_id>', methods=['DELETE'])
def delete_element(element_id):
    element_id = clear_pos_int(element_id)
    if element_id not in elements:
        abort(404)

    del elements[element_id]
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=5000)
    # serve(app, host='0.0.0.0', port=5000)
    # app.run(debug=True, host='0.0.0.0', port=5000)
