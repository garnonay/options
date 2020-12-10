import streamlit as st
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, nbsp, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 63px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0,0,0,0),
        width=percent(100),
        height="auto",
        color="black",
        background_color="#f5f7f8",
        text_align="left",
        opacity=1
    )

    style_hr = styles(
        position="fixed",
        left=0,
        bottom=px(75),
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        #hr(
        #    style=style_hr
        #),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "&nbsp&nbsp Coded by ",
        link("https://www.grantthornton.es/", "Grant Thornton Spain"),
        br(),"&nbsp&nbsp",
        link("https://www.buymeacoffee.com/nonay",
            image('https://camo.githubusercontent.com/b18e4e33eb88215c17a5a66de3b51d92ce22cd7bbaf568561ecb0154ef3c1d76/68747470733a2f2f63646e2d696d616765732d312e6d656469756d2e636f6d2f6d61782f3733382f312a47393575796f6b4148344a433550707678344c6d6f514032782e706e67',
            height=px(20))),
    ]
    layout(*myargs)
