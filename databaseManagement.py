import psycopg2
from config import config

def connect_db():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    return (conn, cur)
 
def close_conn_db(conn, cur):
    conn.commit()
    cur.close()

def insert_store_db(store_name, phone_store, address_store, country_store):
    """ Registra en DB una nueva tienda"""
    sql = """INSERT INTO tbl_store( store_name, address, phone, country) SELECT %s, %s, %s, %s 
          WHERE NOT EXISTS (SELECT * FROM tbl_store WHERE store_name = %s);"""
    try:
        conn, cur = connect_db()
        cur.execute(sql, (store_name, address_store, phone_store, country_store, store_name))
        close_conn_db(conn, cur)
        response = {"status":"New stored added"}
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        response = {"status":str(error)}
    finally:
        if conn is not None:
            conn.close()
        return (response)

def add_manager_db(manager_name, phone):
    """ Registra en DB nuevo supervisor"""
    sql = """INSERT INTO tbl_managers(name, phone)
            VALUES( %s, %s);"""
    try:
        conn, cur = connect_db()
        cur.execute(sql, (manager_name, phone))
        close_conn_db(conn, cur)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def register_product(product_name, brand, model,  description, sku, price):
    """Crea un nuevo producto"""

    sql = """INSERT INTO tbl_products(name_product, brand,model,description,sku, price)
            SELECT  %s, %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT * FROM tbl_products WHERE sku = %s)"""
    try:
        conn, cur = connect_db()
        cur.execute(sql, (product_name, brand, model, description, sku, price, sku))
        close_conn_db(conn, cur)
        response = {"status":"New product available to inventory"}
    except (Exception, psycopg2.DatabaseError) as error:
        response = {"status":str(error)}
    finally:
        if conn is not None:
            conn.close()
        return (response)

def add_to_inventory(store_name, sku, quantity, location):
    """Crea un nuevo producto"""

    sql_select = """SELECT tbl_inventory.id FROM tbl_inventory 
            INNER JOIN tbl_products ON tbl_products.id = tbl_inventory.product_id
            INNER JOIN tbl_store ON  tbl_store.id = tbl_inventory.store_id
            WHERE tbl_store.store_name = %s AND tbl_products.sku = %s ;"""
    try:
        conn, cur = connect_db()
        cur.execute(sql_select, (store_name, sku))
        exist = cur.fetchone()
        if exist == None:
            sql_select_store = """SELECT tbl_store.id FROM tbl_store WHERE store_name = %s;"""
            cur.execute(sql_select_store, (store_name,))
            store_id = cur.fetchone()

            sql_select_store = """SELECT tbl_products.id FROM tbl_products WHERE tbl_products.sku = %s;"""
            cur.execute(sql_select_store, (sku,))
            product_id = cur.fetchone()

            sql_insert= """INSERT INTO tbl_inventory (store_id, product_id, 
                        quantity, location) VALUES (%s, %s, %s, %s)"""
            params =[store_id[0], product_id[0], quantity, location] 
            cur.execute(sql_insert, (params))
            response =  {"status": "Product added to inventory"}
        
        else:
            response =  {"status": "Product already exists"}
        close_conn_db(conn, cur)
    except (Exception, psycopg2.DatabaseError) as error:
        response =  {"status": str(error)}
    finally:
        if conn is not None:
            conn.close()
        return(response)

def increase_stock(store_name, sku, quantity):
    """Aumenta el stock de producto en inventario de tienda"""

    sql_select = """SELECT tbl_inventory.id FROM tbl_inventory 
            INNER JOIN tbl_products ON 
                tbl_products.id = tbl_inventory.product_id
            INNER JOIN tbl_store ON 
                tbl_store.id = tbl_inventory.store_id
            WHERE tbl_store.store_name = %s AND 
                tbl_products.sku = %s ;"""
    try:
        conn, cur = connect_db()
        cur.execute(sql_select, (store_name, sku))
        id_inventory = cur.fetchone()
        if id_inventory != None:
            sql_increase_stock = """  UPDATE tbl_inventory SET quantity = quantity + %s WHERE id = %s; """
            cur.execute(sql_increase_stock, (quantity, id_inventory[0]))
            response = {"status":"Increased stock"}
        else:
            response = {"status":"Inventory don't exist"}
        close_conn_db(conn, cur)
    except (Exception, psycopg2.DatabaseError) as error:
        response = {"status":str(error)}
    finally:
        if conn is not None:
            conn.close()
        return (response)

