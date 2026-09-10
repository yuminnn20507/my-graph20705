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
st.write(
    "영화의 일별 박스오피스 데이터를 시간의 흐름에 따라 살펴봅니다."
)


# ============================================================
# 데이터 불러오기
# ============================================================

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():

    df = pd.read_csv(
        DATA_URL,
        encoding="utf-8-sig"
    )

    # 날짜를 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자 열을 숫자로 변환
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

    # 필요한 데이터가 없는 행 제거
    df = df.dropna(
        subset=["날짜", "영화명", "일관객"]
    )

    # 날짜순 정렬
    df = df.sort_values("날짜")

    return df


df = load_data()


# ============================================================
# 기본 정보
# ============================================================

st.caption(
    f"📊 총 {len(df):,}개의 일별 영화 기록을 불러왔습니다."
)


# ============================================================
# 그래프 1. 영화별 일관객 변화
# ============================================================

st.divider()

st.header("📈 그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화의 날짜별 일관객 수 변화를 확인할 수 있습니다."
)


# ------------------------------------------------------------
# 영화별 등장 횟수
# ------------------------------------------------------------

movie_counts = (
    df["영화명"]
    .value_counts()
    .sort_values(ascending=False)
)

movie_list = movie_counts.index.tolist()


# ------------------------------------------------------------
# 영화 선택
# ------------------------------------------------------------

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


# ------------------------------------------------------------
# 선택한 영화 데이터
# ------------------------------------------------------------

movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


# ------------------------------------------------------------
# 그래프 1
# ------------------------------------------------------------

fig1 = go.Figure()

fig1.add_trace(
    go.Scatter(
        x=movie_df["날짜"],
        y=movie_df["일관객"],
        mode="lines+markers",
        name=selected_movie,
        connectgaps=False,

        hovertemplate=(
            "날짜: %{x|%Y-%m-%d}"
            "<br>일관객: %{y:,.0f}명"
            "<extra></extra>"
        )
    )
)

fig1.update_layout(
    title=f"「{selected_movie}」 날짜별 일관객 변화",

    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)",

    xaxis=dict(
        type="date",
        tickformat="%Y-%m-%d",
        hoverformat="%Y-%m-%d"
    ),

    yaxis=dict(
        tickformat=","
    ),

    hovermode="x",

    height=500,

    margin=dict(
        l=40,
        r=40,
        t=70,
        b=40
    )
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


st.caption(
    f"이 영화는 전체 기간 중 {len(movie_df)}일 동안 10위권에 기록되었습니다."
)


# ============================================================
# 그래프 1 - 이 그래프로 알 수 있는 것
# ============================================================

st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.write(
    "영화의 일관객 수가 날짜에 따라 어떻게 증가하거나 감소하는지 확인할 수 있습니다."
)


# ============================================================
# 그래프 2. 일관객 합계 TOP 5 영화 비교
# ============================================================

st.divider()

st.header("📊 그래프 2. 일관객 합계 TOP 5 영화 비교")

st.write(
    "이 기간 동안 일관객의 합계가 가장 큰 5편의 영화가 날짜별로 "
    "어떻게 변화했는지 비교합니다."
)


# ------------------------------------------------------------
# 기간 전체의 일관객 합계 계산
# ------------------------------------------------------------

movie_total = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
)


# 일관객 합계가 가장 큰 5편
top5_movies = movie_total.head(5).index.tolist()


# ------------------------------------------------------------
# 그래프 2
# ------------------------------------------------------------

fig2 = go.Figure()


for movie in top5_movies:

    # 해당 영화의 날짜별 데이터
    movie_data = (
        df[df["영화명"] == movie]
        .groupby("날짜", as_index=False)["일관객"]
        .sum()
    )

    # 전체 기간의 모든 날짜를 만들어 줌
    # 영화가 그날 10위권에 없으면 NaN이 됨
    # → 그래프에서 선이 끊어짐
    all_dates = pd.date_range(
        start=df["날짜"].min(),
        end=df["날짜"].max(),
        freq="D"
    )

    movie_data = (
        movie_data
        .set_index("날짜")
        .reindex(all_dates)
        .rename_axis("날짜")
        .reset_index()
    )

    fig2.add_trace(
        go.Scatter(
            x=movie_data["날짜"],
            y=movie_data["일관객"],
            mode="lines+markers",
            name=movie,

            # 데이터가 없는 날짜는 선으로 연결하지 않음
            connectgaps=False,

            hovertemplate=(
                "영화: " + movie +
                "<br>날짜: %{x|%Y-%m-%d}" +
                "<br>일관객: %{y:,.0f}명" +
                "<extra></extra>"
            )
        )
    )


# ------------------------------------------------------------
# 그래프 2 모양 설정
# ------------------------------------------------------------

fig2.update_layout(
    title="일관객 합계가 가장 큰 5편의 날짜별 변화",

    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)",

    xaxis=dict(
        type="date",
        tickformat="%Y-%m-%d",
        hoverformat="%Y-%m-%d"
    ),

    yaxis=dict(
        tickformat=","
    ),

    hovermode="x unified",

    height=600,

    margin=dict(
        l=40,
        r=40,
        t=80,
        b=40
    ),

    # 범례를 그래프 위쪽에 배치
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    )
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# ------------------------------------------------------------
# TOP 5 영화의 일관객 합계 표시
# ------------------------------------------------------------

st.markdown("#### 🏆 이 기간 일관객 합계 TOP 5")

for i, movie in enumerate(top5_movies, start=1):

    total = movie_total[movie]

    st.write(
        f"{i}위. **{movie}** — "
        f"{total:,.0f}명"
    )


# ============================================================
# 그래프 2 - 이 그래프로 알 수 있는 것
# ============================================================

st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.write(
    "이 기간 동안 관객을 많이 모은 영화 5편의 흥행 규모와 날짜별 관객 변화 양상을 비교할 수 있습니다."
)


# ============================================================
# 그래프 3
# ============================================================

st.divider()

st.header("📊 그래프 3")

st.info(
    "앞으로 추가할 그래프 영역입니다."
)


# ============================================================
# 그래프 4
# ============================================================

st.divider()

st.header("📊 그래프 4")

st.info(
    "앞으로 추가할 그래프 영역입니다."
)
