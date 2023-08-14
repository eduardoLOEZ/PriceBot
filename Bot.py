import requests
from bs4 import BeautifulSoup
import re


HTML_CLASS_CYBER= "submitButton largeButton cartIconPDP"
HTML_CLASS_MERCADO_LIBRE = "andes-button andes-spinner__icon-base andes-button--loud"
HTML_PRICE_CYBER ="priceText"
HTML_PRICE_MERCADO_LIBRE= "andes-money-amount__fraction"

HEADERS = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
  "Accept": "*/*"
}
#ver que hizo la peticion, un celular, computadroa etc


def guardar_pagina(contenido: str, nombre: str= "res.html") ->None:
    with open(nombre, "w") as f:
        f.write(contenido)


def get_page(url: str) -> str:
    
    res = requests.get(url, headers=HEADERS)  #Introducir HEADERS
    print(f"Código de estado HTTP: {res.status_code}")
    return res.text




def en_existencia(html: str) -> bool: #RETORNAR TIPOS DE DATOS EN ESPECIFICO 
    return HTML_CLASS_CYBER in html or HTML_CLASS_MERCADO_LIBRE in html


def input_prodcuts()-> tuple:
    nombre = input("Ingresa el nombre del producto: ")
    url = input("Ingresa la URL del producto: ")
    return nombre, url 

def input_price_range() -> tuple:
    min_price = float(input("ingresa el precio minimo: "))
    max_price = float(input("ingresa el precio maximo: "))

    return min_price, max_price

def extraer_precio(html: str) -> float:
    soup = BeautifulSoup(html, 'html.parser')
    precio_element = soup.find(class_=HTML_PRICE_CYBER)  # Encuentra el elemento con la clase del precio
    precio_element_mercado_libre = soup.find(class_=HTML_PRICE_MERCADO_LIBRE)

    if precio_element or precio_element_mercado_libre:
        if precio_element:
            precio_texto = precio_element.get_text()  # Obtiene el texto del elemento
        else:
            precio_texto = precio_element_mercado_libre.get_text()

        precio_texto_limpio = re.search(r"[\d.,]+", precio_texto).group()  # Busca y limpia el precio
        precio = float(precio_texto_limpio.replace(",", ""))  # Convierte a punto flotante
        return precio
    else:
        return None  # Si no se puede encontrar el precio, retorna None o un valor por defecto





def main() -> None:
        try:
            nombre, url = input_prodcuts()
            html = get_page(url)

            #guardar_pagina(html, "pagina.html")

            if en_existencia(html):
                min_price, max_price = input_price_range()
                price = extraer_precio(html)

                if min_price <= price <= max_price:
                    print(f"Hay {nombre} en existencia en el rango de precio deseado: ${price}")
                else:
                    print(f"Hay {nombre} en existencia, pero no cumple con el rango de precio. Precio: ${price}")
            else:
                print(f"NO HAY {nombre} en existencia. :(")

        except Exception as e:
              print("Ocurrió un error:", e)


if __name__ == "__main__":
    while True:
        main()
    


