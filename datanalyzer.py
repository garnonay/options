import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from pathlib import Path
import base64
import matplotlib
import footer
import os


st.set_option('deprecation.showfileUploaderEncoding', False)
f = Path('GT data.png')

def img_to_bytes(img_path):
    img_bytes = f.read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descarga {file_label}</a>'
    return href

# def read_markdown_file(markdown_file):
#     return Path(markdown_file).read_text()

header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(img_to_bytes("GT data.png"))
st.markdown(header_html, unsafe_allow_html=True)
st.write('')
st.write('')

intro_markdown = f'''
<details>
    <summary>🔎 Info</summary>
    Esta herramienta te permite realizar una exploración de datos sobre ficheros TXT, XLSX y CSV.
    Simplemente selecciona el fichero que vas a cargar en el menú de la izquierda, el tipo de Informe y carga el fichero a través del menú de abajo! 👇
</details>'''

st.markdown(intro_markdown, unsafe_allow_html=True)
st.write('')
st.write('')

d = st.sidebar.selectbox('Selecciona el tipo de fichero', ('txt', 'xlsx', 'csv'))
e = st.sidebar.selectbox('¿Qué tipo de Informe quieres?', ('Resumido', 'Completo'))

uploaded_file = st.file_uploader("Adjuntar datos para analizar")

if uploaded_file is not None:
    if d == 'txt':
        df = pd.read_table(uploaded_file, sep=',')
    elif d == 'xlsx':
        df = pd.read_excel(uploaded_file)
    elif d == 'csv':
        df = pd.read_csv(uploaded_file, sep=',')
    if e == 'Resumido':
        pr = ProfileReport(df, minimal=True, explorative=True)
    else:
        pr = ProfileReport(df, explorative=True)
    st_profile_report(pr)
    pr.to_file("output.html")
    st.sidebar.markdown(f'''<button type="button" class="btn btn-warning btn-lg btn-block">{get_binary_file_downloader_html('output.html', 'Informe')}</button>''', unsafe_allow_html=True)

st.write('')
st.write('')

footer.footer()
