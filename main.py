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


movie_counts = (
    df["영화명"]
    .value_counts()
    .sort_values(ascending=False)
)

movie_list = movie_counts.index.tolist()

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


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


st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.write(
    "영화의 일관객 수가 날짜에 따라 어떻게 증가하거나 감소하는지 확인할 수 있습니다."
)


# ============================================================
# 그래프 2. 일관객 합계 TOP 5
# ============================================================

st.divider()

st.header("📊 그래프 2. 일관객 합계 TOP 5")

st.write(
    "이 기간 동안 일관객 합계가 가장 큰 5편의 영화가 "
    "날짜별로 어떻게 변화했는지 비교합니다."
)


movie_total = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
)

top5_movies = movie_total.head(5).index.tolist()


fig2 = go.Figure()

all_dates = pd.date_range(
    start=df["날짜"].min(),
    end=df["날짜"].max(),
    freq="D"
)


for movie in top5_movies:

    movie_data = (
        df[df["영화명"] == movie]
        .groupby("날짜")["일관객"]
        .sum()
    )

    movie_data = movie_data.reindex(all_dates)

    fig2.add_trace(
        go.Scatter(
            x=all_dates,
            y=movie_data,
            mode="lines+markers",
            name=movie,
            connectgaps=False,

            hovertemplate=(
                "영화: " + movie +
                "<br>날짜: %{x|%Y-%m-%d}" +
                "<br>일관객: %{y:,.0f}명" +
                "<extra></extra>"
            )
        )
    )


fig2.update_layout(
    title="일관객 합계가 가장 큰 5편의 날짜별 변화",

    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)",

    xaxis=dict(
        type="date",
        tickformat="%Y-%m-%d"
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


st.markdown("#### 🏆 이 기간 일관객 합계 TOP 5")

for i, movie in enumerate(top5_movies, start=1):

    st.write(
        f"{i}위. **{movie}** — "
        f"{movie_total[movie]:,.0f}명"
    )


st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.write(
    "이 기간 동안 관객을 많이 모은 영화 5편의 흥행 규모와 "
    "날짜별 관객 변화 양상을 비교할 수 있습니다."
)


# ============================================================
# 그래프 3. 날짜별 10위권 일관객 합계
# ============================================================

st.divider()

st.header("📊 그래프 3. 날짜별 10위권 일관객 합계")

st.write(
    "날짜별로 그날 박스오피스 10위권 영화의 일관객을 모두 더해 "
    "전체적인 영화 관객 규모의 변화를 확인합니다."
)


daily_total = (
    df.groupby("날짜")["일관객"]
    .sum()
    .reset_index()
    .sort_values("날짜")
)


top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("일관객", ascending=False)
)


fig3 = go.Figure()

fig3.add_trace(
    go.Scatter(
        x=daily_total["날짜"],
        y=daily_total["일관객"],
        mode="lines",
        name="10위권 일관객 합계",
        fill="tozeroy",

        hovertemplate=(
            "날짜: %{x|%Y-%m-%d}"
            "<br>10위권 일관객 합계: %{y:,.0f}명"
            "<extra></extra>"
        )
    )
)


for _, row in top3_days.iterrows():

    date = row["날짜"]
    total = row["일관객"]

    fig3.add_annotation(
        x=date,
        y=total,

        text=(
            f"<b>{date.strftime('%Y-%m-%d')}</b>"
            f"<br>{total:,.0f}명"
        ),

        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-60,

        font=dict(size=13),

        bgcolor="white",
        bordercolor="gray",
        borderwidth=1,
        borderpad=5
    )


fig3.update_layout(
    title="날짜별 10위권 일관객 합계",

    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계 (명)",

    xaxis=dict(
        type="date",
        tickformat="%Y-%m-%d"
    ),

    yaxis=dict(
        tickformat=","
    ),

    hovermode="x",
    height=550,

    margin=dict(
        l=40,
        r=40,
        t=100,
        b=40
    )
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


st.markdown("#### 🏆 일관객 합계가 가장 컸던 날")

for i, (_, row) in enumerate(
    top3_days.iterrows(),
    start=1
):

    st.write(
        f"{i}위. **{row['날짜'].strftime('%Y-%m-%d')}** — "
        f"{row['일관객']:,.0f}명"
    )


st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.write(
    "날짜별로 영화관 전체의 관객 규모가 어떻게 변했는지와 "
    "관객이 가장 많이 몰린 날이 언제였는지 확인할 수 있습니다."
)


# ============================================================
# 그래프 4. 영화별 일관객 합계 TOP 10
# ============================================================

st.divider()

st.header("📊 그래프 4. 영화별 일관객 합계 TOP 10")

st.write(
    "이 기간 동안 일관객을 가장 많이 모은 영화 10편을 비교합니다."
)


movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        기록일수=("날짜", "nunique")
    )
    .sort_values(
        "일관객합계",
        ascending=False
    )
)


