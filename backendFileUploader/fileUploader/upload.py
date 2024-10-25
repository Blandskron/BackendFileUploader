import requests

# URL del endpoint de tu API de Django para subir archivos
url = 'http://localhost:8000/api/upload/'

# Ruta local al archivo que deseas subir
file_path = '1.pdf'  # Cambia esto por la ruta real de tu archivo

# Abre el archivo en modo binario para leer
with open(file_path, 'rb') as f:
    # Crea un diccionario con el archivo que deseas subir
    files = {'file': f}
    
    # Realiza la petición POST al endpoint de subida
    response = requests.post(url, files=files)
    
    # Imprimir la respuesta del servidor
    print('Status code:', response.status_code)
    print('Response body:', response.json())
    