
import os
import pytest


from app import app
from app import db

# @pytest.fixture
# def create_new(scope ='module'):
#     new_bl = BrokenLaptop(brand='HP-new',price=1234)
#     #new_bl = BrokenLaptop(brand='HP-new',price='1234')
#     
#     return new_bl
# 
# # this is a unit test example (to check if each function is producing correct output)
# def test_create_new(create_new):
#     """
#     GIVEN a BrokenLaptop model 
#     WHEN a new BrokenLaptop is created 
#     THEN check the name and price 
#     """
#     assert create_new.brand == 'HP-new'
#     assert create_new.price == 1234
     

@pytest.fixture
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
   
    os.unlink('testing.db')
    
# route /
def test_index(client):
    """Main page shows a welcome message."""
    main_page = client.get('/')
    #assert b'This is an application to manage Broken Laptops' in main_page.data
    assert b'Hello, world!' in main_page.data
    assert b'Brand' in main_page.data 
    assert b'Price' in main_page.data 
    
    
# route /create
def test_create_page(client):
    create_page = client.get('/create')
    assert b'New Broken Laptop' in create_page.data 
    assert b'Add' in create_page.data

# route /create (submit with data)
def test_create_page_submit(client):
    data = {
        "brand":"My-Brand",
        "price": 56
        }
    #page1 = client.post('/create',data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    client.post('/create',data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    #assert page1.status == '200 OK'
    
    page2 = client.get('/')
    assert b'My-Brand' in page2.data
    assert b'56.0' in page2.data
    
    
    