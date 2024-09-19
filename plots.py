import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
import matplotlib.ticker as ticker

# Encontrar el archivo CSV
archivos_csv = glob('laptops*.csv')
if not archivos_csv:
    raise FileNotFoundError("No se encontró ningún archivo CSV que comience con 'laptops'.")
archivo_csv = archivos_csv[0]

# Leer el archivo CSV
df = pd.read_csv(archivo_csv)

# Convertir Price a numérico, eliminando cualquier símbolo de moneda
df['Price'] = df['Price'].replace(r'[$,]', '', regex=True).astype(float)

# Crear una figura con dos subtramas
fig, (eje1, eje2) = plt.subplots(2, 1, figsize=(12, 14))


# Función para formatear las etiquetas del eje x con 6 decimales
def funcion_formato(valor, numero_tick):
    return f"{valor:.6f}"


# Gráfico 1: Histograma de Prices con KDE
sns.histplot(df['Price'], kde=True, ax=eje1)
eje1.set_title('Distribución de Prices de Laptops')
eje1.set_xlabel('Price')
eje1.set_ylabel('Frecuencia')
eje1.xaxis.set_major_formatter(ticker.FuncFormatter(funcion_formato))

# Calcular RIC (Rango Intercuartílico)
Q1 = df['Price'].quantile(0.25)
Q3 = df['Price'].quantile(0.75)
RIC = Q3 - Q1

# Gráfico 2: Gráfico de violín
sns.violinplot(x=df['Price'], ax=eje2)
eje2.set_title('Gráfico de Violín de Prices de Laptops')
eje2.set_xlabel('Price')
eje2.xaxis.set_major_formatter(ticker.FuncFormatter(funcion_formato))

# Añadir anotación de texto para RIC con 6 decimales
eje2.text(0.95, 0.95, f'RIC: {RIC:.6f}', transform=eje2.transAxes,
          verticalalignment='top', horizontalalignment='right')

# Ajustar diseño y mostrar gráficos
plt.tight_layout()
plt.show()

# Imprimir estadísticas resumidas con alta precisión
pd.set_option('display.float_format', '{:.6f}'.format)
print(df['Price'].describe())

# Encontrar los rangos de Prices más frecuentes
rango_Prices = pd.cut(df['Price'], bins=10)
print("\nRangos de Prices más frecuentes:")
print(rango_Prices.value_counts().nlargest(3))

# Restablecer el formato flotante al predeterminado
pd.reset_option('display.float_format')
