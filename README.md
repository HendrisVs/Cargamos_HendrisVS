# Cargamos_HendrisVS
Prueba técnica para postulación a Cargamos. 
API Rest de tiendas. Posibilidad de agregar y consultar inventario de distintas tiendas. 

## Python Version
Python 3.8.2

## Postgresssql Version
postgressql v10.16-1

## REST Client to testing
Insomnia Core 2020.5.2

## Add Store
route: "/store"  
method: "POST"
```json
JSON = {"store_name":"MiPrimerTienda", 
		"phone":"558-123-4567",
		"address":"Street 1 #10", 
		 "country":"Mexico"}
```

## Register product information
route: "/product"  
method: "POST"
```json
JSON = {"product_name":"Celular", 
		"brand":"Huawei",
		"model":"Mate 20", 
		"description":"Black color", 
		"SKU":"SKU154D744", 
		"price":3500}
````

## Add to inventory
route: "/inventory"  
method: "POST"
```json
JSON = {"store_name":"MiPrimerTienda", 
		"sku":"SKU154D744",
		"quantity":20,
		"location":"A50"}
````
## Increase stock
route: "/inventory"  
method: "PUT"
```json
JSON = {"store_name":"MiPrimerTienda", 
		"sku":"SKU154D744",
		"quantity":5}
```
## Get all products in store
```
route: "inventory/MiPrimerTienda"`
```

## Get stock by product
```
route: "inventory/MiPrimerTienda/SKU154D744"
```
## Check status stock by desired quantity
```
route: "/stock_status/MiPrimerTienda/SKU154D744/600"
```