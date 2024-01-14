#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    
    if not animal:
        response_body = '<h1>Animal not found</h1>'
        response = make_response(response_body, 404)
        return response
    
    response_body = f'''
        <h1>{animal.name}</h1>
        <h2>{animal.species}</h2>
        <h3>{animal.enclosure.environment}</h3>
        <h3>{animal.zookeeper.name}</h3>
    '''
    response = make_response(response_body, 200)
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    
    if not zookeeper:
        response_body = '<h1>Zookeeper not found</h1>'
        response = make_response(response_body, 404)
        return response
    
    response_body = f'''
        <h1>{zookeeper.name}</h1>
        <h2>{zookeeper.birthday}</h2>
    '''
    animals = [animal for animal in zookeeper.animal]
    
    if not animals:
        response_body += f'<h2>Has no animals<h2>'
        
    else:
        for animal in animals:
            response_body += f'<h2>{Animal.id}<h2>'

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    environment = Enclosure.query.filter(Enclosure.id == id).first()
    
    if not environment:
        response_body = '<h1>Enclosure not found</h1>'
        response = make_response(response_body, 404)
        return response
    
    response_body = f'''
        <h1>{environment.environment}</h1>
        <h2>{environment.open_to_visitors}</h2>
    '''
    animals = [animal for animal in environment.animal]
    
    if not animals:
        response_body += f'<h2>Has no animals<h2>'
        
    else:
        for animal in animals:
            response_body += f'<h2>{Animal.id}<h2>'
            
    response = make_response(response_body, 200)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
