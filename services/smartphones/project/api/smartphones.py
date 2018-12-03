# services/users/project/api/smartphones.py
from flask import Blueprint, jsonify, request, render_template
# from sqlalchemy import update
from sqlalchemy import exc
# from sqlalchemy.sql import func
from project.api.models import Smartphone, Persona
from project import db

smartphones_blueprint = Blueprint("smartphones",
                                  __name__,
                                  template_folder='./templates')


@smartphones_blueprint.route('/smartphones/jinga/index',
                             methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        brand = request.form['brand']
        price = request.form['price']
        color = request.form['color']
        quantity = request.form['quantity']
        if request.form['propietario']:
            propietario = request.form['propietario']
            db.session.add(Smartphone(name=name, brand=brand, price=price,
                                      color=color, quantity=quantity,
                                      propietario=propietario))
        else:
            db.session.add(Smartphone(name=name, brand=brand, price=price,
                                      color=color, quantity=quantity))
            db.session.commit()
    smartphones = Smartphone.query.all()
    personas = Persona.query.all()
    return render_template('index.html', smartphones=smartphones,
                           personas=personas)


@smartphones_blueprint.route('/smartphones/jinga/persona',
                             methods=['GET', 'POST'])
def persona_view():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        age = request.form['age']
        gender = request.form['gender']
        db.session.add(Persona(name=name, lastname=lastname, age=age,
                               gender=gender))
        db.session.commit()
    personas = Persona.query.all()
    return render_template('addPersona.html', personas=personas)


@smartphones_blueprint.route('/smartphones/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@smartphones_blueprint.route('/smartphones', methods=['POST'])
def add_smartphones():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'carga invalida.'
    }
    if not post_data:
        return jsonify(response_object), 400
    name = post_data.get('name')
    brand = post_data.get('brand')
    price = post_data.get('price')
    color = post_data.get('color')
    quantity = post_data.get('quantity')
    propietario = post_data.get('propietario')
    try:
        smartphone = Smartphone.query.filter_by(name=name, brand=brand).first()
        if not smartphone:
            if propietario:
                db.session.add(Smartphone(name=name, brand=brand,
                                          price=price, color=color,
                                          quantity=quantity,
                                          propietario=propietario))
                response_object['message'] = f'{name}, marca {brand} a sido '\
                                             'agregado con propietario!!'
            else:
                db.session.add(Smartphone(name=name, brand=brand,
                                          price=price, color=color,
                                          quantity=quantity))
                response_object['message'] = f'{name}, marca {brand} a sido '\
                                             'agregado sin propietario!!'
            db.session.commit()
            response_object['status'] = 'success'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Lo siento. '\
                'Este smartphone ya existe.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


"""@smartphones_blueprint.route('/smartphones/update', methods=['POST'])
def update_smartphones():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'carga invalida.'
    }
    if not post_data:
        return jsonify(response_object), 400
    idd = post_data.get('id')
    name = post_data.get('name')
    brand = post_data.get('brand')
    price = post_data.get('price')
    color = post_data.get('color')
    quantity = post_data.get('quantity')
    try:
        smartphone = Smartphone.query.filter_by(id=int(idd)).first()
        if not smartphone:
            response_object['message'] = f'Lo siento. '\
                'Este smartphone no existe.'
            return jsonify(response_object), 400
        Smartphone.update().where(Smartphone.c.id == smartphone.id).\
            values(name=name, brand=brand, price=price,
                   color=color, quantity=quantity,
                   modification_date=func.now())
        response_object['status'] = 'success'
        response_object['message'] = f'{name}, marca '\
            '{brand} a sido modificado!!'
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@smartphones_blueprint.route('/smartphones/<int:smartphone_id>/delete',
                             methods=['GET'])
def delete_single_smartphone(smartphone_id):
    response_object = {
        'status': 'fail',
        'message': 'el smartphone no existe'
    }
    try:
        smartphone = Smartphone.query.filter_by(id=int(smartphone_id)).delete()
        if not smartphone:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'message': 'el smartphone fue eliminado.'
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
"""


@smartphones_blueprint.route('/smartphones/<smartphone_id>',
                             methods=['GET'])
def get_single_smartphone(smartphone_id):
    """Obtener detalles de smartphone unico"""
    response_object = {
        'status': 'fail',
        'message': 'el smartphone no existe'
    }
    try:
        smartphone = Smartphone.query.filter_by(id=int(smartphone_id)).first()
        if not smartphone:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': smartphone.id,
                    'name': smartphone.name,
                    'brand': smartphone.brand,
                    'price': smartphone.price,
                    'color': smartphone.color,
                    'quantity': smartphone.quantity,
                    'active': smartphone.active
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@smartphones_blueprint.route('/smartphones/persona/<int:persona_id>',
                             methods=['GET'])
def get_single_persona(persona_id):
    """Obtener detalles de Person unico"""
    response_object = {
        'status': 'fail',
        'message': 'la persona no existe'
    }
    try:
        persona = Persona.query.filter_by(id=int(persona_id)).first()
        if not persona:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': persona.id,
                    'name': persona.name,
                    'lastname': persona.lastname,
                    'age': persona.age,
                    'gender': persona.gender,
                    'active': persona.active
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@smartphones_blueprint.route('/smartphones', methods=['GET'])
def get_all():
    """Obteniendo todos los smartphones"""
    response_object = {
        'status': 'success',
        'data': {
            'smartphones': [smartphone.to_json()
                            for smartphone
                            in Smartphone.query.all()]
        }
    }
    return jsonify(response_object), 200


@smartphones_blueprint.route('/smartphones/personas/all',
                             methods=['GET'])
def get_allPersonas():
    """Obteniendo todos las Personas"""
    response_object = {
        'status': 'success',
        'data': {
            'personas': [personas.to_json()
                         for personas
                         in Persona.query.all()]
        }
    }
    return jsonify(response_object), 200


@smartphones_blueprint.route('/smartphones/personas/<int:id_persona>/telefono',
                             methods=['GET'])
def get_one_personas_phones(id_persona):
    """Obteniendo las Personas con sus telefonos"""
    lista_con_smartphone = Smartphone.query.join(Persona).add_columns(
        Persona.lastname,
        Persona.age,
        Persona.gender,
        Smartphone.name,
        Smartphone.brand,
        Smartphone.price,
        Smartphone.color).filter(Smartphone.propietario == id_persona)
    response_object = {
                'status': 'success',
                'data': {
                    'misCelulares': [convert_json(smartphone)
                                     for smartphone
                                     in lista_con_smartphone]
                }
    }
    return jsonify(response_object), 200


@smartphones_blueprint.route('/smartphones/personas/all/telefono',
                             methods=['GET'])
def get_all_personas_phones():
    """Obteniendo todas las Personas con sus telefonos"""
    lista_con_smartphone = Smartphone.query.join(Persona).add_columns(
        Persona.lastname,
        Persona.age,
        Persona.gender,
        Smartphone.name,
        Smartphone.brand,
        Smartphone.price,
        Smartphone.color).order_by(Smartphone.id)
    response_object = {
                'status': 'success',
                'data': {
                    'misCelulares': [convert_json(smartphone)
                                     for smartphone
                                     in lista_con_smartphone]
                }
    }
    return jsonify(response_object), 200


def convert_json(smartphone_lista):
    return {
            'lastname': smartphone_lista.lastname,
            'age': smartphone_lista.age,
            'gender': smartphone_lista.gender,
            'name': smartphone_lista.name,
            'brand': smartphone_lista.brand,
            'price': smartphone_lista.price,
            'color': smartphone_lista.color
        }
