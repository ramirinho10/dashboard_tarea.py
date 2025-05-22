
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

df = load_data()

st.title("Dashboard Interactivo - Análisis de Ventas y Clientes")

st.sidebar.header("Filtros")
branches = st.sidebar.multiselect("Sucursal", df["Branch"].unique(), default=df["Branch"].unique())
product_lines = st.sidebar.multiselect("Línea de Producto", df["Product line"].unique(), default=df["Product line"].unique())

df_filtered = df[(df["Branch"].isin(branches)) & (df["Product line"].isin(product_lines))]

# Evolución de ventas
st.subheader("Evolución de Ventas Totales")
sales_by_month = df_filtered.groupby("Month")["Total"].sum()
st.line_chart(sales_by_month)

# Ingresos por línea de producto
st.subheader("Ingresos por Línea de Producto")
sales_by_product = df_filtered.groupby("Product line")["Total"].sum().sort_values()
fig1, ax1 = plt.subplots()
sns.barplot(x=sales_by_product.values, y=sales_by_product.index, ax=ax1)
ax1.set_xlabel("Total")
st.pyplot(fig1)

# Distribución de calificaciones
st.subheader("Distribución de la Calificación de Clientes")
fig2, ax2 = plt.subplots()
sns.histplot(df_filtered["Rating"], bins=10, kde=True, ax=ax2)
st.pyplot(fig2)

# Comparación de gasto por tipo de cliente
st.subheader("Gasto Total por Tipo de Cliente")
fig3, ax3 = plt.subplots()
sns.boxplot(data=df_filtered, x="Customer type", y="Total", ax=ax3)
st.pyplot(fig3)

# Relación entre costo y ganancia
st.subheader("Relación entre Costo (COGS) y Ganancia Bruta")
fig4, ax4 = plt.subplots()
sns.scatterplot(data=df_filtered, x="cogs", y="gross income", hue="Branch", ax=ax4)
st.pyplot(fig4)

# Métodos de pago preferidos
st.subheader("Frecuencia de Métodos de Pago")
payment_count = df_filtered["Payment"].value_counts()
fig5, ax5 = plt.subplots()
payment_count.plot(kind="bar", ax=ax5)
ax5.set_ylabel("Frecuencia")
st.pyplot(fig5)

# Correlación numérica
st.subheader("Matriz de Correlación entre Variables Numéricas")
numeric_cols = ["Unit price", "Quantity", "Tax 5%", "Total", "cogs", "gross income", "Rating"]
fig6, ax6 = plt.subplots(figsize=(10, 6))
sns.heatmap(df_filtered[numeric_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax6)
st.pyplot(fig6)

# Ingreso bruto por sucursal y producto
st.subheader("Ingreso Bruto por Sucursal y Línea de Producto")
pivot_data = df_filtered.pivot_table(index="Product line", columns="Branch", values="gross income", aggfunc="sum")
fig7, ax7 = plt.subplots()
pivot_data.plot(kind="bar", stacked=True, ax=ax7)
ax7.set_ylabel("Ingreso Bruto")
st.pyplot(fig7)

