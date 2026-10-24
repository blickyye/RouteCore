from app.test.test_db import client

def get_auth_token(client, login, email):
    registration_response = client.post('/app/auth/registration', json={'login': login, 'email': email, 'password': 's'})
    
    assert registration_response.status_code == 200

    login_response = client.post('/app/auth/login', json={'login': login, 'password': 's'})

    assert login_response.status_code == 200
    return login_response.json()['access_token']


def get_auth_courier_token(client, login, email):
    registration_response = client.post('/app/auth/registration', json={'login': login, 'email': email, 'password': 'b'})
    
    assert registration_response.status_code == 200
    
    login_response = client.post('/app/auth/login', json={"login": login,"password": "b"})

    assert login_response.status_code == 200
    token = login_response.json()['access_token']

    create_courier_response = client.post('/app/couriers/', headers={'Authorization': f'Bearer {token}'})

    assert create_courier_response.status_code == 200
    return token


def test_create_order_200(client):
    token = get_auth_token(client, 's', 's')

    response = client.post('/app/orders/', json={'pickup_address': 's', 'delivery_address': 's', 'description': 's'},

                        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200

def test_create_order_422(client):
    token = get_auth_token(client, 's', 's')

    response = client.post('/app/orders/', json={'pickup_address': 12, 'delivery_address': None, 'description': 777},
                        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 422

def test_cancel_someone_order(client):
    creator_token = get_auth_token(client, 'c', 'c')
    canceller_token = get_auth_token(client, 'b', 'b')

    create_order_response = client.post('/app/orders/', json={'pickup_address': 's', 'delivery_address': 's', 'description': 's'},
                headers={'Authorization': f'Bearer {creator_token}'})
    
    assert create_order_response.status_code == 200
    order_id = create_order_response.json()['id']

    cancel_response = client.patch(f'/app/orders/{order_id}/cancel', headers={'Authorization': f'Bearer {canceller_token}'})

    assert cancel_response.status_code == 403

def test_accept_order(client):
    client_token = get_auth_token(client, 's', 's')
    courier_token = get_auth_courier_token(client, 'b', 'b')

    create_order_response = client.post('/app/orders/', json={'pickup_address': 's', 'delivery_address': 's', 'description': 's'},
                headers={'Authorization': f'Bearer {client_token}'})
    
    assert create_order_response.status_code == 200
    order_id = create_order_response.json()['id']

    accept_response = client.post(f'/app/orders/courier/{order_id}/accept', headers={'Authorization': f'Bearer {courier_token}'})

    assert accept_response.status_code == 200

def test_accept_someone_order(client):
    creator_client_token = get_auth_token(client, 'f', 'f')
    courier_accepter_token = get_auth_courier_token(client, 's', 's')
    someone_courier_token = get_auth_courier_token(client, 'b', 'b')

    create_order_response = client.post('/app/orders/', json={'pickup_address': 's', 'delivery_address': 's', 'description': 's'},
                headers={'Authorization': f'Bearer {creator_client_token}'})
    assert create_order_response.status_code == 200

    order_id = create_order_response.json()['id']
    
    accept_order_response = client.post(f'/app/orders/courier/{order_id}/accept', headers={'Authorization': f'Bearer {courier_accepter_token}'})
    assert create_order_response.status_code == 200

    accept_order_by_someone_response = client.post(f'/app/orders/courier/{order_id}/accept', headers={'Authorization': f'Bearer {someone_courier_token}'})

    assert accept_order_by_someone_response.status_code == 401