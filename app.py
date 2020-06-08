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

import plotly.graph_objects as go
from numpy import log
from guang.sci.utils import culc_frequency
from guang.sci.scattering import get_k1k2, predict

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
        figpath = st.text_input("保存路径:",
                                r'C:\Users\beidongjiedeguang\OneDrive\a_论文公式文件夹\公式图片\误差图\MieOrDebye.svg')
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

@st.cache
def getting_data(mode="debye", **kwargs):
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


def compare_mie_debye():
    st.title("Compare Mie and Debye series")
    st.sidebar.title("Compare Mie and Debye")
    alpha = st.sidebar.slider("粒径参数", 1, 10000, 500, 2)
    rm = st.sidebar.slider("相对折射率实部", 0., 2., 0.78, step=0.001, format="%f")
    p = st.sidebar.slider("两debye阶数", 0, 36, (0,1))
    N = st.sidebar.slider("采样数", 1800, 28000, 1800, 100)
    show_critial_angle = st.sidebar.selectbox("show critical angle",(False, True))
    show_brewster_angle = st.sidebar.selectbox("show brewster angle",(False, True))

    f"""
    The current parameters: $\\alpha={alpha}$, $m={rm}$, $p={p}$, $N={N}$
    """

    @st.cache(allow_output_mutation=True)
    def get_mie_fig(alpha, rm, im, N_ta,figsize):
        return Mie.plotMie(alpha, rm, im, N_ta, figsize,
                           show_critial_angle, show_brewster_angle)

    @st.cache(allow_output_mutation=True)
    def get_debye_fig(alpha, rm, im, p, N_ta, figsize):
        return Debye.plot_debye(alpha, rm, im, p, N_ta, figsize,
                                show_critial_angle, show_brewster_angle)

    fig_mie = get_mie_fig(alpha, rm, im=0.0, N_ta=N,figsize=(15, 6))
    savefig(fig_mie, "save Mie figure")
    st.pyplot(fig_mie)


    fig_debye = get_debye_fig(alpha, rm, im=0.0, p=p, N_ta=N, figsize=(15, 6))
    savefig(fig_debye, "save Debye figure")
    st.pyplot(fig_debye)

    th_min, th_max = st.slider("选择角度区间:", 0., 180.,(0., 180.), format="%f")

    theta_MIE, i1_mie, i2_mie = getting_data(mode="mie", alpha=alpha, rm=rm, im=0.0, N_ta=N)
    theta_mie, I1_mie, I2_mie = range_intensity(th_min, th_max, theta_MIE, i1_mie, i2_mie)

    theta_DEBYE, i1_debye, i2_debye = getting_data(mode="debye",alpha=alpha, rm=rm, im=0.0, p=p, N_ta=N)
    theta_debye, I1_debye, I2_debye = range_intensity(th_min, th_max, theta_DEBYE, i1_debye, i2_debye)

    theta_GOA, i1_goa, i2_goa = getting_data(mode="goa",alpha=alpha, rm=rm, p=p, N_ta=N)
    theta_goa, I1_goa, I2_goa = range_intensity(th_min, th_max, theta_GOA, i1_goa, i2_goa)

    "Fourier analyse - $I_1$"
    compare_fourier(theta_mie, I1_mie, theta_debye, I1_debye, legend=["$Mie-I_1$", "$Debye-I_1$"])
    "Fourier analyse - $I_2$"
    compare_fourier(theta_mie, I2_mie, theta_debye, I2_debye, legend=["$Mie-I_2$", "$Debye-I_2$"])

    "Fourier analyse - $Mie-goa - I_1$"
    compare_fourier(theta_mie, I1_mie, theta_goa, I1_goa, legend=["$Mie-I_1$", "$GOA-I_1$"])
    "Fourier analyse - $Mie-goa - I_2$"
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

