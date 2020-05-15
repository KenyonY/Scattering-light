import os
import Mie
import Debye
import GOA
import streamlit as st
from fourier import space2fre
space2fre = st.cache(func=space2fre, allow_output_mutation=True)

from typing import List
import numpy as np
from sciplot import plot, fillplot
import matplotlib.pyplot as plt
import plotly.express as px
from numpy import log

def drawMie():
    st.title("Draw Mie")
    st.sidebar.title("Mie")
    alpha = st.sidebar.slider("粒径参数alpha", 1, 10000, 500, 2)
    rm = st.sidebar.slider("相对折射率实部", 0., 2., 0.78, step=0.001, format="%f")
    N = st.sidebar.slider("采样数", 1800, 18000, 1800, 100)

    st.markdown(f"""
    当前: $\\alpha={alpha}$, $m={rm}$, $N={N}$
    """)

    @st.cache(allow_output_mutation=True)
    def get_mie_data(alpha, rm, im, N_ta, figsize=(15, 8)):
        fig = Mie.plotMie_dop(alpha, rm, im, N_ta, figsize)
        return fig
    fig = get_mie_data(alpha, rm = rm, im= 0.0, N_ta = N, figsize=(18, 12))
    st.pyplot(fig)


def savefig(fig, checkname="save figure"):
    if st.checkbox(f"{checkname}"):
        figpath = st.text_input("保存路径:", r'C:\Users\beidongjiedeguang\OneDrive\a_论文公式文件夹\公式图片\误差图\MieOrDebye.svg')
        if st.checkbox("save"):
            fig.savefig(figpath,
                        dpi=600, format=os.path.basename(figpath).split('.')[-1],
                        facecolor=fig.get_facecolor())
            st.text("File saved success!")

def drawDebye():
    st.title("Draw Debye")
    st.sidebar.title("Debye")
    alpha = st.sidebar.slider("粒径参数alpha", 1, 10000, 500, 2)
    rm = st.sidebar.slider("相对折射率实部", 0., 2., 0.78, step=0.001, format="%f")
    p = st.sidebar.slider("两debye阶数", 0, 16, (0,1))
    N = st.sidebar.slider("采样数", 1800, 28000, 1800, 100)

    f"""
    The current parameters: $\\alpha={alpha}$,  $m={rm}$,  $p={p}$,  $N={N}$
    """

    @st.cache(allow_output_mutation=True)
    def get_data(alpha, rm, im, p, N_ta,figsize):
        fig = Debye.plotData_multi(alpha, rm, im, p, N_ta, figsize)
        return fig

    fig = get_data(alpha, rm=rm, im=0., p=p, N_ta=N,figsize=(18, 12))
    st.pyplot(fig)
    savefig(fig, "save Debye")


def range_intensity(th_min, th_max, theta, i1, i2):
    idx1 = np.argwhere(theta <= th_max)
    idx2 = np.argwhere(theta >= th_min)
    idx=np.intersect1d(idx1, idx2)
    return theta[idx], i1[idx], i2[idx]

@st.cache(allow_output_mutation=True)
def get_data(mode="debye", **kwargs):
    """
    :arg mode: options: "debye" ,"mie", "goa"
    """

    if mode == "debye":
        theta, i1, i2 = Debye.superposition_intensity(**kwargs)
        check_key = "show debye"
    elif mode == "mie":
        theta, i1, i2 = Mie.intensity(**kwargs)
        check_key = "show mie"
    elif mode == "goa":
        theta, i1, i2 = GOA.superposition_intensity(**kwargs)
        check_key = "show goa"
    else:
        raise ValueError("mode illegal!")
    return theta, i1, i2

def compare_fourier(thetaI, I, theta_II, II, legend=["$Mie-I_1$", "$Debye-I_1$"]):
    freI, ampI = space2fre(thetaI, I)
    freII, ampII = space2fre(theta_II, II)
    fig = fillplot(freI, ampI)
    fig = fillplot(freII, ampII, fig, xlabel="Frequency", ylabel="Magnitude(Energy)",legend=legend)
    st.write(fig)

# def fourier(th_min, th_max, mode="debye", **kwargs):
#     """
#     :arg mode: options: "debye" ,"mie", "goa"
#     """
#
#     theta, i1, i2 = get_data(mode, **kwargs)
#     theta, i1, i2 = range_intensity(th_min, th_max, theta, i1, i2)
#
#     fre1, amp1 = space2fre(theta, i1)
#     fre2, amp2 = space2fre(theta, i2)

    # fig = plot(fre1, amp1)
    # fig = plot(fre2, (amp2), fig, xlabel="Frequency", ylabel="Amplitude")
    # fig = hist(fre1, amp1 , xlabel="Frequency", ylabel="Magnitude(Energy)")

    # fig = hist(fre2, amp2, xlabel="Frequency", ylabel="Magnitude(Energy)",legend="$I_2$")
    # st.write(fig)


