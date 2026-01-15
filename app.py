from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.engine import Database
from db.schema import Column

app = Flask(__name__)
db = Database()

# Initialize with users table if it doesn't exist
try:
    db.create_table('users', [
        Column('id', 'INT', primary_key=True),
        Column('name', 'TEXT'),
        Column('email', 'TEXT', unique=True)
    ])
except ValueError:
    pass  # Table already exists

@app.route('/')
def home():
    return jsonify({
        'message': 'Pesapal RDBMS API',
        'endpoints': {
            'GET /users': 'List all users',
            'POST /users': 'Create user',
            'PUT /users/<id>': 'Update user',
            'DELETE /users/<id>': 'Delete user'
        }
    })

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = db.select_all('users')
        return jsonify({'users': users})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        db.insert('users', [data['id'], data['name'], data['email']])
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        users = db.select_where('users', 'id', user_id)
        if not users:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'user': users[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        if 'name' in data:
            db.update('users', 'name', data['name'], 'id', user_id)
        if 'email' in data:
            db.update('users', 'email', data['email'], 'id', user_id)
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        db.delete('users', 'id', user_id)
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)