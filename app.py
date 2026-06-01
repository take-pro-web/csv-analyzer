import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

st.set_page_config(page_title="CSV分析ツール", layout="wide")
st.title("📊 CSV自動分析ツール")
st.caption("CSVをアップロードするだけで自動でグラフ・統計を表示します")

uploaded = st.file_uploader("CSVファイルをアップロード", type="csv")

if uploaded:
    df = pd.read_csv(uploaded, encoding="utf-8")
    
    st.subheader("📋 データ一覧")
    st.dataframe(df, use_container_width=True)

    num_cols = df.select_dtypes(include="number").columns.tolist()
    
    if num_cols:
        st.subheader("📐 統計サマリー")
        st.dataframe(df[num_cols].describe(), use_container_width=True)

        st.subheader("📈 グラフ")
        col1, col2, col3 = st.columns(3)
        x_col = col1.selectbox("X軸", df.columns.tolist())
        y_col = col2.selectbox("Y軸", num_cols)
        chart = col3.selectbox("グラフ種類", ["折れ線", "棒グラフ"])

        fig, ax = plt.subplots(figsize=(10, 4))
        if chart == "折れ線":
            ax.plot(df[x_col].astype(str), df[y_col], marker="o", color="#00b4d8")
        else:
            ax.bar(df[x_col].astype(str), df[y_col], color="#00b4d8")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
else:
    st.info("← 左のメニューからCSVをアップロードしてください")