def compare_mie_debye():
    st.title("Compare Mie and Debye series")
    st.sidebar.title("Compare Mie and Debye")
    alpha = st.sidebar.slider("粒径参数", 1, 10000, 500, 2)
    rm = st.sidebar.slider("相对折射率实部", 0., 2., 0.78, step=0.001, format="%f")
    p = st.sidebar.slider("两debye阶数", 0, 36, (0,1))
    N = st.sidebar.slider("采样数", 1800, 28000, 1800, 100)

    f"""
    The current parameters: $\\alpha={alpha}$, $m={rm}$, $p={p}$, $N={N}$
    """

    @st.cache(allow_output_mutation=True)
    def get_mie_fig(alpha, rm, im, N_ta,figsize):
        return Mie.plotMie(alpha, rm, im, N_ta, figsize)

    @st.cache(allow_output_mutation=True)
    def get_debye_fig(alpha, rm, im, p, N_ta, figsize):
        return Debye.plot_debye(alpha, rm, im, p, N_ta, figsize)

    fig_mie = get_mie_fig(alpha, rm, im=0.0, N_ta=N,figsize=(15, 6))
    savefig(fig_mie, "save Mie figure")
    st.pyplot(fig_mie)


    fig_debye = get_debye_fig(alpha, rm, im=0.0, p=p, N_ta=N, figsize=(15, 6))
    savefig(fig_debye, "save Debye figure")
    st.pyplot(fig_debye)


    th_min, th_max = st.slider("选择角度区间:", 0., 180.,(0., 180.), format="%f")


    theta, i1_mie, i2_mie = get_data(mode="mie", alpha=alpha, rm=rm, im=0.0, N_ta=N)
    theta_mie, I1_mie, I2_mie = range_intensity(th_min, th_max, theta, i1_mie, i2_mie)

    theta, i1_debye, i2_debye = get_data(mode="debye",alpha=alpha, rm=rm, im=0.0, p=p, N_ta=N)
    theta_debye, I1_debye, I2_debye = range_intensity(th_min, th_max, theta, i1_debye, i2_debye)

    "Fourier analyse - $I_1$"
    compare_fourier(theta_mie, I1_mie, theta_debye, I1_debye, legend=["$Mie-I_1$", "$Debye-I_1$"])
    "Fourier analyse - $I_2$"
    compare_fourier(theta_mie, I2_mie, theta_debye, I2_debye, legend=["$Mie-I_2$", "$Debye-I_2$"])

    theta, i1_goa, i2_goa = get_data(mode="goa",alpha=alpha, rm=rm, p=p, N_ta=N)
    theta_goa, I1_goa, I2_goa = range_intensity(th_min, th_max, theta, i1_goa, i2_goa)
    "Fourier analyse - $Mie-goa - I_1$"
    compare_fourier(theta_mie, I1_mie, theta_goa, I1_goa, legend=["$Mie-I_2$", "$GOA-I_1$"])
    "Fourier analyse - $Mie-goa - I_1$"
    compare_fourier(theta_mie, I2_mie, theta_goa, I2_goa, legend=["$Mie-I_2$", "$GOA-I_2$"])



def drawGOA():
    st.title("plot GOA")
    st.sidebar.title("GOA")
    alpha = st.sidebar.slider("粒径参数alpha", 1, 10000, 500, 2)
    rm = st.sidebar.slider("相对折射率实部", 0., 2., 0.78, step=0.001, format="%f")
    p = st.sidebar.slider("分波阶数", 0, 16, (0,1))
    N = st.sidebar.slider("采样数", 1800, 28000, 1800, 100)

    f"""
    The current parameters: $\\alpha={alpha}$,  $m={rm}$,  $p={p}$,  $N={N}$
    """

    @st.cache(allow_output_mutation=True)
    def get_data(alpha, rm, im, p, N_ta,figsize):
        fig = GOA.plot_multi(alpha, rm, p, N_ta, figsize)
        return fig

    fig = get_data(alpha, rm=rm, im=0., p=p, N_ta=N,figsize=(18, 10))
    st.pyplot(fig)
    savefig(fig, "save GOA")

def compare_debye_goa():
    st.title("Compare Debye series and GOA")
    st.sidebar.title("Compare Debye and GOA")
    alpha = st.sidebar.slider("粒径参数", 1, 10000, 500, 2)
    rm = st.sidebar.slider("相对折射率实部", 0., 2., 0.78, step=0.001, format="%f")
    p = st.sidebar.slider("分波阶数", 0, 16, (0,1))
    N = st.sidebar.slider("采样数", 1800, 28000, 1800, 100)

    f"""
    The current parameters: $\\alpha={alpha}$, $m={rm}$, $p={p}$, $N={N}$
    """

    @st.cache(allow_output_mutation=True)
    def get_goa_fig(alpha, rm, p, N_ta,figsize):
        return GOA.plot_goa(alpha, rm, p, N_ta, figsize)

    @st.cache(allow_output_mutation=True)
    def get_debye_fig(alpha, rm, im, p, N_ta, figsize):
        return Debye.plot_debye(alpha, rm, im, p, N_ta, figsize)

    fig_goa = get_goa_fig(alpha, rm, p, N_ta=N,figsize=(15, 6))
    st.write(fig_goa)
    savefig(fig_goa, "save goa figure")

    fig_debye = get_debye_fig(alpha, rm, im=0.0, p=p, N_ta=N, figsize=(15, 6))
    st.write(fig_debye)
    savefig(fig_debye, "save Debye figure")

def main():
    mode_list = ["Mie-DOP", "Debye","Mie-Debye", "GOA", "GOA-Debye"]
    mode = st.sidebar.selectbox("Choose the mode", mode_list)
    if mode == mode_list[0]:
        drawMie()
    elif mode == mode_list[1]:
        drawDebye()
    elif mode == mode_list[2]:
        compare_mie_debye()
    elif mode == mode_list[3]:
        drawGOA()
    elif mode == mode_list[4]:
        compare_debye_goa()

main()





