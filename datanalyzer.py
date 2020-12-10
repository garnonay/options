import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from pathlib import Path
import base64
import matplotlib
import footer


st.set_option('deprecation.showfileUploaderEncoding', False)
f = Path('GT data.png')

def img_to_bytes(img_path):
    img_bytes = f.read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(img_to_bytes("GT data.png"))
st.markdown(header_html, unsafe_allow_html=True)
st.write('')
st.write('')


d = st.sidebar.selectbox('Selecciona el tipo de fichero', ('xls', 'txt', 'csv'))


#df = pd.read_csv(r'C:\Users\jgarcian\Desktop\Proyectos\Bankia\ProyectoValidacion\07. Pricers\NuevoVaR\V2\var_cfs_vol.txt', sep=',')
uploaded_file = st.file_uploader("Adjuntar datos para analizar")

if uploaded_file is not None:
    if d == 'txt':
        df = pd.read_table(uploaded_file, sep=',')
    elif d == 'xls':
        df = pd.read_excel(uploaded_file)
    elif d == 'csv':
        df = pd.read_csv(uploaded_file, sep=',')
    pr = ProfileReport(df, explorative=True)
    st_profile_report(pr)

st.write('')
st.write('')

footer.footer()
