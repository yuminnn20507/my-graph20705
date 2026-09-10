# ============================================================
# 그래프 5. 월 × 요일별 일관객 합계 히트맵
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

# 월
heatmap_df["월"] = heatmap_df["날짜"].dt.month

# 요일
# pandas: 월요일=0, 화요일=1, ... 일요일=6
weekday_names = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

heatmap_df["요일번호"] = heatmap_df["날짜"].dt.weekday
heatmap_df["요일"] = heatmap_df["요일번호"].map(
    lambda x: weekday_names[x]
)


# ------------------------------------------------------------
# 월 × 요일별 일관객 합계 계산
# ------------------------------------------------------------

heatmap_data = (
    heatmap_df
    .groupby(["월", "요일번호", "요일"])["일관객"]
    .sum()
    .reset_index()
)


# ------------------------------------------------------------
# 히트맵용 표 만들기
# ------------------------------------------------------------

heatmap_pivot = (
    heatmap_data
    .pivot(
        index="월",
        columns="요일번호",
        values="일관객"
    )
)

# 월요일 → 일요일 순서로 정렬
heatmap_pivot = heatmap_pivot.reindex(
    columns=range(7)
)

# 1월 → 12월 순서
heatmap_pivot = heatmap_pivot.reindex(
    index=range(1, 13)
)


# ------------------------------------------------------------
# Plotly 히트맵
# ------------------------------------------------------------

fig5 = go.Figure()


fig5.add_trace(
    go.Heatmap(
        x=weekday_names,
        y=[f"{month}월" for month in heatmap_pivot.index],
        z=heatmap_pivot.values,

        colorscale="Blues",

        # 마우스를 올렸을 때 표시
        customdata=[
            [
                heatmap_pivot.iloc[row, col]
                for col in range(7)
            ]
            for row in range(len(heatmap_pivot))
        ],

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


# ------------------------------------------------------------
# 그래프 모양 설정
# ------------------------------------------------------------

fig5.update_layout(
    title="월 × 요일별 10위권 일관객 합계",

    xaxis_title="요일",
    yaxis_title="월",

    xaxis=dict(
        categoryorder="array",
        categoryarray=weekday_names
    ),

    yaxis=dict(
        categoryorder="array",
        categoryarray=[f"{month}월" for month in range(1, 13)]
    ),

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


# ============================================================
# 그래프 5 - 이 그래프로 알 수 있는 것
# ============================================================

st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.write(
    "어떤 달과 요일에 영화 관객이 많이 몰렸는지 한눈에 비교할 수 있습니다."
)
