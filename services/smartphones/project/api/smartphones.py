# services/users/project/api/smartphones.py
# from flask import render_template
from flask import Blueprint, jsonify, request
# from sqlalchemy import update
from sqlalchemy import exc
from sqlalchemy.sql import func
from project.api.models import Smartphone
from project import db

smartphones_blueprint = Blueprint("smartphones",
                                  __name__,
                                  template_folder='./templates')


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
    try:
        smartphone = Smartphone.query.filter_by(name=name, brand=brand).first()
        if not smartphone:
            db.session.add(Smartphone(name=name, brand=brand, price=price,
                                      color=color, quantity=quantity))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{name}, '\
                'marca {brand} a sido agregado!!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Lo siento. '\
                'Este smartphone ya existe.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@smartphones_blueprint.route('/smartphones/update', methods=['POST'])
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


@smartphones_blueprint.route('/smartphones/<smartphone_id>', methods=['GET'])
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


@smartphones_blueprint.route('/smartphones/<int:smartphone_id>/delete',
                             methods=['GET'])
def delete_single_smartphone(smartphone_id):
    """Eliminar un smartphone"""
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