def mie_plotly():
    st.title("m>1")
    # st.sidebar.title("My Algorithm(m>1)")
    alpha = st.sidebar.slider("粒径参数alpha", 1, 5000, 1627, 1)
    rm = st.sidebar.slider("相对折射率实部", 1.301, 1.399, 1.334, step=0.0002, format="%f")
    N = st.sidebar.slider("采样数", 1800, 28000, 16000, 100)

    st.markdown(f"""
    当前: $\\alpha={alpha}$, $m={rm}$, $N={N}$
    """)

    theta_MIE, i1_mie, i2_mie = getting_data(mode="mie", alpha=alpha, rm=rm, im=0.0, N_ta=N)


    fig1 = go.Figure(go.Scatter(x=theta_MIE, y=np.log(i1_mie), name='i1'))
    fig1.add_trace(go.Scatter(x=theta_MIE, y=np.log(i2_mie), name='i2'))
    fig1

    theta1 = st.number_input('theta 1', 0., 180., 14.5)
    dth16 = st.number_input('the range of theta_1(degree)', 0., 180., 4.14)

    theta2 = st.number_input('theta 2', 0., 180., 60.)
    dth62 = st.number_input('the range of theta_2(degree)', 0., 180., 3.26)
    # dth16, dth62 = 4.14, 3.26
    th_min= theta1-dth16/2
    th_max =theta1+dth16/2

    theta_mie, I1_mie, I2_mie = range_intensity(th_min, th_max, theta_MIE, i1_mie, i2_mie)
    fig2 = go.Figure(go.Scatter(x=theta_mie, y=np.log(I1_mie), name="i1"))
    fig2.add_trace(go.Scatter(x=theta_mie, y=np.log(I2_mie), name='i2'))
    fig2
    fre1_i1 = culc_frequency(theta_mie, I1_mie)[0]
    fre1_i2 = culc_frequency(theta_mie, I2_mie)[0]
    f"$i_1$频率: $v_{{\\theta_1}}$：{fre1_i1}"
    f"$i_2$频率$v_{{\\theta_1}}$：{fre1_i2}"


    th_min= theta2-dth62/2
    th_max =theta2+dth62/2
    theta_mie, I1_mie, I2_mie = range_intensity(th_min, th_max, theta_MIE, i1_mie, i2_mie)
    fig3 = go.Figure(go.Scatter(x=theta_mie, y=np.log(I1_mie), name="i1"))
    fig3.add_trace(go.Scatter(x=theta_mie, y=np.log(I2_mie), name='i2'))
    fig3
    fre2_i1 = culc_frequency(theta_mie, I1_mie)[0]
    fre2_i2 = culc_frequency(theta_mie, I2_mie)[0]
    f"$i_1$频率$v_{{\\theta_2}}$：{fre2_i1}"
    f"$i_2$频率$v_{{\\theta_2}}$：{fre2_i2}"
    "---"
    f"$i_1:$ $\\frac{{k_{{\\theta_1}}}}{{k_{{\\theta_2}}}} = \\frac{{v_{{\\theta_1}}}}{{v_{{\\theta_2}}}}=$ {fre1_i1/fre2_i1}"

    k1, k2 = get_k1k2(theta1-dth16/2, theta2-dth62/2, dth16, dth62)
    test_m = np.linspace(1.31, 1.39, 200)
    "由论文中算法计算得到的 m从1.31-1.39范围内$\\frac{{k_{{\\theta_1}}}}{{k_{{\\theta_2}}}}$的变化情况(对应论文中$R_{{i,j}}(m)$):"
    fig4 = go.Figure(go.Scatter(x=test_m, y=k1(test_m)/k2(test_m), name="k1/k2"))
    fig4
    "使用$i_1$频率反演折射率与粒径：(m: 1.301~1.399 )"
    alpha1_p,alpha2_p, m_p = predict(fre1_i1,fre2_i1, k1, k2)
    f"$\\alpha_{1}=$ {alpha1_p:.3f}, $\\alpha_{2}=$ {alpha2_p:.3f}, $m=$ {m_p:.9f}"
    "注：这里是为了演示，所有计算均直接使用输入的角度区间，" \
    "而对其没有重新计算，所以对于粒径较小时结果不准确"




def main():
    mode_list = ["Mie-DOP", "Debye","Mie-Debye", "GOA", "GOA-Debye", "paper test(m>1)"]
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
    elif mode == mode_list[5]:
        mie_plotly()

main()





