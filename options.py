#
# Black-Scholes-Merton (1973) European Call & Put Valuation
#

import streamlit as st
import pandas as pd
import math
import numpy as np
from scipy.integrate import quad
from scipy.stats import norm
from PIL import Image
from datetime import date, timedelta
import datetime
today = date.today()
tomorrow = date.today() + timedelta(days=1)
from pathlib import Path
import base64
#image = Image.open('bankia.png')
#st.image(image, use_column_width=False)
import login

# from SessionState import get
# session_state = get(password='')
#
# if session_state.password != 'pwd123':
#     pwd_placeholder = st.empty()
#     pwd = pwd_placeholder.text_input("Password:", value="", type="password")
#     session_state.password = pwd
#     if session_state.password == 'pwd123':
#         pwd_placeholder.empty()
#         main()
#     elif session_state.password != '':
#         st.error("the password you entered is incorrect")
# else:
#     main()


st.set_option('deprecation.showfileUploaderEncoding', False)
f = Path('bankia2.png')

def img_to_bytes(img_path):
    img_bytes = f.read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(img_to_bytes("bankia2.png"))
st.markdown(header_html, unsafe_allow_html=True)

suby = float(3300)
strike = float(3500)
fval = datetime.datetime(2019, 12, 31)
fvto = datetime.datetime(2020, 12, 31)
vola = float(30.50)
tipo = float(-0.10)


uploaded_file = st.sidebar.file_uploader("Adjuntar datos de Murex", type="xlsx")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    suby = float(df.iloc[0,22])
    strike = float(df.iloc[0,23])
    #fval = datetime.datetime(int(df.iloc[0,0].strftime('%d-%m-%Y')))
    #fvto = df.iloc[0,14].strftime('%d-%m-%Y')
    vola = float(df.iloc[0,24])
    tipo = float(df.iloc[0,25])
    Card =  f'''<ul class="list-group">
              <li class="list-group-item d-flex justify-content-between align-items-center">
                Fecha Valoración
                <span class="badge badge-primary badge-pill">{df.iloc[0,0].strftime('%d-%m-%Y')}</span>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                Fecha Vencimiento
                <span class="badge badge-primary badge-pill">{df.iloc[0,14].strftime('%d-%m-%Y')}</span>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                Precio Subyacente
                <span class="badge badge-primary badge-pill">{df.iloc[0,22]}</span>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                Strike
                <span class="badge badge-primary badge-pill">{df.iloc[0,23]}</span>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                Volatilidad
                <span class="badge badge-primary badge-pill">{df.iloc[0,24]}</span>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                Tipo de Interés
                <span class="badge badge-primary badge-pill">{df.iloc[0,25]}</span>
              </li>
            </ul>'''
    st.sidebar.markdown(Card,unsafe_allow_html=True)


st.sidebar.header('Parámetros Challenge')

St = st.sidebar.number_input('Subyacente', 0.0, 10000.0, suby)  # index level
K = st.sidebar.number_input('Strike', 0.0, 10000.0, strike)  # option strike
#t = st.sidebar.number_input('Fecha Valoración', -1000, 1000, 0)  # valuation date
tcalc = st.sidebar.date_input( "Fecha de Valoración", fval)
tcalc2 = tcalc - today
tcalc3 = tcalc2.days
t = tcalc3 / 365
#Td = st.sidebar.number_input('Dias a Vencimiento', 0.00, 1000.00, 1.00)  # maturity date
Td = st.sidebar.date_input( "Fecha de Vencimiento",fvto)
DateCalc = Td - today
DateCalc2 = DateCalc.days
T = DateCalc2 / 365
rfr = st.sidebar.slider('Tipo Interés', -5.00, 10.00, tipo)  # risk-less short rate
r = rfr / 100
vol = st.sidebar.slider('Volatilidad', 0.00, 100.00, vola)  # volatility
sigma = vol / 100


#'''
# Calculadora de Opciones
#'''