top10_movies = movie_summary.head(10).copy()


fig4 = go.Figure()

fig4.add_trace(
    go.Bar(
        x=top10_movies["일관객합계"],
        y=top10_movies.index,
        orientation="h",

        name="일관객 합계",

        customdata=top10_movies["기록일수"],

        hovertemplate=(
            "영화: %{y}"
            "<br>일관객 합계: %{x:,.0f}명"
            "<br>10위권 기록 일수: %{customdata}일"
            "<extra></extra>"
        )
    )
)


fig4.update_layout(
    title="영화별 일관객 합계 TOP 10",

    xaxis_title="일관객 합계 (명)",
    yaxis_title="영화",

    xaxis=dict(
        tickformat=","
    ),

    yaxis=dict(
        autorange="reversed"
    ),

    height=600,

    margin=dict(
        l=40,
        r=40,
        t=80,
        b=40
    )
)

st.plotly_chart(
    fig4,
    use_container_width=True
)


st.markdown("#### 🏆 일관객 합계 TOP 10")

for i, (movie, row) in enumerate(
    top10_movies.iterrows(),
    start=1
):

    st.write(
        f"{i}위. **{movie}** — "
        f"{row['일관객합계']:,.0f}명 "
        f"({row['기록일수']}일)"
    )


st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.write(
    "이 기간 동안 어떤 영화가 가장 많은 관객을 모았는지와 "
    "각 영화가 10위권에 얼마나 오래 머물렀는지를 비교할 수 있습니다."
)


# ============================================================
# 그래프 5. 월 × 요일별 일관객 합계
# ============================================================

st.divider()

st.header("📊 그래프 5. 월 × 요일별 일관객 합계")

st.write(
    "날짜의 월과 요일을 기준으로 10위권 일관객 합계를 비교합니다."
)


# ------------------------------------------------------------
# 월과 요일 추출
# ------------------------------------------------------------

heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month
heatmap_df["요일번호"] = heatmap_df["날짜"].dt.weekday


weekday_names = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]


heatmap_df["요일"] = heatmap_df["요일번호"].map(
    lambda x: weekday_names[x]
)


# ------------------------------------------------------------
# 월 × 요일별 일관객 합계
# ------------------------------------------------------------

heatmap_data = (
    heatmap_df
    .groupby(["월", "요일번호", "요일"])["일관객"]
    .sum()
    .reset_index()
)


# ------------------------------------------------------------
# 히트맵 표 만들기
# ------------------------------------------------------------

heatmap_pivot = (
    heatmap_data
    .pivot(
        index="월",
        columns="요일번호",
        values="일관객"
    )
    .reindex(
        index=range(1, 13),
        columns=range(7)
    )
)


# ------------------------------------------------------------
# 히트맵
# ------------------------------------------------------------

fig5 = go.Figure()

fig5.add_trace(
    go.Heatmap(
        x=weekday_names,

        y=[
            f"{month}월"
            for month in range(1, 13)
        ],

        z=heatmap_pivot.values,

        colorscale="Blues",

        hovertemplate=(
            "%{y} %{x}"
            "<br>일관객 합계: %{z:,.0f}명"
            "<extra></extra>"
        ),

        colorbar=dict(
            title="일관객<br>합계"
        )
    )
)


fig5.update_layout(
    title="월 × 요일별 10위권 일관객 합계",

    xaxis_title="요일",
    yaxis_title="월",

    height=650,

    margin=dict(
        l=50,
        r=50,
        t=80,
        b=50
    )
)


st.plotly_chart(
    fig5,
    use_container_width=True
)


st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.write(
    "어떤 달과 요일에 영화 관객이 많이 몰렸는지 한눈에 비교할 수 있습니다."
)


# ============================================================
# 그래프 6
# ============================================================

st.divider()

st.header("📊 그래프 6")

st.info(
    "앞으로 추가할 그래프 영역입니다."
)
