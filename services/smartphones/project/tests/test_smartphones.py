import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import Smartphone


def add_smartphone(name, brand, price, color, quantity):
    smartphone = Smartphone(name=name, brand=brand,
                            price=price, color=color,
                            quantity=quantity)
    db.session.add(smartphone)
    db.session.commit()
    return smartphone


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

#    def test_delete_smartphone(self):
#        """Asegurando de que se pueda eliminar un Smartphone en la db"""
#        with self.client:
#            response = self.client.get('/smartphones/1/delete')
#            data = json.loads(response.data.decode())
#            self.assertIn('el smartphone fue eliminado.', data['message'])
#            self.assertEqual(response.status_code, 200)
#            self.assertIn("success", data["status"])

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


if __name__ == '__main__':
    unittest.main()
