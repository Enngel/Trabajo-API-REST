# Probar limpieza de datos y representacion de datos
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración básica para que los gráficos se vean bien
sns.set_theme(style="whitegrid")

# Cargar el dataset
df = pd.read_csv('proyecto_institutos\\data\\centros_merged.csv')

# Vemos la estructura básica
print(f"Total de registros iniciales: {len(df)}") #Cuantos registros hay

# 1. Definir los tipos de centro que corresponden a IES y FP
tipos_ies_fp = ['IES', 'CIFP', 'CPR FP', 'CPR FPE', 'IFP', 'SFP', 'CFP', 'CP FPE', 'CP IFP']

# 2. Filtrar el DataFrame
df_institutos = df[df['tipo'].isin(tipos_ies_fp)].copy() #Recoge del anterior array solo los que tengan esas terminaciones

# 3. Limpiar valores nulos en coordenadas
df_institutos = df_institutos.dropna(subset=['latitud', 'longitud'])

print(f"Total de institutos y centros FP tras la limpieza: {len(df_institutos)}") #Total de registros tras el filtro

#Esto es para representar los datos,pero no es necesario, descomentadolo si quereis saber
#Como se distribuyen los institutos y centros de FP por titularidad y por municipio. Esto nos dará una idea de dónde se concentran más estos centros
# y si hay alguna diferencia significativa entre públicos y privados.
"""

### REPRESENTACION DE DATOS ###

# Gráfico 1: Distribución por Titularidad (Público / Privado)
plt.figure(figsize=(8, 5))
sns.countplot(data=df_institutos, x='titularidad', palette='viridis')
plt.title('Distribución de IES y FP por Titularidad')
plt.xlabel('Titularidad')
plt.ylabel('Cantidad de Centros')
plt.show()

# Gráfico 2: Top 10 municipios con más centros de IES/FP
plt.figure(figsize=(10, 6))
top_municipios = df_institutos['municipio'].value_counts().head(10)
sns.barplot(y=top_municipios.index, x=top_municipios.values, palette='magma')
plt.title('Top 10 Municipios con más IES y Centros de FP')
plt.xlabel('Número de Institutos')
plt.ylabel('Municipio')
plt.show()


"""



# Guardar el CSV filtrado para el paso de Ingesta (Load)
archivo_limpio = 'proyecto_institutos\\data\\institutos_limpios.csv'
df_institutos.to_csv(archivo_limpio, index=False, encoding='utf-8')
print(f"Archivo exportado  como {archivo_limpio}.")