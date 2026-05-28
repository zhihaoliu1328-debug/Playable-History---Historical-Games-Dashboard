from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


DATA_PATH = Path("data/cleaned_games_playable_history.csv")

PARCHMENT = "#F7EFD9"
INK_NAVY = "#162436"
BURGUNDY = "#7B2038"
TEAL = "#287C87"
GOLD = "#D09A2D"
MOSS = "#6F7F45"
DARK_TEXT = "#201C18"

TYPE_COLORS = {
    "Command history": BURGUNDY,
    "Lived history": TEAL,
    "Hybrid history": GOLD,
    "Low-tag / mixed": MOSS,
    "Mixed / unclear": MOSS,
}

COMMAND_MODES = [
    ("Warfare / conflict", "has_warfare"),
    ("Strategy / system", "has_strategy_system"),
    ("Management / economy", "has_management_economy"),
    ("Empire / expansion", "has_empire_expansion"),
    ("Politics / diplomacy", "has_politics_diplomacy"),
]

LIVED_MODES = [
    ("Society / culture", "has_society_culture"),
    ("Narrative / adventure", "has_narrative_adventure"),
    ("Open world / sandbox", "has_open_world_sandbox"),
]


st.set_page_config(
    page_title="Playable History",
    page_icon="P",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    for col in ["release_year", "rating", "command_control_score", "lived_experience_score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in [c for c in df.columns if c.startswith("has_")]:
        if df[col].dtype == bool:
            continue
        df[col] = df[col].astype(str).str.strip().str.lower().isin(
            ["true", "1", "yes", "y"]
        )

    for col in ["main_genre", "historical_play_type", "title"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown").astype(str)

    return df


def apply_theme() -> None:
    st.markdown(
        f"""
        <style>
        :root {{
            --parchment: {PARCHMENT};
            --ink-navy: {INK_NAVY};
            --burgundy: {BURGUNDY};
            --teal: {TEAL};
            --gold: {GOLD};
            --moss: {MOSS};
            --dark-text: {DARK_TEXT};
        }}

        .stApp {{
            background:
                linear-gradient(rgba(247, 239, 217, 0.92), rgba(247, 239, 217, 0.92)),
                repeating-linear-gradient(0deg, rgba(32, 28, 24, 0.035) 0px,
                rgba(32, 28, 24, 0.035) 1px, transparent 1px, transparent 5px);
            color: var(--dark-text);
        }}

        [data-testid="stSidebar"] {{
            display: none;
        }}

        [data-testid="collapsedControl"] {{
            display: none;
        }}

        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            color: var(--ink-navy);
            letter-spacing: 0;
        }}

        .block-container {{
            padding-top: 2.2rem;
            padding-bottom: 3rem;
            max-width: 1220px;
        }}

        .hero-kicker {{
            color: var(--burgundy);
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }}

        .hero-title {{
            color: var(--ink-navy);
            font-family: Georgia, 'Times New Roman', serif;
            font-size: clamp(3rem, 6vw, 5.8rem);
            font-weight: 700;
            line-height: 0.95;
            margin-bottom: 0.35rem;
        }}

        .hero-subtitle {{
            color: var(--dark-text);
            font-size: 1.25rem;
            max-width: 760px;
            margin-bottom: 1.15rem;
        }}

        .thesis-box, .dataset-box, .method-box {{
            background: rgba(255, 250, 235, 0.68);
            border: 1px solid rgba(22, 36, 54, 0.22);
            border-left: 6px solid var(--gold);
            padding: 1rem 1.15rem;
            box-shadow: 0 8px 28px rgba(32, 28, 24, 0.07);
        }}

        .section-heading {{
            color: var(--ink-navy);
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.18;
            margin-top: 2.45rem;
            margin-bottom: 1rem;
        }}

        .concept-card {{
            min-height: 220px;
            background: rgba(255, 250, 235, 0.62);
            border: 1px solid rgba(22, 36, 54, 0.22);
            padding: 1.25rem;
            box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.3);
        }}

        .concept-card.command {{
            border-top: 7px solid var(--burgundy);
        }}

        .concept-card.lived {{
            border-top: 7px solid var(--teal);
        }}

        .card-title {{
            font-family: Georgia, 'Times New Roman', serif;
            font-size: 1.8rem;
            font-weight: 700;
            line-height: 1.1;
            margin: 0 0 0.7rem 0;
            color: var(--ink-navy);
        }}

        .concept-card p {{
            font-size: 1rem;
            line-height: 1.48;
        }}

        .keywords {{
            color: var(--ink-navy);
            font-size: 0.92rem;
            font-weight: 700;
            margin-top: 1rem;
        }}

        .small-note {{
            color: rgba(32, 28, 24, 0.78);
            font-size: 0.93rem;
            line-height: 1.45;
        }}

        .dataset-box {{
            border-left-color: var(--moss);
            margin-top: 0.9rem;
        }}

        .contrast-band {{
            display: grid;
            grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
            align-items: center;
            gap: 0.85rem;
            margin: 1rem 0 0.25rem 0;
        }}

        .contrast-pole {{
            min-height: 70px;
            padding: 0.9rem 1rem;
            color: #fffaf0;
            font-weight: 800;
            border: 1px solid rgba(22, 36, 54, 0.18);
        }}

        .contrast-pole.command {{
            background: var(--burgundy);
            text-align: right;
        }}

        .contrast-pole.lived {{
            background: var(--teal);
        }}

        .contrast-arrow {{
            color: var(--ink-navy);
            font-size: 2rem;
            font-weight: 900;
        }}

        .footprint {{
            display: flex;
            gap: 0.55rem;
            align-items: stretch;
            margin: 1rem 0 0.85rem 0;
        }}

        .footprint-tile {{
            min-width: 5.8rem;
            padding: 0.8rem 0.85rem;
            color: #fffaf0;
            border: 1px solid rgba(255, 250, 235, 0.62);
            box-shadow: 0 8px 22px rgba(32, 28, 24, 0.08);
        }}

        .footprint-tile.zero {{
            color: var(--gold);
            background: rgba(255, 250, 235, 0.58) !important;
            border-color: var(--gold);
            box-shadow: none;
        }}

        .footprint-label {{
            font-size: 0.85rem;
            font-weight: 800;
            line-height: 1.2;
        }}

        .footprint-count {{
            font-family: Georgia, 'Times New Roman', serif;
            font-size: 1.75rem;
            font-weight: 700;
            line-height: 1;
            margin-top: 0.3rem;
        }}

        div[data-testid="stMetric"] {{
            background: rgba(255, 250, 235, 0.58);
            border: 1px solid rgba(22, 36, 54, 0.18);
            padding: 0.75rem 0.9rem;
        }}

        div[data-testid="stDataFrame"] {{
            border: 1px solid rgba(22, 36, 54, 0.18);
        }}

        .stRadio label, .stSelectbox label, .stMultiSelect label, .stSlider label {{
            color: var(--ink-navy) !important;
            font-weight: 700;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_heading(text: str) -> None:
    st.markdown(f'<div class="section-heading">{text}</div>', unsafe_allow_html=True)


def playable_region(row: pd.Series) -> str:
    command = row["command_control_score"]
    lived = row["lived_experience_score"]
    if pd.isna(command) or pd.isna(lived):
        return "Low-tag / mixed"
    if command > 2.5 and lived >= 1.5:
        return "Hybrid history"
    if command > 2.5:
        return "Command history"
    if lived >= 1.5:
        return "Lived history"
    return "Low-tag / mixed"


def category_display_label(category: str) -> str:
    if category == "Lived history":
        return "Experiential history"
    if category == "Low-tag / mixed":
        return "Mixed / low signal"
    return category


def category_value_from_display(category: str) -> str:
    if category == "Experiential history":
        return "Lived history"
    return category


def category_counts(df: pd.DataFrame) -> pd.DataFrame:
    categories = [
        "Command history",
        "Hybrid history",
        "Lived history",
        "Low-tag / mixed",
    ]
    if df.empty:
        return pd.DataFrame({"category": categories, "count": [0, 0, 0, 0]})

    regions = df.apply(playable_region, axis=1)
    counts = regions.value_counts().reindex(categories, fill_value=0).reset_index()
    counts.columns = ["category", "count"]
    return counts


def render_category_footprint(df: pd.DataFrame) -> None:
    counts = category_counts(df)
    total = max(int(counts["count"].sum()), 1)
    tiles = []
    for _, row in counts.iterrows():
        category = row["category"]
        count = int(row["count"])
        percent = count / total * 100
        visual_width = 5 if count == 0 else max(percent, 12)
        color = TYPE_COLORS.get(category, MOSS)
        label = category_display_label(category)
        zero_class = " zero" if count == 0 else ""
        tiles.append(
            f'<div class="footprint-tile{zero_class}" style="flex: {visual_width:.1f} 1 0; background: {color};">'
            f'<div class="footprint-label">{label}</div>'
            f'<div class="footprint-count">{count}</div>'
            f'<div>{percent:.0f}% of games in view</div>'
            f'</div>'
        )

    st.markdown(f'<div class="footprint">{"".join(tiles)}</div>', unsafe_allow_html=True)


def styled_plotly_layout(fig: go.Figure, height: int) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,250,235,0.55)",
        font=dict(color=DARK_TEXT, family="Georgia, Times New Roman, serif"),
        height=height,
        margin=dict(l=20, r=24, t=34, b=30),
        hoverlabel=dict(
            bgcolor="#fff8e5",
            bordercolor=INK_NAVY,
            font=dict(color=DARK_TEXT, family="Arial, sans-serif"),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor="rgba(0,0,0,0)",
        ),
    )
    fig.update_xaxes(
        gridcolor="rgba(22,36,54,0.15)",
        zerolinecolor="rgba(22,36,54,0.36)",
        linecolor="rgba(22,36,54,0.45)",
        title_font=dict(color=INK_NAVY),
    )
    fig.update_yaxes(
        gridcolor="rgba(22,36,54,0.11)",
        linecolor="rgba(22,36,54,0.45)",
        title_font=dict(color=INK_NAVY),
    )
    return fig


def title_list(series: pd.Series, limit: int = 14) -> str:
    titles = [str(title) for title in series.dropna().sort_values()]
    shown = titles[:limit]
    extra = len(titles) - len(shown)
    text = "<br>".join(shown)
    if extra > 0:
        text += f"<br>... and {extra} more"
    return text


def dominant_type(series: pd.Series) -> str:
    counts = series.value_counts()
    if counts.empty:
        return "Mixed / unclear"
    return str(counts.index[0])


def build_grid_cells(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby(["command_control_score", "lived_experience_score"], dropna=False)
        .agg(
            games=("title", "size"),
            avg_rating=("rating", "mean"),
            titles=("title", title_list),
            dominant_play_type=("historical_play_type", dominant_type),
        )
        .reset_index()
        .dropna(subset=["command_control_score", "lived_experience_score"])
    )

    if grouped.empty:
        return grouped

    grouped["label"] = grouped["games"].apply(lambda value: f"{int(value)} games")
    grouped["grid_category"] = grouped.apply(playable_region, axis=1)
    grouped["grid_category_label"] = grouped["grid_category"].map(category_display_label)
    grouped["color"] = grouped["grid_category"].map(TYPE_COLORS).fillna(MOSS)
    grouped["avg_rating_label"] = grouped["avg_rating"].map(
        lambda value: "Not rated" if pd.isna(value) else f"{value:.2f}"
    )
    grouped["hover_text"] = grouped.apply(
        lambda row: (
            f"Command/control score: {row['command_control_score']}<br>"
            f"Lived/experiential score: {row['lived_experience_score']}<br>"
            f"Games: {int(row['games'])}<br>"
            f"Average rating: {row['avg_rating_label']}<br>"
            f"Grid category: {row['grid_category_label']}<br>"
            f"Dominant data label: {row['dominant_play_type']}<br><br>"
            f"{row['titles']}"
        ),
        axis=1,
    )
    return grouped


def add_grid_backdrop(fig: go.Figure) -> None:
    fig.add_shape(
        type="rect",
        x0=-0.45,
        x1=2.5,
        y0=-0.35,
        y1=1.5,
        fillcolor=MOSS,
        opacity=0.08,
        line_width=0,
        layer="below",
        showlegend=False,
    )
    fig.add_shape(
        type="rect",
        x0=2.5,
        x1=5.45,
        y0=-0.35,
        y1=1.5,
        fillcolor=BURGUNDY,
        opacity=0.08,
        line_width=0,
        layer="below",
        showlegend=False,
    )
    fig.add_shape(
        type="rect",
        x0=-0.45,
        x1=2.5,
        y0=1.5,
        y1=2.45,
        fillcolor=TEAL,
        opacity=0.08,
        line_width=0,
        layer="below",
        showlegend=False,
    )
    fig.add_shape(
        type="rect",
        x0=2.5,
        x1=5.45,
        y0=1.5,
        y1=2.45,
        fillcolor=GOLD,
        opacity=0.08,
        line_width=0,
        layer="below",
        showlegend=False,
    )


def add_grid_annotations(fig: go.Figure, df: pd.DataFrame) -> None:
    count_map = {
        row["category"]: int(row["count"])
        for _, row in category_counts(df).iterrows()
    }

    fig.add_annotation(
        x=4.25,
        y=0.25,
        text=f"Command history<br>{count_map.get('Command history', 0)} games<br>war / empire / control",
        showarrow=False,
        font=dict(color=BURGUNDY, size=13),
        bgcolor="rgba(255,250,235,0.74)",
        bordercolor=BURGUNDY,
        borderwidth=1,
    )
    fig.add_annotation(
        x=4.15,
        y=2.15,
        text=f"Hybrid history<br>{count_map.get('Hybrid history', 0)} games<br>systems + lived experience",
        showarrow=False,
        font=dict(color=GOLD, size=13),
        bgcolor="rgba(255,250,235,0.74)",
        bordercolor=GOLD,
        borderwidth=1,
    )
    fig.add_annotation(
        x=0.95,
        y=2.15,
        text=f"Experiential history<br>{count_map.get('Lived history', 0)} games<br>society / narrative / place",
        showarrow=False,
        font=dict(color=TEAL, size=13),
        bgcolor="rgba(255,250,235,0.74)",
        bordercolor=TEAL,
        borderwidth=1,
    )
    fig.add_annotation(
        x=0.9,
        y=0.25,
        text=f"Mixed / low signal<br>{count_map.get('Low-tag / mixed', 0)} games",
        showarrow=False,
        font=dict(color=MOSS, size=13),
        bgcolor="rgba(255,250,235,0.74)",
        bordercolor=MOSS,
        borderwidth=1,
    )


def style_grid_axes(fig: go.Figure) -> go.Figure:
    fig.update_xaxes(
        title="Command/control score",
        range=[-0.45, 5.45],
        dtick=1,
    )
    fig.update_yaxes(
        title="Lived/experiential score",
        range=[-0.35, 2.45],
        dtick=1,
    )
    fig.update_layout(title_text="", showlegend=False, legend_title_text="")
    return styled_plotly_layout(fig, height=620)


def make_grid_traces(grouped: pd.DataFrame, sizeref: float) -> list[go.Scatter]:
    traces = []
    categories = [
        "Command history",
        "Hybrid history",
        "Lived history",
        "Low-tag / mixed",
    ]

    for play_type in categories:
        if grouped.empty:
            cell_df = grouped
        else:
            cell_df = grouped[grouped["grid_category"] == play_type]
        if cell_df.empty:
            traces.append(
                go.Scatter(
                    x=[],
                    y=[],
                    mode="markers+text",
                    name=play_type,
                    marker=dict(color=TYPE_COLORS.get(play_type, MOSS)),
                    hovertemplate="%{hovertext}<extra></extra>",
                )
            )
            continue
        traces.append(
            go.Scatter(
                x=cell_df["command_control_score"],
                y=cell_df["lived_experience_score"],
                mode="markers+text",
                name=play_type,
                text=cell_df["label"],
                textposition="middle center",
                textfont=dict(color="#fffaf0", size=12),
                marker=dict(
                    size=cell_df["games"],
                    sizemode="area",
                    sizeref=sizeref * 0.55,
                    sizemin=24,
                    color=cell_df["color"],
                    line=dict(color="#fff8e5", width=2),
                    opacity=0.9,
                ),
                hovertext=cell_df["hover_text"],
                hovertemplate="%{hovertext}<extra></extra>",
            )
        )
    return traces


def plot_playable_history_grid(
    df: pd.DataFrame,
    region_filter: str = "All categories",
    time_view: str = "All years",
) -> go.Figure:
    working = df.copy()
    working["grid_category"] = working.apply(playable_region, axis=1)
    if region_filter != "All categories":
        region_filter = category_value_from_display(region_filter)
        working = working[working["grid_category"] == region_filter]

    grouped_all = build_grid_cells(working)
    max_games = max(grouped_all["games"].max(), 1) if not grouped_all.empty else 1
    sizeref = 2.0 * max_games / (58.0**2)

    fig = go.Figure()
    add_grid_backdrop(fig)
    add_grid_annotations(fig, working)

    if time_view == "Animate by release year" and "release_year" in working.columns:
        years = sorted(
            int(year)
            for year in working["release_year"].dropna().unique()
        )
        if years:
            first_year = years[0]
            first_grouped = build_grid_cells(working[working["release_year"] <= first_year])
            for trace in make_grid_traces(first_grouped, sizeref):
                fig.add_trace(trace)

            frames = []
            for year in years:
                year_df = working[working["release_year"] <= year]
                frame_grouped = build_grid_cells(year_df)
                frames.append(
                    go.Frame(
                        name=str(year),
                        data=make_grid_traces(frame_grouped, sizeref),
                    )
                )
            fig.frames = frames
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="left",
                        x=0,
                        y=1.12,
                        buttons=[
                            dict(
                                label="Play",
                                method="animate",
                                args=[
                                    None,
                                    {
                                        "frame": {"duration": 900, "redraw": True},
                                        "fromcurrent": True,
                                        "transition": {"duration": 350},
                                    },
                                ],
                            ),
                            dict(
                                label="Pause",
                                method="animate",
                                args=[
                                    [None],
                                    {
                                        "frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate",
                                    },
                                ],
                            ),
                        ],
                    )
                ],
                sliders=[
                    dict(
                        active=0,
                        y=-0.06,
                        currentvalue={"prefix": "Through "},
                        steps=[
                            dict(
                                label=str(year),
                                method="animate",
                                args=[
                                    [str(year)],
                                    {
                                        "frame": {"duration": 350, "redraw": True},
                                        "mode": "immediate",
                                        "transition": {"duration": 250},
                                    },
                                ],
                            )
                            for year in years
                        ],
                    )
                ],
            )
        else:
            for trace in make_grid_traces(grouped_all, sizeref):
                fig.add_trace(trace)
    else:
        for trace in make_grid_traces(grouped_all, sizeref):
            fig.add_trace(trace)

    fig.add_vline(x=2.5, line_color=INK_NAVY, line_width=1.5, line_dash="dash")
    fig.add_hline(y=1.5, line_color=INK_NAVY, line_width=1.5, line_dash="dash")
    return style_grid_axes(fig)


def build_mode_summary(df: pd.DataFrame, display_as: str) -> pd.DataFrame:
    rows = []
    for label, col in COMMAND_MODES:
        if col in df.columns:
            count = int(df[col].sum())
            rows.append(
                {
                    "mode": label,
                    "column": col,
                    "group": "Command/control",
                    "count": count,
                    "signed_count": count,
                    "color": BURGUNDY,
                    "group_order": 1,
                }
            )

    for label, col in LIVED_MODES:
        if col in df.columns:
            count = int(df[col].sum())
            rows.append(
                {
                    "mode": label,
                    "column": col,
                    "group": "Lived/experiential",
                    "count": count,
                    "signed_count": -count,
                    "color": TEAL,
                    "group_order": 0,
                }
            )

    summary = pd.DataFrame(rows)
    if summary.empty:
        return summary

    denominator = max(len(df), 1)
    summary["percent"] = summary["count"] / denominator * 100
    summary["signed_percent"] = summary["signed_count"] / denominator * 100

    if display_as == "Percentage of corpus":
        summary["value"] = summary["signed_percent"]
        summary["label"] = summary["percent"].map(lambda value: f"{value:.0f}%")
        summary["axis_title"] = "Share of filtered corpus"
    else:
        summary["value"] = summary["signed_count"]
        summary["label"] = summary["count"].astype(str)
        summary["axis_title"] = "Number of games"

    summary = summary.sort_values(["group_order", "count"], ascending=[True, True])

    return summary


def plot_balance_chart(summary: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    if summary.empty:
        return styled_plotly_layout(fig, height=440)

    y_order = summary["mode"].tolist()
    fig.add_trace(
        go.Bar(
            x=summary["value"],
            y=summary["mode"],
            orientation="h",
            marker=dict(color=summary["color"], line=dict(color="#fff8e5", width=1)),
            text=summary["label"],
            textposition="outside",
            customdata=summary[["group", "count", "percent"]],
            hovertemplate=(
                "Mode: %{y}<br>"
                "Interpretive group: %{customdata[0]}<br>"
                "Games: %{customdata[1]}<br>"
                "Share of corpus: %{customdata[2]:.1f}%<extra></extra>"
            ),
            showlegend=False,
        )
    )
    axis_title = str(summary["axis_title"].iloc[0])
    max_abs = max(abs(summary["value"]).max(), 1)
    fig.add_vline(x=0, line_color=INK_NAVY, line_width=2)
    fig.add_annotation(
        x=max_abs * 0.72,
        y=1.04,
        xref="x",
        yref="paper",
        text="Command/control",
        showarrow=False,
        font=dict(color=BURGUNDY, size=13),
    )
    fig.add_annotation(
        x=-max_abs * 0.72,
        y=1.04,
        xref="x",
        yref="paper",
        text="Lived/experiential",
        showarrow=False,
        font=dict(color=TEAL, size=13),
    )
    fig.update_xaxes(
        title=axis_title,
        range=[-max_abs * 1.35, max_abs * 1.35],
        tickformat=",.0f",
    )
    fig.update_yaxes(categoryorder="array", categoryarray=y_order)
    fig.update_layout(title_text="", margin=dict(l=20, r=36, t=56, b=30))
    return styled_plotly_layout(fig, height=470)


def plot_rating_reception(df: pd.DataFrame) -> go.Figure:
    rating_df = df.dropna(subset=["rating"]).copy()
    fig = go.Figure()
    if rating_df.empty:
        return styled_plotly_layout(fig, height=430)

    order = [
        category
        for category in ["Lived history", "Low-tag / mixed", "Hybrid history", "Command history"]
        if category in rating_df["historical_play_type"].unique()
    ]
    if not order:
        order = sorted(rating_df["historical_play_type"].unique())

    y_positions = {category: index for index, category in enumerate(order)}
    rating_df["y"] = rating_df["historical_play_type"].map(y_positions)
    rating_df["color"] = rating_df["historical_play_type"].map(TYPE_COLORS).fillna(MOSS)

    # Deterministic micro-jitter makes overlapping ratings visible without changing meaning.
    rating_df["jitter"] = (
        rating_df.groupby("historical_play_type").cumcount().mod(5) - 2
    ) * 0.035
    rating_df["plot_y"] = rating_df["y"] + rating_df["jitter"]

    fig.add_trace(
        go.Scatter(
            x=rating_df["rating"],
            y=rating_df["plot_y"],
            mode="markers",
            marker=dict(
                size=13,
                color=rating_df["color"],
                line=dict(color="#fff8e5", width=1.2),
                opacity=0.86,
            ),
            customdata=rating_df[
                [
                    "title",
                    "release_year",
                    "main_genre",
                    "historical_play_type",
                    "command_control_score",
                    "lived_experience_score",
                ]
            ],
            hovertemplate=(
                "%{customdata[0]} (%{customdata[1]})<br>"
                "Rating: %{x:.1f}<br>"
                "Play type: %{customdata[3]}<br>"
                "Genre: %{customdata[2]}<br>"
                "Command score: %{customdata[4]}<br>"
                "Lived score: %{customdata[5]}<extra></extra>"
            ),
            showlegend=False,
        )
    )

    medians = (
        rating_df.groupby("historical_play_type", as_index=False)["rating"]
        .median()
        .rename(columns={"rating": "median_rating"})
    )
    for _, row in medians.iterrows():
        category = row["historical_play_type"]
        y = y_positions.get(category)
        if y is None:
            continue
        median = row["median_rating"]
        color = TYPE_COLORS.get(category, MOSS)
        fig.add_shape(
            type="line",
            x0=median,
            x1=median,
            y0=y - 0.3,
            y1=y + 0.3,
            line=dict(color=color, width=4),
        )
        fig.add_annotation(
            x=median,
            y=y + 0.38,
            text=f"median {median:.1f}",
            showarrow=False,
            font=dict(color=color, size=12),
            bgcolor="rgba(255,250,235,0.72)",
        )

    fig.update_xaxes(title="Rating", range=[6.8, 8.95], dtick=0.5)
    fig.update_yaxes(
        title="Historical play type",
        tickmode="array",
        tickvals=list(y_positions.values()),
        ticktext=list(y_positions.keys()),
        range=[-0.65, len(order) - 0.35],
    )
    fig.update_layout(title_text="")
    return styled_plotly_layout(fig, height=max(380, len(order) * 95 + 160))


def plot_genre_orientation(
    df: pd.DataFrame,
    sort_by: str = "Orientation gap",
    min_games: int = 1,
    highlight_genre: str = "None",
) -> go.Figure:
    genre_rows = []
    for genre, genre_df in df.groupby("main_genre"):
        examples = genre_df["title"].dropna().sort_values().head(5).tolist()
        genre_rows.append(
            {
                "main_genre": genre,
                "avg_command": genre_df["command_control_score"].mean(),
                "avg_lived": genre_df["lived_experience_score"].mean(),
                "games": len(genre_df),
                "avg_rating": genre_df["rating"].mean(),
                "examples": "<br>".join(examples),
            }
        )

    summary = pd.DataFrame(genre_rows).dropna(subset=["avg_command", "avg_lived"])
    if summary.empty:
        return styled_plotly_layout(go.Figure(), height=500)

    summary["orientation_gap"] = summary["avg_command"] - summary["avg_lived"]
    summary = summary[summary["games"] >= min_games].copy()
    if summary.empty:
        return styled_plotly_layout(go.Figure(), height=500)

    if sort_by == "Most command-oriented":
        summary = summary.sort_values("orientation_gap", ascending=True)
    elif sort_by == "Most lived-oriented":
        summary = summary.sort_values("orientation_gap", ascending=False)
    elif sort_by == "Most games":
        summary = summary.sort_values("games", ascending=True)
    elif sort_by == "Average rating":
        summary = summary.sort_values("avg_rating", ascending=True)
    else:
        summary = summary.sort_values("orientation_gap", ascending=True)

    summary = summary.reset_index(drop=True)
    summary["y"] = list(range(len(summary)))
    summary["avg_rating_label"] = summary["avg_rating"].map(
        lambda value: "Not rated" if pd.isna(value) else f"{value:.2f}"
    )
    summary["is_highlight"] = (
        (highlight_genre != "None") & (summary["main_genre"] == highlight_genre)
    )

    line_x = []
    line_y = []
    for _, row in summary.iterrows():
        line_x.extend([row["avg_lived"], row["avg_command"], None])
        line_y.extend([row["y"], row["y"], None])

    size_max = max(summary["games"].max(), 1)
    marker_sizes = summary["games"].map(lambda count: 14 + (count / size_max) * 30)
    marker_opacity = summary["is_highlight"].map(
        lambda highlighted: 1.0 if highlighted or highlight_genre == "None" else 0.28
    )
    custom = summary[
        [
            "main_genre",
            "games",
            "avg_rating_label",
            "avg_command",
            "avg_lived",
            "examples",
        ]
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=line_x,
            y=line_y,
            mode="lines",
            line=dict(color="rgba(22,36,54,0.38)", width=3),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=summary["avg_lived"],
            y=summary["y"],
            mode="markers",
            name="Average lived/experiential score",
            marker=dict(
                color=TEAL,
                size=marker_sizes,
                line=dict(color="#fff8e5", width=1.5),
                opacity=marker_opacity,
            ),
            customdata=custom,
            hovertemplate=(
                "Genre: %{customdata[0]}<br>"
                "Games: %{customdata[1]}<br>"
                "Average rating: %{customdata[2]}<br>"
                "Average command score: %{customdata[3]:.2f}<br>"
                "Average lived score: %{customdata[4]:.2f}<br><br>"
                "Examples:<br>%{customdata[5]}<extra></extra>"
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=summary["avg_command"],
            y=summary["y"],
            mode="markers",
            name="Average command/control score",
            marker=dict(
                color=BURGUNDY,
                size=marker_sizes,
                line=dict(color="#fff8e5", width=1.5),
                opacity=marker_opacity,
            ),
            customdata=custom,
            hovertemplate=(
                "Genre: %{customdata[0]}<br>"
                "Games: %{customdata[1]}<br>"
                "Average rating: %{customdata[2]}<br>"
                "Average command score: %{customdata[3]:.2f}<br>"
                "Average lived score: %{customdata[4]:.2f}<br><br>"
                "Examples:<br>%{customdata[5]}<extra></extra>"
            ),
        )
    )
    max_score = max(summary["avg_command"].max(), summary["avg_lived"].max(), 2)
    fig.update_xaxes(title="Average score by genre", range=[-0.15, max_score + 0.55])
    fig.update_yaxes(
        title="Main genre",
        tickmode="array",
        tickvals=summary["y"],
        ticktext=summary["main_genre"],
    )
    fig.update_layout(title_text="")
    if highlight_genre != "None" and highlight_genre in summary["main_genre"].values:
        row = summary[summary["main_genre"] == highlight_genre].iloc[0]
        fig.add_annotation(
            x=max(row["avg_command"], row["avg_lived"]) + 0.15,
            y=row["y"],
            text="selected",
            showarrow=False,
            font=dict(color=INK_NAVY, size=12),
            bgcolor="rgba(255,250,235,0.78)",
            bordercolor=INK_NAVY,
            borderwidth=1,
        )
    return styled_plotly_layout(fig, height=max(520, 58 * len(summary) + 140))


apply_theme()

try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "The data file was not found. Expected: data/cleaned_games_playable_history.csv"
    )
    st.stop()


filtered = df.copy()

st.markdown(
    '<div class="hero-kicker">Zhihao Liu data visualization project</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="hero-title">Playable History</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="thesis-box">
    This project does not ask whether historical games are historically accurate. It asks what kind of historical agency they make playable.
    In this curated corpus, games are mapped between two poles: command/control history &mdash; warfare, strategy, empire,
    management, politics &mdash; and lived/experiential history &mdash; society, narrative, place, and embodied exploration.
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="dataset-box">
    <b>Dataset and scoring:</b> I built this dataset from historical video game entries on MobyGames.com.
    The themes come from MobyGames metadata, including terms such as warfare, strategy, empire, society, narrative, and open-world exploration.
    During data cleaning, I grouped those themes into two scores: command/control and lived/experiential. The graphs use those scores to show
    whether a game makes history playable as something players command, manage, conquer, or govern, or as something players inhabit, witness,
    survive, and experience through place and narrative.
    </div>
    """,
    unsafe_allow_html=True,
)

page_heading("Two Ways History Becomes Playable")
card_left, card_right = st.columns(2)

with card_left:
    st.markdown(
        """
        <div class="concept-card command">
        <div class="card-title">Command History</div>
        <p>History as something the player commands, manages, conquers, optimizes, or governs.</p>
        <div class="keywords">Keywords: warfare, strategy, empire, management, politics.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with card_right:
    st.markdown(
        """
        <div class="concept-card lived">
        <div class="card-title">Lived History</div>
        <p>History as something the player inhabits, witnesses, survives, or experiences through place and narrative.</p>
        <div class="keywords">Keywords: society, culture, narrative, open world, embodied experience.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="contrast-band">
        <div class="contrast-pole command">Command, management, conquest, optimization, governance</div>
        <div class="contrast-arrow">&harr;</div>
        <div class="contrast-pole lived">Inhabiting, witnessing, surviving, place, narrative</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if filtered.empty:
    st.warning("No games are available in the dataset.")
    st.stop()

page_heading("Visualization 1: Playable History Grid")
grid_control_left, grid_control_right = st.columns([1, 1])
with grid_control_left:
    grid_region = st.selectbox(
        "Show category",
        [
            "All categories",
            "Command history",
            "Hybrid history",
            "Experiential history",
            "Low-tag / mixed",
        ],
    )
with grid_control_right:
    grid_time_view = st.radio(
        "Time view",
        ["All years", "Animate by release year"],
        horizontal=True,
    )

footprint_df = filtered.copy()
footprint_df["grid_category"] = footprint_df.apply(playable_region, axis=1)
if grid_region != "All categories":
    footprint_df = footprint_df[
        footprint_df["grid_category"] == category_value_from_display(grid_region)
    ]

render_category_footprint(footprint_df)
st.plotly_chart(
    plot_playable_history_grid(filtered, grid_region, grid_time_view),
    width="stretch",
    config={"displayModeBar": False},
)

page_heading("Visualization 2: Historical Game Themes: Experiential vs Command")

display_as = st.radio(
    "Measure",
    ["Percentage of corpus", "Number of games"],
    horizontal=True,
)

mode_summary = build_mode_summary(filtered, display_as)
st.plotly_chart(
    plot_balance_chart(mode_summary),
    width="stretch",
    config={"displayModeBar": False},
)

page_heading("Visualization 3: Genre Orientation Plot")
genre_control_left, genre_control_mid, genre_control_right = st.columns([1, 1, 1])
genre_counts = filtered["main_genre"].value_counts()
max_genre_count = int(genre_counts.max()) if not genre_counts.empty else 1
with genre_control_left:
    genre_sort = st.selectbox(
        "Sort genres",
        [
            "Orientation gap",
            "Most command-oriented",
            "Most lived-oriented",
            "Most games",
            "Average rating",
        ],
    )
with genre_control_mid:
    min_genre_games = st.slider(
        "Minimum games in genre",
        min_value=1,
        max_value=max(max_genre_count, 1),
        value=1,
        step=1,
    )
eligible_genres = sorted(
    genre_counts[genre_counts >= min_genre_games].index.tolist()
)
with genre_control_right:
    highlighted_genre = st.selectbox("Highlight genre", ["None"] + eligible_genres)

st.plotly_chart(
    plot_genre_orientation(filtered, genre_sort, min_genre_games, highlighted_genre),
    width="stretch",
    config={"displayModeBar": False},
)

if highlighted_genre != "None":
    highlight_table = (
        filtered[filtered["main_genre"] == highlighted_genre][
            [
                "title",
                "release_year",
                "historical_play_type",
                "command_control_score",
                "lived_experience_score",
                "rating",
            ]
        ]
        .sort_values(["release_year", "title"], ascending=[False, True])
        .reset_index(drop=True)
    )
    st.dataframe(highlight_table, width="stretch", hide_index=True)

page_heading("Ratings as Reception Clue")
st.markdown(
    '<div class="small-note">Ratings are included as reception evidence: useful for context, but not proof that one kind of playable history is better or causes higher scores.</div>',
    unsafe_allow_html=True,
)
st.plotly_chart(
    plot_rating_reception(filtered),
    width="stretch",
    config={"displayModeBar": False},
)
