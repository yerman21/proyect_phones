import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import Smartphone, Persona


def add_smartphone(name, brand, price, color, quantity):
    smartphone = Smartphone(name=name, brand=brand,
                            price=price, color=color,
                            quantity=quantity)
    db.session.add(smartphone)
    db.session.commit()
    return smartphone


def add_smartphone_with_propietario(name, brand, price,
                                    color, quantity,
                                    propietario):
    smartphone = Smartphone(name=name, brand=brand,
                            price=price, color=color,
                            quantity=quantity,
                            propietario=propietario)
    db.session.add(smartphone)
    db.session.commit()
    return smartphone


def add_persona(name, lastname, age, gender):
    persona = Persona(name=name, lastname=lastname,
                      age=age, gender=gender)
    db.session.add(persona)
    db.session.commit()
    return persona


class TestSmartphoneService(BaseTestCase):
    """Tests para el servicio Smartphone."""

    def test_smartphones(self):
        """Nos aseguramos que la ruta
        localhost:5001/smartphones/ping
        esta funcionando correctamente."""
        response = self.client.get('/smartphones/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_smartphone(self):
        """Asegurando de que se pueda agregar un
        nuevo Smartphone a la db"""
        with self.client:
            response = self.client.post('/smartphones', data=json.dumps({
                    "name": "Nokia 23",
                    "brand": "Nokia",
                    "price": 920,
                    'color': 'amarillo',
                    'quantity': 10
                    }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn("success", data["status"])
        self.assertIn('Nokia 23, marca Nokia a sido agregado '
                      'sin propietario!!', data["message"])

    def test_add_smartphone_with_propietario(self):
        """Asegurando de que se pueda agregar un
        nuevo Smartphone a la db"""
        with self.client:
            persona = add_persona('yerman', 'Guz', 22, 'M')
            response = self.client.post('/smartphones', data=json.dumps({
                    "name": "Nokia 23",
                    "brand": "Nokia",
                    "price": 920,
                    'color': 'amarillo',
                    'quantity': 10,
                    'propietario': persona.id
                    }), content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn("success", data["status"])
        self.assertIn('Nokia 23, marca Nokia a sido '
                      'agregado con propietario!!',
                      data["message"])

#    def test_update_smartphone(self):
#        """Asegurando de que se pueda modificar
#        un Smartphone en la db"""
#        with self.client:
#            response = self.client.post('/smartphones/update',
#            data=json.dumps({
#                    "id": 1,
#                    "name": "Nokia Modificado",
#                    "brand": "Nokia",
#                    "price": 9000,
#                    'color': 'Rosado',
#                    'quantity': 10
#                    }), content_type="application/json")
#        data = json.loads(response.data.decode())
#        self.assertIn('Nokia Modificado,
#        marca Nokia a sido modificado!!', data['message'])
#        self.assertEqual(response.status_code, 201)
#        self.assertIn("success", data["status"])

#     def test_delete_smartphone(self):
#         """Asegurando de que se pueda eliminar un Smartphone en la db"""
#         with self.client:
#             sm = add_smartphone('Nokia n24', 'Nokia', 203, 'rojo', 29)
#             response = self.client.get('/smartphones/{sm.id}/delete')
#             data = json.loads(response.data.decode())
#             self.assertIn('el smartphone fue eliminado.', data['message'])
#             self.assertEqual(response.status_code, 200)
#             self.assertIn("success", data["status"])

    def test_add_smartphone_invalid_json(self):
        """ Asegurando de que se arroje un error
         si el objeto JSON está vacío."""
        with self.client:
            response = self.client.post(
                '/smartphones',
                data=json.dumps({}),
                content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('carga invalida.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_smartphone_invalid_json_keys(self):
        """Asegurando de que se produce un error si el
         objeto JSON no tiene una clave
         de brand de smartphone."""
        with self.client:
            response = self.client.post(
                '/smartphones',
                data=json.dumps({'name': 'Samsung J6'}),
                content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])

    def test_add_smartphone_duplicate_email(self):
        """Asegurando de que se haya producido
        un error si el nombre del smartphone y
        la marca ya existen."""
        with self.client:
            self.client.post(
                '/smartphones',
                data=json.dumps({
                        "name": "Nokia 23",
                        "brand": "Nokia",
                        "price": 920,
                        'color': 'Rosado',
                        'quantity': 10}),
                content_type='application/json',)
            response = self.client.post(
                '/smartphones',
                data=json.dumps({
                    "name": "Nokia 23",
                    "brand": "Nokia",
                    "price": 1000,
                    'color': 'Rosado',
                    'quantity': 10
                    }),
                content_type='application/json',)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Lo siento. Este smartphone ya existe.',
                          data['message'])
            self.assertIn('fail', data['status'])

    def test_single_smartphone(self):
        """Asegurando de que el smartphone
        individual se comporte correctamente"""
        smartphone = add_smartphone('Nokia 90', 'Nokia', 800, 'Azul', 3)
        with self.client:
            response = self.client.get(f'/smartphones/{smartphone.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Nokia 90', data['data']['name'])
            self.assertIn('Nokia', data['data']['brand'])
            self.assertEqual(800, data['data']['price'])
            self.assertIn('success', data['status'])

    def test_single_persona(self):
        """Asegurando de que la persona
        individual se comporte correctamente"""
        persona = add_persona('Julio', 'Guzman', 23, 'M')
        with self.client:
            response = self.client.get(f'/smartphones/persona/{persona.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Julio', data['data']['name'])
            self.assertIn('Guzman', data['data']['lastname'])
            self.assertEqual(23, data['data']['age'])
            self.assertIn('M', data['data']['gender'])
            self.assertIn('success', data['status'])

    def test_single_smartphone_no_id(self):
        """Asegurese de que se arroje un error
        si no se proporciona una identificacion."""
        with self.client:
            response = self.client.get("/smartphones/blah")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('el smartphone no existe', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_smartphone_incorrect_id(self):
        """Asegurando se que se arroje un error si
        la identificacion no existe"""
        with self.client:
            response = self.client.get("/smartphones/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('el smartphone no existe', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_smartphones(self):
        """Asegurando de que todos los smartphones se
        comporten correctamente"""
        add_smartphone('Nokia 90', 'Nokia', 800, 'Ginda', 10)
        add_smartphone('Nokia 100', 'Nokia', 1000, 'Celeste', 2)
        with self.client:
            response = self.client.get("/smartphones")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['smartphones']), 2)
            self.assertIn('Nokia 90', data['data']['smartphones'][0]['name'])
            self.assertIn(
                'Nokia', data['data']['smartphones'][0]['brand'])
            self.assertIn('Nokia 100', data['data']['smartphones'][1]['name'])
            self.assertIn(
                'Nokia', data['data']['smartphones'][1]['brand'])
            self.assertIn('success', data['status'])

    def test_all_personas(self):
        """Asegurando de que todos las personas se
        comporten correctamente"""
        add_persona('Maria', 'Guzman', 23, 'F')
        add_persona('Mordonia', 'Gune', 20, 'M')
        with self.client:
            response = self.client.get("/smartphones/personas/all")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['personas']), 2)
            self.assertIn('Maria', data['data']['personas'][0]['name'])
            self.assertIn(
                'Guzman', data['data']['personas'][0]['lastname'])
            self.assertIn('Mordonia', data['data']['personas'][1]['name'])
            self.assertIn(
                'Gune', data['data']['personas'][1]['lastname'])
            self.assertIn('success', data['status'])

    def test_one_personas_relations(self):
        """Asegurando de que una de las personas que tengan celulares
        se comporten correctamente"""
        persona = add_persona('Maria', 'Guzman', 23, 'F')
        add_smartphone_with_propietario('Nokia 90', 'Nokia',
                                        800, 'Ginda', 10,
                                        persona.id)
        add_smartphone_with_propietario('Nokia 100', 'Nokia',
                                        1000, 'Celeste',
                                        2, persona.id)
        with self.client:
            response = self.client.get(f'/smartphones/personas/{persona.id}'
                                       '/telefono')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['misCelulares']), 2)
            self.assertIn('Guzman',
                          data['data']['misCelulares'][0]['lastname'])
            self.assertIn(
                'F', data['data']['misCelulares'][0]['gender'])
            self.assertIn('Nokia 90', data['data']['misCelulares'][0]['name'])
            self.assertIn(
                'Nokia 100', data['data']['misCelulares'][1]['name'])
            self.assertIn('success', data['status'])

    def test_all_personas_relations(self):
        """Asegurando de que todos las personas que tengan celulares
        se comporten correctamente"""
        persona = add_persona('Maria', 'Guzman', 23, 'F')
        add_smartphone_with_propietario('Nokia 98', 'Nokia',
                                        800, 'Ginda', 10,
                                        persona.id)
        add_smartphone_with_propietario('Nokia 10', 'Nokia',
                                        1000, 'Celeste',
                                        2, persona.id)
        with self.client:
            response = self.client.get(f'/smartphones/personas/all'
                                       '/telefono')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['misCelulares']), 2)
            self.assertIn('Guzman',
                          data['data']['misCelulares'][0]['lastname'])
            self.assertIn(
                'F', data['data']['misCelulares'][0]['gender'])
            self.assertIn('Nokia 98', data['data']['misCelulares'][0]['name'])
            self.assertIn(
                'Nokia 10', data['data']['misCelulares'][1]['name'])
            self.assertIn('success', data['status'])

    def test_main_with_users(self):
        """Ensure the main route behaves correctly when smartphones have been
        added to the database."""
        add_smartphone('Nokia 0', 'Nokia', 900, 'Azul', 2)
        add_smartphone('Motorl d30', 'Motorola', 1000, 'Azul', 2)
        with self.client:
            response = self.client.get('/smartphones/jinga/index')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Smartphones', response.data)
            self.assertNotIn(b'<p>No Smartphones!</p>', response.data)
            self.assertIn(b'Nokia 0', response.data)
            self.assertIn(b'Motorl d30', response.data)

    def test_main_no_smartphones(self):
        """Ensure the main route behaves correctly when
        no smartphones have been added to the database."""
        response = self.client.get('/smartphones/jinga/index')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Smartphones', response.data)
        self.assertIn(b'<p>No Smartphones!</p>', response.data)

    def test_main_add_smartphone(self):
        """Ensure a new smartphone can be added to the database."""
        with self.client:
            persona = add_persona('Marcos', 'Guzman', 23, 'M')
            response = self.client.post(
                '/smartphones/jinga/index',
                data=dict(name='iPhone X', brand='Apple',
                          price=320, color='blanco',
                          quantity=290, propietario=persona.id),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Smartphones', response.data)
            self.assertNotIn(b'<p>No Smartphones!</p>', response.data)
            self.assertIn(b'iPhone X', response.data)


if __name__ == '__main__':
    unittest.main()