def decrease_stock(store_name, sku, quantity):
    """Disminuye el stock de producto en tienda al comprar"""

    sql_select = """SELECT tbl_inventory.id, tbl_inventory.quantity FROM tbl_inventory 
            INNER JOIN tbl_products ON 
                tbl_products.id = tbl_inventory.product_id
            INNER JOIN tbl_store ON 
                tbl_store.id = tbl_inventory.store_id
            WHERE tbl_store.store_name = %s AND 
                tbl_products.sku = %s ;"""
    try:
        conn, cur = connect_db()
        cur.execute(sql_select, (store_name, sku))
        inventory = cur.fetchone()
        if inventory != None:
            in_stock = int(inventory[1])
            if in_stock - quantity >=0 :
                sql_decrease_stock = """UPDATE tbl_inventory SET quantity = quantity - %s WHERE id = %s; """
                cur.execute(sql_decrease_stock, (quantity, inventory[0]))
                response = {"status":"Decreased stock"}
            else:
                response = {"status":"Insufficient stock"}
        else:
            response = {"status":"Inventory don't exist"}
        close_conn_db(conn, cur)
    except (Exception, psycopg2.DatabaseError) as error:
        response = {"status":str(error)}
    finally:
        if conn is not None:
            conn.close()
        return (response)

def get_stock_product(store_name, sku):
    """Consulta de stock en tienda por producto"""

    sql_select = """SELECT tbl_products.name_product, 
                            tbl_products.description, 
                            tbl_products.brand, 
                            tbl_products.model, 
                            tbl_inventory.quantity,
                            tbl_inventory.location
            FROM tbl_inventory 
            INNER JOIN tbl_products ON 
                tbl_products.id = tbl_inventory.product_id
            INNER JOIN tbl_store ON 
                tbl_store.id = tbl_inventory.store_id
            WHERE tbl_store.store_name = %s AND 
                tbl_products.sku = %s ; """

    try:
        conn, cur = connect_db()
        cur.execute(sql_select, (store_name, sku))
        stock = cur.fetchone()
        if stock != None:
            response = {"name_product": stock[0], 
                "description": stock[1], 
                "brand": stock[2], 
                "model": stock[3], 
                "quantity": str(stock[4]), 
                "location": stock[5]}
        else:
            response = {"status":"Info don't exist"}
        close_conn_db(conn, cur)
    except (Exception, psycopg2.DatabaseError) as error:
        response = {"status":str(error)}
    finally:
        if conn is not None:
            conn.close()
        return (response)

def get_stock_products(store_name):
    """Consulta todo el stock en tienda"""

    sql_select = """SELECT tbl_products.name_product, 
                            tbl_products.description, 
                            tbl_products.brand, 
                            tbl_products.model, 
                            tbl_inventory.quantity,
                            tbl_inventory.location
            FROM tbl_inventory 
            INNER JOIN tbl_products ON 
                tbl_products.id = tbl_inventory.product_id
            INNER JOIN tbl_store ON 
                tbl_store.id = tbl_inventory.store_id
            WHERE tbl_store.store_name = %s"""

    try:
        conn, cur = connect_db()
        cur.execute(sql_select, (store_name, ))
        products = cur.fetchall()
        listProducts = []
        for product in products: 
            dictProduct  = {
                "name_product": product[0], 
                "description": product[1], 
                "brand": product[2], 
                "model": product[3], 
                "quantity": str(product[4]), 
                "location": product[5]
            }
            listProducts.append(dictProduct)

        response = {"name_store": store_name, 
            "products": listProducts}
        close_conn_db(conn, cur)
    except (Exception, psycopg2.DatabaseError) as error:
        response = {"status":str(error)}
    finally:
        if conn is not None:
            conn.close()
        return (response)

def check_stock(store_name, product_sku, quantity):
    """Devuelve un bool representando el stock suficiente de producto"""
    sql_select = """SELECT tbl_inventory.quantity FROM tbl_inventory 
            INNER JOIN tbl_products ON 
                tbl_products.id = tbl_inventory.product_id
            INNER JOIN tbl_store ON 
                tbl_store.id = tbl_inventory.store_id
            WHERE tbl_store.store_name = %s AND 
                tbl_products.sku = %s ;"""
    try:
        stock_status = False
        conn, cur = connect_db()
        cur.execute(sql_select, (store_name, product_sku))
        inventory = cur.fetchone()
        if inventory != None:
            in_stock = int(inventory[0])
            if in_stock-int(quantity) >= 0:
                stock_status = True
            response = {"stock_available": stock_status}
        else:
            response = {"message":"Data don`t exists"}
    except (Exception, psycopg2.DatabaseError) as error:
        response = {"error":str(error)}
    finally:
        if conn is not None:
            conn.close()
        return (response)

