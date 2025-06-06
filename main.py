# ? ASIGNATURA: Extracción de Conocimiento en Base de Datos
# ? Unidad 2: Preparación de los datos
# ? PE: Ingeniería en Desarrollo y Gestión de Software
# ? Realizado Por: Eli Haziel Ortiz Ramirez

##### ! IMPORTACIÓN DE LIBRERÍAS y PAQUETES  A UTILIZAR #####
import numpy as np
import pandas as pd
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

# * Graficadores
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# Inicializar console de Rich
console = Console()

# * Importamos los datos a un DataFrame
df = pd.read_csv("data/salaries.csv")

# Mostrar información del DataFrame con estilo
console.print(Panel.fit("📊 INFORMACIÓN DEL DATAFRAME", style="bold blue"))
rprint("[cyan]Estructura del DataFrame:[/cyan]")
df.info()
rprint(f"[green]📈 Número total de registros:[/green] [bold]{df.size}[/bold]")
rprint(f"[green]📋 Número de filas:[/green] [bold]{len(df)}[/bold]")

analysis_criteria = [
    "work_year",
    "experience_level",
    "employment_type",
    "job_title",
    "employee_residence",
    "company_location",
    "company_size",
]

# Tema de color
def_color = "pink"

console.print(Panel.fit("📈 GENERANDO HISTOGRAMAS", style="bold magenta"))
for f in analysis_criteria:
    rprint(f"[yellow]⏳ Procesando:[/yellow] [bold cyan]{f}[/bold cyan]")
    fig = px.histogram(df, x=f, color=f, color_discrete_sequence=[def_color])
    fig.update_layout(title_text=f"Distribución de {f}", title_x=0.5)
    # fig.show()
    time.sleep(1)

# Crear tabla para mostrar dimensiones del DataFrame
dimension_table = Table(title="📏 Dimensiones del DataFrame")
dimension_table.add_column("Métrica", style="cyan", no_wrap=True)
dimension_table.add_column("Valor", style="magenta")
dimension_table.add_row("Forma", str(df.shape))
dimension_table.add_row("Filas", str(df.shape[0]))
dimension_table.add_row("Columnas", str(df.shape[1]))
console.print(dimension_table)

# * Limitamos los datos y solo nos enfocamos en los datos recolectados desde 2023 empleos de tiempo completo (Full Time) en Estados Unidos (US)
console.print(
    Panel.fit("🔍 FILTRADO DE DATOS (2023+, Full Time, US)", style="bold green")
)

df_after2023 = df[
    (df.work_year >= 2023)
    & (df.employment_type == "FT")
    & (df.company_location == "US")
    & (df.salary_currency == "USD")
].copy()  # Agregar .copy() para evitar el warning

bins = [0, 100000, 250000, float("inf")]
labels = ["0-100K", "100K-250K", "250K+"]

# ? Eliminación de datos duplicados
console.print(Panel.fit("🧹 LIMPIEZA DE DATOS", style="bold yellow"))

# Crear tabla para mostrar estadísticas de limpieza
limpieza_table = Table(title="📊 Estadísticas de Limpieza")
limpieza_table.add_column("Descripción", style="cyan")
limpieza_table.add_column("Cantidad", style="magenta")

df_sin_duplicados = df_after2023.dropna()
datos_eliminados = len(df) - len(df_sin_duplicados)

limpieza_table.add_row("Tamaño DF Original", str(len(df)))
limpieza_table.add_row("Tamaño DF Sin Duplicados", str(len(df_sin_duplicados)))
limpieza_table.add_row("Datos Eliminados", str(datos_eliminados))

console.print(limpieza_table)

# * 5.- Análisis Básico del DataFrame (Datos Estadísticos Generales)
console.print(Panel.fit("📈 ANÁLISIS ESTADÍSTICO BÁSICO", style="bold blue"))
rprint("[cyan]Estadísticas descriptivas del DataFrame:[/cyan]")
console.print(df.describe())  # Usar console.print para mejor formato

df_after2023["salary_range"] = pd.cut(
    df_after2023["salary_in_usd"], bins=bins, labels=labels
)

salario_por_rango = df_after2023["salary_range"].value_counts().sort_index()

# Crear tabla para mostrar distribución salarial
salary_table = Table(title="💰 Distribución Salarial por Rangos")
salary_table.add_column("Rango Salarial", style="cyan")
salary_table.add_column("Cantidad de Empleos", style="green")

for rango, cantidad in salario_por_rango.items():
    salary_table.add_row(str(rango), str(cantidad))

console.print(salary_table)

rprint("[bold green]✅ Generando gráfico de barras...[/bold green]")
grafica = px.bar(
    x=salario_por_rango.index,
    y=salario_por_rango.values,
    labels={"x": "Rango de salario", "y": "Numero de empleos"},
    color=salario_por_rango.index,
    color_discrete_sequence=["skyblue"],
)
grafica.show()

console.print(Panel.fit("✨ ANÁLISIS COMPLETADO", style="bold green"))