#Descomentar esto si añadimos fichero para subir
#if uploaded_file is not None:
    #data = pd.read_csv(uploaded_file)
    #st.write('Estos son los datos cargados en el modelo:')
    #st.write(data)

def dN(x):
    ''' Probability density function of standard normal random variable x. '''
    return math.exp(-0.5 * x ** 2) / math.sqrt(2 * math.pi)


def N(d):
    ''' Cumulative density function of standard normal random variable x. '''
    return quad(lambda x: dN(x), -20, d, limit=50)[0]


def d1f(St, K, t, T, r, sigma):
    ''' Black-Scholes-Merton d1 function.
        Parameters see e.g. BSM_call_value function. '''
    d1 = (math.log(St / K) + (r + 0.5 * sigma ** 2)
          * (T - t)) / (sigma * math.sqrt(T - t))
    return d1

def BSM_call_value(St, K, t, T, r, sigma):
    ''' Calculates Black-Scholes-Merton European call option value.
    Parameters
    ==========
    St : float
        stock/index level at time t
    K : float
        strike price
    t : float
        valuation date
    T : float
        date of maturity/time-to-maturity if t = 0; T > t
    r : float
        constant, risk-less short rate
    sigma : float
        volatility
    Returns
    =======
    call_value : float
        European call present value at t
    '''
    d1 = d1f(St, K, t, T, r, sigma)
    d2 = d1 - sigma * math.sqrt(T - t)
    call_value = St * N(d1) - math.exp(-r * (T - t)) * K * N(d2)
    return call_value


def BSM_put_value(St, K, t, T, r, sigma):
    ''' Calculates Black-Scholes-Merton European put option value.
    Parameters
    ==========
    St : float
        stock/index level at time t
    K : float
        strike price
    t : float
        valuation date
    T : float
        date of maturity/time-to-maturity if t = 0; T > t
    r : float
        constant, risk-less short rate
    sigma : float
        volatility
    Returns
    =======
    put_value : float
        European put present value at t
    '''
    put_value = BSM_call_value(St, K, t, T, r, sigma) \
        - St + math.exp(-r * (T - t)) * K
    return put_value

def BSM_delta(St, K, t, T, r, sigma):
    ''' Black-Scholes-Merton DELTA of European call option.
    Parameters
    ==========
    St : float
        stock/index level at time t
    K : float
        strike price
    t : float
        valuation date
    T : float
        date of maturity/time-to-maturity if t = 0; T > t
    r : float
        constant, risk-less short rate
    sigma : float
        volatility
    Returns
    =======
    delta : float
        European call option DELTA
    '''
    d1 = d1f(St, K, t, T, r, sigma)
    delta = N(d1)
    return delta


def BSM_gamma(St, K, t, T, r, sigma):
    ''' Black-Scholes-Merton GAMMA of European call option.
    Parameters
    ==========
    St : float
        stock/index level at time t
    K : float
        strike price
    t : float
        valuation date
    T : float
        date of maturity/time-to-maturity if t = 0; T > t
    r : float
        constant, risk-less short rate
    sigma : float
        volatility
    Returns
    =======
    gamma : float
        European call option GAMM
    '''
    d1 = d1f(St, K, t, T, r, sigma)
    gamma = N(d1) / (St * sigma * math.sqrt(T - t))
    #gamma = dN(d1) / (St * sigma * math.sqrt(T - t))
    return gamma


def BSM_theta(St, K, t, T, r, sigma):
    ''' Black-Scholes-Merton THETA of European call option.
    Parameters
    ==========
    St : float
        stock/index level at time t
    K : float
        strike price
    t : float
        valuation date
    T : float
        date of maturity/time-to-maturity if t = 0; T > t
    r : float
        constant, risk-less short rate
    sigma : float
        volatility
    Returns
    =======
    theta : float
        European call option THETA
    '''
    d1 = d1f(St, K, t, T, r, sigma)
    d2 = d1 - sigma * math.sqrt(T - t)
    theta = (-(St * dN(d1) * sigma / (2 * math.sqrt(T - t)) +
              r * K * math.exp(-r * (T - t)) * N(d2)))/365
    return theta


