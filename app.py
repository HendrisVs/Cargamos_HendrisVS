from flask import Flask
from flask import jsonify
from flask import request
import databaseManagement

app = Flask(__name__)

@app.route("/store", methods = ["POST"])
def add_store():
    """Registra una tienda nueva"""
    store_name = request.json["store_name"]
    phone = request.json["phone"]
    address = request.json["address"]
    country = request.json["country"]
    response = databaseManagement.insert_store_db(store_name, phone, address, country)
    return (jsonify(response))

@app.route("/product", methods = ["POST"])
def register_product():
    """Registra un producto para ser usado dentro de los inventarios"""
    product_name = request.json["product_name"]
    brand = request.json["brand"]
    model = request.json["model"]
    description = request.json["description"]
    sku = request.json["SKU"]
    price = request.json["price"]
    response = databaseManagement.register_product(product_name, brand, model,  description, sku, price)
    return (jsonify(response))

@app.route("/inventory", methods = ["POST"])
def add_to_inventory():
    """Agrega producto nuevo a inventario de tienda, incluye su localización"""
    store_name = request.json["store_name"]
    sku = request.json["sku"]
    quantity = request.json["quantity"]
    location = request.json["location"]
    response = databaseManagement.add_to_inventory(store_name, sku, quantity, location)
    return (jsonify(response))

@app.route("/inventory", methods = ["PUT"])
def increase_stock():
    """Incrementa el stock de la tienda de producto indicado por SKU"""
    store_name = request.json["store_name"]
    sku = request.json["sku"]
    quantity = request.json["quantity"]
    response = databaseManagement.increase_stock(store_name, sku, quantity)
    return (jsonify(response))

@app.route("/sale", methods = ["PUT"])
def decrease_stock():
    """Decrementa el stock de la tienda al realizar compra"""
    store_name = request.json["store_name"]
    sku = request.json["sku"]
    quantity = request.json["quantity"]
    response = databaseManagement.decrease_stock(store_name, sku, quantity)
    return (jsonify(response))

@app.route("/inventory/<string:store_name>/<string:product_sku>", methods = ["GET"])
def get_stock_product(store_name, product_sku): 
    """Stock de la tienda, por producto"""
    response = databaseManagement.get_stock_product(store_name, product_sku)
    return (jsonify(response))

@app.route("/inventory/<string:store_name>/", methods = ["GET"])
def get_stock_products(store_name): 
    """Stock de la tienda, todos los productos"""
    response = databaseManagement.get_stock_products(store_name)
    return (jsonify(response))

@app.route("/stock_status/<string:store_name>/<string:product_sku>/<int:quantity>", methods = ["GET"])
def check_stock(store_name, product_sku, quantity):
    """Determina si hay suficiente stock de producto en base a cantidad deseada"""
    response = databaseManagement.check_stock(store_name, product_sku, quantity)
    return (jsonify(response))

if __name__=="__main__":
    app.run(debug=True, port=5000)
