import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ============================================================
# 페이지 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("영화의 일별 박스오피스 데이터를 시간의 흐름에 따라 살펴봅니다.")


# ============================================================
# 데이터 불러오기
# ============================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜 열을 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자 데이터는 숫자 형식으로 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # 날짜가 잘못된 행 제거
    df = df.dropna(subset=["날짜", "영화명"])

    # 날짜 순서대로 정렬
    df = df.sort_values("날짜")

    return df


df = load_data()


# ============================================================
# 데이터 기본 확인
# ============================================================

st.caption(
    f"📊 총 {len(df):,}개의 기록을 불러왔습니다."
)


# ============================================================
# 그래프 1. 영화별 일관객 변화
# ============================================================

st.divider()
st.header("📈 그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화의 날짜별 일관객 수 변화를 확인할 수 있습니다."
)


# 영화 목록 만들기
movie_list = sorted(
    df["영화명"].dropna().unique().tolist()
)


selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


# 선택한 영화의 데이터만 추출
movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


# ------------------------------------------------------------
# Plotly 선 그래프
# ------------------------------------------------------------

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=movie_df["날짜"],
        y=movie_df["일관객"],
        mode="lines+markers",
        name=selected_movie,
        hovertemplate=(
            "날짜: %{x|%Y-%m-%d}"
            "<br>일관객: %{y:,.0f}명"
            "<extra></extra>"
        )
    )
)

fig.update_layout(
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)",
    hovermode="x unified",
    height=500,
    margin=dict(l=40, r=40, t=70, b=40)
)

fig.update_yaxes(
    tickformat=","
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ------------------------------------------------------------
# 이 그래프로 알 수 있는 것
# ------------------------------------------------------------

st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.write(
    "여기에 이 그래프를 통해 알 수 있는 내용을 작성하세요."
)


# ============================================================
# 그래프 2. 앞으로 추가할 그래프
# ============================================================

st.divider()
st.header("📊 그래프 2")

st.info(
    "앞으로 추가할 그래프 영역입니다."
)


# ============================================================
# 그래프 3. 앞으로 추가할 그래프
# ============================================================

st.divider()
st.header("📊 그래프 3")

st.info(
    "앞으로 추가할 그래프 영역입니다."
)


# ============================================================
# 그래프 4. 앞으로 추가할 그래프
# ============================================================

st.divider()
st.header("📊 그래프 4")

st.info(
    "앞으로 추가할 그래프 영역입니다."
)