def BSM_rho(St, K, t, T, r, sigma):
    ''' Black-Scholes-Merton RHO of European call option.
    Parameters
    ==========
    St : float
        stock/index level at time t
    K : float
        strike price
    t : float
        valuation date
    T : float
        date of maturity/time-to-maturity if t = 0; T > t
    r : float
        constant, risk-less short rate
    sigma : float
        volatility
    Returns
    =======
    rho : float
        European call option RHO
    '''
    d1 = d1f(St, K, t, T, r, sigma)
    d2 = d1 - sigma * math.sqrt(T - t)
    rho = K * (T - t) * math.exp(-r * (T - t)) * N(d2)
    return rho


def BSM_vega(St, K, t, T, r, sigma):
    ''' Black-Scholes-Merton VEGA of European call option.
    Parameters
    ==========
    St : float
        stock/index level at time t
    K : float
        strike price
    t : float
        valuation date
    T : float
        date of maturity/time-to-maturity if t = 0; T > t
    r : float
        constant, risk-less short rate
    sigma : float
        volatility
    Returns
    =======
    vega : float
        European call option VEGA
    '''
    d1 = d1f(St, K, t, T, r, sigma)
    vega = (St * dN(d1) * math.sqrt(T - t))/100
    return vega


#if st.sidebar.button('Introducir datos manualmente'):
st.write('')
st.markdown('---')

#st.write('El valor de la opción Call es: ', round(BSM_call_value(St, K, t, T, r, sigma), 2))
#st.write('El valor de la opción Put es: ', round(BSM_put_value(St, K, t, T, r, sigma), 2))

Opt = f'''<div class="card-columns">
  <div class="card text-center border-success mb-3" style="width: 08rem">
    <div class="card-header">Call</div>
    <div class="card-body">
      <p class="card-text">{BSM_call_value(St, K, t, T, r, sigma):,.4f}</p>
    </div>
  </div>
  <div class="card text-center border-success mb-3" style="width: 08rem">
    <div class="card-header">Put</div>
    <div class="card-body">
      <p class="card-text">{BSM_put_value(St, K, t, T, r, sigma):,.4f}</p>
    </div>
  </div>
</div>'''

st.markdown('El precio de las opciones es: ')
st.write('')
st.markdown(Opt,unsafe_allow_html=True)

st.markdown('---')
st.markdown('Resultados de las griegas:')
st.write('>**Delta:** ', BSM_delta(St, K, t, T, r, sigma))
st.write('>**Gamma:** ', BSM_gamma(St, K, t, T, r, sigma))
st.write('>**Theta:** ', BSM_theta(St, K, t, T, r, sigma))
st.write('>**Rho:** ', BSM_rho(St, K, t, T, r, sigma))
st.write('>**Vega:** ', BSM_vega(St, K, t, T, r, sigma))
st.write('')
st.write('')
if st.button('Iniciar cálculo del VaR'):
    chart_data = pd.DataFrame(
    np.random.randn(252, 1),
    columns=["PnL"])
    st.bar_chart(chart_data)
    VaR_90 = norm.ppf(1-0.9,0,0.05)
    VaR_95 = norm.ppf(1-0.95,0,0.05)
    VaR_99 = norm.ppf(1-0.99,0,0.05)
    st.write('>**VaR 90%:** ', VaR_90 * 1000000)
    st.write('>**VaR 95%:** ', VaR_95 * 1000000)
    st.write('>**VaR 99%:** ', VaR_99 * 1000000)
st.write('')
st.write('')
st.write('')
st.write('')
st.info("""\
        Hecho por: [Grant Thornton Spain](https://www.grantthornton.es/)
    """)
