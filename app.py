import os
import Mie
import Debye
import GOA
import streamlit as st

    


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

def compare_mie_debye():
    st.title("Compare Mie and Debye series")
    st.sidebar.title("Compare Mie and Debye")
    alpha = st.sidebar.slider("粒径参数", 1, 10000, 500, 2)
    rm = st.sidebar.slider("相对折射率实部", 0., 2., 0.78, step=0.001, format="%f")
    p = st.sidebar.slider("两debye阶数", 0, 16, (0,1))
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

    fig_mie = get_mie_fig(alpha, rm=rm, im=0.0, N_ta=N,figsize=(15, 6))
    st.pyplot(fig_mie)
    savefig(fig_mie, "save Mie figure")

    fig_debye = get_debye_fig(alpha, rm, im=0.0, p=p, N_ta=N, figsize=(15, 6))
    st.pyplot(fig_debye)
    savefig(fig_debye, "save Debye figure")

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
    st.pyplot(fig_goa)
    savefig(fig_goa, "save goa figure")

    fig_debye = get_debye_fig(alpha, rm, im=0.0, p=p, N_ta=N, figsize=(15, 6))
    st.pyplot(fig_debye)
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




