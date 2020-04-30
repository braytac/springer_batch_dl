#!/usr/bin/env python
# coding: utf-8

import os
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup
import urllib.request

directorio_destino = '<path>'


archivo = open("file.txt")

for linea in archivo:

    link = re.findall(r'(http\:[.\S]*)', linea, re.M|re.IGNORECASE)

    if link:
        try:
            page = requests.get(link[0])
            soup = BeautifulSoup(page.content, features='html')
            nombre_libro = soup.select(".evaluation-section .page-title h1")

            urls={}

            urls.update({"epub" : [link.get("href") 
                                  for link in soup("a", 
                                                attrs={"class": "test-bookepub-link"})] 
                        })
            urls.update({"pdf": [link.get("href") 
                                  for link in soup("a", 
                                                attrs={"class": "test-bookpdf-link"})] 
                        })
            for (formato,url) in urls.items():

                if url and nombre_libro:

                    nombre_libro_str = nombre_libro[0].get_text()
                    nombre_libro_str = nombre_libro_str.replace('/', '-')
                    nombre_libro_str = re.sub('[^0-9a-zA-Z\s\.\-_]+', '', nombre_libro_str)

                    if "//link.springer.com" in url[0]:
                        url = url[0]
                    else:
                        url = "https://link.springer.com"+url[0]
                    archivo = Path(os.path.join(
                                    directorio_destino,formato,nombre_libro_str+'.'+formato)
                                  )
                    
                    if not archivo.is_file():
                        print("==> Descargando "+url+" ...")
                        try:
                            urllib.request.urlretrieve(url, archivo)
                            #urllib.request.urlretrieve(url, os.path.join(
                            #        directorio_destino,formato,nombre_libro+'.'+formato))
                        except:
                            print("falló, probablemente no exista.")
                            pass
                    else:
                        print(str(archivo)+" ya existe.")
        finally: 
            pass
