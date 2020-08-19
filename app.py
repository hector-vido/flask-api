#!/usr/bin/env python3

import sqlite3
from migration import migration
from flask import Flask, jsonify, request, make_response, render_template

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/')
def home():
	content = {}
	childs = []
	with sqlite3.connect('data.db') as db:
		db.row_factory = sqlite3.Row
		cursor = db.cursor()
		cursor.execute("SELECT * FROM contents WHERE id LIKE 'home_%'")
		for row in cursor.fetchall():
			if row['content'] == '[]':
				childs.append(row['id'])
				content[row['id']] = []
				continue
			content[row['id']] = row['content']

		if len(childs) > 0:
			cursor.execute("SELECT * FROM contents_childs WHERE parent IN ('{0}')".format("','".join(childs)))
			for row in cursor.fetchall():
				content[row['parent']].append({'icon' : row['icon'], 'title' : row['title'], 'content' : row['content']})
	return render_template('index.html', c=content)

@app.route('/api/items')
def get_items():
	childs = {}
	items = []
	with sqlite3.connect('data.db') as db:
		db.row_factory = sqlite3.Row
		cursor = db.cursor()
		
		cursor.execute("SELECT * FROM contents_childs")
		for row in cursor.fetchall():
			try:
				childs[row['parent']].append(row['id'])
			except KeyError:
				childs[row['parent']] = []
				childs[row['parent']].append(row['id'])
		
		cursor.execute("SELECT id FROM contents")
		for row in cursor.fetchall():
			if row['id'] in childs:
				items.append({row['id'] : childs[row['id']]})
			else:
				items.append(row['id'])
	return jsonify(items)

@app.route('/api/item/<_id>/subitems')
def get_subitems(_id):
	subitems = []
	with sqlite3.connect('data.db') as db:
		db.row_factory = sqlite3.Row
		cursor = db.cursor()
		cursor.execute("SELECT id FROM contents WHERE id = ?", (_id,))
		row = cursor.fetchone()
		if not row:
			return make_response(jsonify({'message' : 'Item {0} não encontrado'.format(_id)}), 404)

		cursor.execute("SELECT id FROM contents_childs WHERE parent = ?", (_id,))
		for row in cursor.fetchall():
			subitems.append(row['id'])
	return jsonify(subitems)

@app.route('/api/item/<_id>', methods=['PUT'])
def items(_id):
	if request.method == 'PUT':
		if _id == 'home_m1_boxes':
			return make_response(jsonify({'message' : 'É possível alterar somente os subitens "home_m1_boxes"'}), 403)

	try:
		data = request.json
	except:
		return make_response(jsonify({'message' : 'Não foi possível converter os dados enviados em JSON', 'sent' : request.get_data()}), 400)
	
	if 'content' not in data:
		return make_response(jsonify({'message' : 'Propriedade "content" não encontrada', 'sent' : request.get_data()}), 400)
	
	with sqlite3.connect('data.db') as db:
		db.row_factory = sqlite3.Row
		cursor = db.cursor()
		cursor.execute("SELECT * FROM contents WHERE id = ?", (_id,))
		row = cursor.fetchone()
		if not row:
			return make_response(jsonify({'message' : 'Item {0} não encontrado'.format(_id)}), 404)
		cursor.execute("UPDATE contents SET content = ? WHERE id = ?", (data['content'], _id))
	return jsonify({'message' : 'Item {0} atualizado!'.format(_id)})

@app.route('/api/item/<_parent>/subitem', methods=['POST'])
def post_subitem(_parent):
	try:
		data = request.json
	except:
		return make_response(jsonify({'message' : 'Não foi possível converter os dados enviados em JSON', 'sent' : request.get_data()}), 400)
	
	for key in ['id', 'title', 'icon', 'content']:
		if key not in data:
			return make_response(jsonify({'message' : 'Todas as chaves id, title, icon e content são obrigatórias', 'sent' : request.get_data()}), 400)
	
	with sqlite3.connect('data.db') as db:
		db.row_factory = sqlite3.Row
		cursor = db.cursor()
		
		cursor.execute("SELECT id FROM contents WHERE id = ?", (_parent,))
		row = cursor.fetchone()
		if not row:
			return make_response(jsonify({'message' : 'Item {0} não encontrado'.format(_parent)}), 404)
		
		cursor.execute("SELECT parent, id FROM contents_childs WHERE parent = ?", (_parent,))
		rows = cursor.fetchall()
		if len(rows) >= 3:
			return make_response(jsonify({'message' : 'O item {0} pode possuir apenas 3 subitens'.format(_parent)}), 409)
		for row in rows:
			if row['id'] == data['id']:
				return make_response(jsonify({'message' : 'Subitem {0} de {1} já existe'.format(data['id'], _parent)}), 409)

		cursor.execute("INSERT INTO contents_childs (parent, id, title, icon, content) VALUES (?, ?, ?, ?, ?)", (_parent, data['id'], data['title'], data['icon'], data['content']))
	return jsonify({'message' : 'Item {0} cadastrado com sucesso!'.format(data['id'])})

@app.route('/api/item/<_parent>/<_id>', methods=['PUT'])
def put_subitem(_parent, _id):
	try:
		data = request.json
	except:
		return make_response(jsonify({'message' : 'Não foi possível converter os dados enviados em JSON', 'sent' : request.get_data()}), 400)
	
	for key in ['id', 'title', 'icon', 'content']:
		if key in data:
			break
	else:
		return make_response(jsonify({'message' : 'Nenhuma das chaves id, title, icon ou content foram enviadas', 'sent' : request.get_data()}), 400)
	
	with sqlite3.connect('data.db') as db:
		db.row_factory = sqlite3.Row
		cursor = db.cursor()
		cursor.execute("SELECT * FROM contents_childs WHERE parent = ? AND id = ?", (_parent, _id,))
		row = cursor.fetchone()
		if not row:
			return make_response(jsonify({'message' : 'Subitem {0} de {1} não encontrado'.format(_id, _parent)}), 404)
		for key in ['id', 'title', 'icon', 'content']:
			if key not in data:
				data[key] = row[key]
		cursor.execute("UPDATE contents_childs SET id = ?, title = ?, icon = ?, content = ? WHERE parent = ? AND id = ?", (data['id'], data['title'], data['icon'], data['content'], _parent, _id))
	return jsonify({'message' : 'Item {0} de {1} atualizado!'.format(_id, _parent)})

@app.route('/api/item/<_parent>/<_id>', methods=['DELETE'])
def delete_subitem(_parent, _id):
	with sqlite3.connect('data.db') as db:
		db.row_factory = sqlite3.Row
		cursor = db.cursor()
		cursor.execute("SELECT parent, id FROM contents_childs WHERE parent = ? AND id = ?", (_parent, _id,))
		row = cursor.fetchone()
		if not row:
			return make_response(jsonify({'message' : 'Subitem {0} de {1} não encontrado'.format(_id, _parent)}), 404)
		cursor.execute("DELETE FROM contents_childs WHERE parent = ? AND id = ?", (_parent, _id))
	return jsonify({'message' : 'Item {0} de {1} removido!'.format(_id, _parent)})

@app.route('/feature')
def feature():
	return render_template('feature.html')

@app.route('/pricing')
def price():
	return render_template('pricing.html')

@app.route('/blog')
def blog():
	return render_template('blog.html')

@app.route('/blog-details')
def blog_details():
	return render_template('blog-details.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/signup')
def signup():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
