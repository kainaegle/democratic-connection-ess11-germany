# app/app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import base64
import textwrap


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="The Democratic Trust Gap",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =============================================================================
# PATHS
# =============================================================================

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
DATA_CLEAN = PROJECT_ROOT / "data" / "clean"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_APP = PROJECT_ROOT / "data" / "app"
ASSETS_DIR = APP_DIR / "assets"
HERO_IMAGE = ASSETS_DIR / "democratic_connection_hero.png"


# =============================================================================
# STYLE
# =============================================================================

st.markdown(
    """
    <style>
    :root {
        --bg-main: #0E1117;
        --bg-card: #161B22;
        --bg-card-2: #1F2630;
        --text-main: #F2F2F2;
        --text-muted: #B8C0CC;
        --accent-green: #009E73;
        --accent-purple: #CC79A7;
        --accent-yellow: #F0E442;
        --accent-blue: #56B4E9;
        --border-soft: rgba(255,255,255,0.08);
    }

    .main {
        background-color: var(--bg-main);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    h1, h2, h3 {
        letter-spacing: -0.03em;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.1rem 2.3rem;
        border-radius: 24px;
        background:
            radial-gradient(circle at top left, rgba(86,180,233,0.25), transparent 35%),
            radial-gradient(circle at bottom right, rgba(204,121,167,0.18), transparent 35%),
            linear-gradient(135deg, #111827 0%, #161B22 55%, #0E1117 100%);
        border: none;
        outline: 1px solid rgba(255,255,255,0.04);
        outline-offset: -1px;
        margin-bottom: 1.4rem;
    }

    .hero-title {
        font-size: 2.75rem;
        font-weight: 800;
        color: var(--text-main);
        margin-bottom: 0.45rem;
        line-height: 1.05;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        color: var(--text-muted);
        max-width: 980px;
        line-height: 1.55;
    }

    .hero-tag {
        display: inline-block;
        padding: 0.35rem 0.72rem;
        border-radius: 999px;
        color: #0E1117;
        background: #F0E442;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        letter-spacing: 0.02em;
    }

    .kpi-card {
        padding: 1.2rem 1.25rem;
        border-radius: 18px;
        background: linear-gradient(180deg, #1F2630 0%, #161B22 100%);
        border: 1px solid var(--border-soft);
        min-height: 140px;
    }

    .kpi-label {
        color: var(--text-muted);
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }

    .kpi-value {
        color: var(--text-main);
        font-size: 1.95rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
        line-height: 1.1;
    }

    .kpi-note {
        color: var(--text-muted);
        font-size: 0.86rem;
        line-height: 1.35;
    }

    .insight-box {
        padding: 1.15rem 1.25rem;
        border-radius: 18px;
        background: #161B22;
        border-left: 5px solid #56B4E9;
        border-top: 1px solid var(--border-soft);
        border-right: 1px solid var(--border-soft);
        border-bottom: 1px solid var(--border-soft);
        margin: 0.7rem 0 1rem 0;
        color: var(--text-main);
    }

    .method-box {
        padding: 1rem 1.15rem;
        border-radius: 16px;
        background: rgba(86,180,233,0.08);
        border: 1px solid rgba(86,180,233,0.18);
        color: var(--text-muted);
        font-size: 0.93rem;
        line-height: 1.45;
        margin-top: 0.75rem;
        margin-bottom: 1.2rem;
    }

    .profile-card {
        padding: 1.2rem 1.25rem;
        border-radius: 18px;
        background: #161B22;
        border: 1px solid var(--border-soft);
        min-height: 230px;
    }

    .profile-title {
        font-size: 1.1rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .profile-meta {
        color: var(--text-muted);
        font-size: 0.9rem;
        margin-bottom: 0.9rem;
    }

    .small-muted {
        color: var(--text-muted);
        font-size: 0.88rem;
        line-height: 1.45;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.65rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.4rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 14px 14px 0 0;
        padding-left: 18px;
        padding-right: 18px;
        background-color: #161B22;
        border: 1px solid rgba(255,255,255,0.06);
    }

    .stTabs [aria-selected="true"] {
        background-color: #1F2630;
        border-bottom: 2px solid #56B4E9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================================================================
# CONSTANTS
# =============================================================================

OKABE_ITO = {
    "blue": "#56B4E9",
    "green": "#009E73",
    "yellow": "#F0E442",
    "purple": "#CC79A7",
    "orange": "#E69F00",
    "vermillion": "#D55E00",
}

PROFILE_COLORS = {
    "Connected Democratic Core": OKABE_ITO["green"],
    "Disappointed Democratic Participants": OKABE_ITO["purple"],
    "Disengaged Non-voters": OKABE_ITO["yellow"],
}

OUTCOME_COLORS = {
    "Democracy satisfaction": OKABE_ITO["blue"],
    "Trust in political parties": OKABE_ITO["purple"],
    "Trust in parliament": OKABE_ITO["green"],
    "Trust in politicians": OKABE_ITO["yellow"],
}

GROUP_COLORS = {
    "Voted": OKABE_ITO["green"],
    "Did not vote": OKABE_ITO["yellow"],
    "Low efficacy": OKABE_ITO["purple"],
    "Medium efficacy": OKABE_ITO["blue"],
    "High efficacy": OKABE_ITO["green"],
    "Low social trust": OKABE_ITO["purple"],
    "Medium social trust": OKABE_ITO["blue"],
    "High social trust": OKABE_ITO["green"],
    "Secure or coping": OKABE_ITO["green"],
    "Economically strained": OKABE_ITO["purple"],
    "Left (0–3)": OKABE_ITO["blue"],
    "Center (4–6)": OKABE_ITO["green"],
    "Right (7–10)": OKABE_ITO["purple"],
}

COLOR_MAP = {
    **PROFILE_COLORS,
    **OUTCOME_COLORS,
    **GROUP_COLORS,
    "Political efficacy": OKABE_ITO["blue"],
    "Social trust": OKABE_ITO["green"],
    "Income feeling": OKABE_ITO["yellow"],
    "Income difficulty": OKABE_ITO["yellow"],
    "Left-right placement": OKABE_ITO["purple"],
    "Voted share": OKABE_ITO["blue"],
    "Voting participation": OKABE_ITO["yellow"],
}

PROFILE_ORDER = [
    "Connected Democratic Core",
    "Disappointed Democratic Participants",
    "Disengaged Non-voters",
]

PLOT_TEMPLATE = "plotly_dark"
ALIGNMENT_COLOR_SCALE = [
    [0.0, "#CC79A7"],
    [0.5, "#1F2630"],
    [1.0, "#F0E442"]
]


# =============================================================================
# DATA LOADING
# =============================================================================

@st.cache_data
def load_csv(path: Path, required: bool = True) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    if required:
        st.error(f"Required file not found: `{path}`")
        st.stop()
    return pd.DataFrame()


profile_summary = load_csv(DATA_PROCESSED / "democratic_connection_profile_summary_final.csv")
profile_z = load_csv(DATA_PROCESSED / "democratic_connection_profile_z_summary.csv", required=False)
strategy_table = load_csv(DATA_PROCESSED / "democratic_connection_profile_strategy_table.csv")
regression_results = load_csv(DATA_PROCESSED / "regression_results_democracy_satisfaction_party_trust.csv")
regression_model_comparison = load_csv(DATA_PROCESSED / "regression_model_comparison.csv")
diagnostic_summary = load_csv(DATA_PROCESSED / "regression_diagnostic_summary.csv", required=False)
vif_results = load_csv(DATA_PROCESSED / "regression_vif_results.csv", required=False)
hypothesis_summary = load_csv(DATA_APP / "app_hypothesis_testing_summary.csv", required=False)

participation_gap = load_csv(DATA_PROCESSED / "participation_gap_validation.csv")
efficacy_gap = load_csv(DATA_PROCESSED / "political_efficacy_gap_validation.csv")
social_gap = load_csv(DATA_PROCESSED / "social_trust_gap_validation.csv")
economic_gap = load_csv(DATA_PROCESSED / "economic_security_gap_binary_validation.csv")
orientation_gap = load_csv(DATA_PROCESSED / "political_orientation_pattern_validation.csv")
priority_table = load_csv(DATA_PROCESSED / "analytical_priority_table.csv")
gap_strength = load_csv(DATA_PROCESSED / "trust_gap_strength_ranking.csv")

profiles_data = load_csv(DATA_CLEAN / "ess11_germany_democratic_connection_profiles.csv")
extended_data = load_csv(DATA_CLEAN / "ess11_germany_extended_clean.csv", required=False)

pca_data = load_csv(DATA_PROCESSED / "democratic_connection_profiles_pca_coordinates.csv", required=False)
pca_variance = load_csv(DATA_PROCESSED / "democratic_connection_profiles_pca_explained_variance.csv", required=False)
pca_loadings = load_csv(DATA_PROCESSED / "democratic_connection_profiles_pca_loadings.csv", required=False)
party_alignment_long = load_csv(DATA_APP / "app_party_alignment_long.csv", required=False)
party_alignment_matrix = load_csv(DATA_APP / "app_party_alignment_matrix.csv", required=False)
party_alignment_summary = load_csv(DATA_APP / "app_party_alignment_party_summary.csv", required=False)
party_dimension_evidence = load_csv(DATA_APP / "app_party_dimension_evidence_strength.csv", required=False)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def image_to_base64(path: Path) -> str:
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def plot_layout(fig, title=None, height=520, x_title=None, y_title=None):
    fig.update_layout(
        template=PLOT_TEMPLATE,
        title=dict(
            text=title,
            x=0.02,
            xanchor="left",
            font=dict(size=21)
        ) if title else None,
        height=height,
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="#F2F2F2"),
        margin=dict(l=30, r=30, t=75 if title else 40, b=50),
        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    if x_title:
        fig.update_xaxes(title_text=x_title, gridcolor="rgba(255,255,255,0.08)")
    else:
        fig.update_xaxes(gridcolor="rgba(255,255,255,0.08)")
    if y_title:
        fig.update_yaxes(title_text=y_title, gridcolor="rgba(255,255,255,0.08)")
    else:
        fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")
    return fig


def kpi_card(label, value, note):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def insight_box(text):
    st.markdown(f"""<div class="insight-box">{text}</div>""", unsafe_allow_html=True)


def method_box(text, title="Method / reading note", expanded=False):
    clean_text = textwrap.dedent(text).strip()

    with st.expander(title, expanded=expanded):
        st.markdown(
            f"""
            <div class="method-box">
                {clean_text}
            </div>
            """,
            unsafe_allow_html=True
        )


def format_profile_name(name):
    return str(name).replace("_", " ")


def clean_profile_summary(df):
    df = df.copy()
    if "democratic_connection_profile" not in df.columns and "connection_profile" in df.columns:
        df = df.rename(columns={"connection_profile": "democratic_connection_profile"})
    return df


profile_summary = clean_profile_summary(profile_summary)

if not profile_z.empty:
    if "democratic_connection_profile" not in profile_z.columns:
        first_col = profile_z.columns[0]
        profile_z = profile_z.rename(columns={first_col: "democratic_connection_profile"})


# =============================================================================
# HEADER
# =============================================================================

hero_bg = image_to_base64(HERO_IMAGE) if HERO_IMAGE.exists() else ""


if hero_bg:
    st.markdown(
        f"""
        <style>
        .hero {{
            position: relative;
            overflow: hidden;
            background:
                linear-gradient(
                    90deg,
                    rgba(14,17,23,1.00) 0%,
                    rgba(14,17,23,0.99) 18%,
                    rgba(14,17,23,0.93) 38%,
                    rgba(14,17,23,0.62) 68%,
                    rgba(14,17,23,0.34) 100%
                ),
                url("data:image/png;base64,{hero_bg}"),
                linear-gradient(135deg, #111827 0%, #161B22 55%, #0E1117 100%);
            background-size: cover;
            background-position: center center;
            box-shadow:
                inset 0 0 0 1px rgba(255,255,255,0.06),
                inset 24px 0 36px rgba(14,17,23,0.98),
                0 18px 45px rgba(0,0,0,0.25);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">ESS Round 11 · Germany · Democratic Trust Analysis</div>
        <div class="hero-title">The Democratic Trust Gap</div>
        <div class="hero-subtitle">
            A data-driven analysis of trust, voice and participation in Germany.
            Behind this project is a simple question: Who feels represented, who feels heard,
            and who starts to disengage?
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    kpi_card("Germany ESS11 sample", "2,420", "Respondents in the Germany subset before analytical filtering.")

with kpi_col2:
    reg_n = int(regression_model_comparison["n_observations"].max()) if "n_observations" in regression_model_comparison.columns else 2064
    kpi_card("Regression sample", f"{reg_n:,}", "Model-ready cases for democratic satisfaction and party trust models.")

with kpi_col3:
    kpi_card("Strongest signal", "Political efficacy", "Most consistent predictor in correlations, group tests and regressions.")

with kpi_col4:
    disappointed_share = profile_summary.loc[
        profile_summary["democratic_connection_profile"].str.contains("Disappointed", case=False, na=False),
        "percentage"
    ]
    disappointed_value = f"{float(disappointed_share.iloc[0]):.1f}%" if len(disappointed_share) else "≈39%"
    kpi_card("Strategic risk group", disappointed_value, "Voters with low democratic satisfaction and low party trust.")


st.markdown("---")


# =============================================================================
# TABS
# =============================================================================

tabs = st.tabs([
    "Overview",
    "Hypotheses",
    "Trust Gaps",
    "Regression",
    "Profiles",
    "PCA Explorer",
    "Strategy",
    "Party Transfer",
    "Method Notes"
])


# =============================================================================
# TAB 1: OVERVIEW
# =============================================================================

with tabs[0]:
    st.subheader("Overview: Trust, voice and participation")

    insight_box(
        """
        <b>Core idea:</b> The project asks who feels represented, who feels heard,
        and who starts to disengage. It translates abstract democratic trust into measurable
        survey dimensions: trust, voice, participation, social confidence and economic security.
        """
    )

    method_box(
        """
        Data source: European Social Survey Round 11, Germany subset. All results are interpreted as
        associations, not causal effects. Survey scales usually range from 0 to 10, where higher values
        indicate higher satisfaction or trust unless stated otherwise.
        """
    )

    st.markdown("### Core analytical dimensions")

    core_dimensions = pd.DataFrame(
        [
            {
                "Analytical dimension": "Trust",
                "Plain-language meaning": "Do people trust democratic institutions and political parties?",
                "ESS-based measure": "Democratic satisfaction, party trust and institutional trust indicators"
            },
            {
                "Analytical dimension": "Voice",
                "Plain-language meaning": "Do people feel that they can influence politics and be heard?",
                "ESS-based measure": "Political efficacy index"
            },
            {
                "Analytical dimension": "Participation",
                "Plain-language meaning": "Do people still take part in democracy through voting?",
                "ESS-based measure": "Cleaned voting participation variable"
            },
            {
                "Analytical dimension": "Social confidence",
                "Plain-language meaning": "Do people generally trust others and expect fair behaviour?",
                "ESS-based measure": "Social trust index"
            },
            {
                "Analytical dimension": "Economic security",
                "Plain-language meaning": "Do people feel economically secure or under strain?",
                "ESS-based measure": "Subjective income feeling"
            },
            {
                "Analytical dimension": "Political transfer layer",
                "Plain-language meaning": "How do selected party positions relate to the identified democratic connection priorities?",
                "ESS-based measure": "Exploratory Wahl-O-Mat 2025 mapping, not part of the core ESS model"
            },
        ]
    )

    st.dataframe(
        core_dimensions,
        use_container_width=True,
        hide_index=True
    )

    method_box(
        """
        The German ESS Round 11 data is based on a probability sample and face-to-face computer-assisted interviews.
        However, the official response rate for Germany is 26.7%.

        This matters for interpretation: if people with very low political trust, low institutional confidence or high
        disengagement are less likely to participate in the survey, democratic disconnection may be under- or differently
        represented in the data.

        Therefore, the results should be read as robust associational patterns within the achieved sample, not as a perfect
        census of democratic attitudes in Germany.
        """,
        title="Data quality note: response rate and interpretation"
    )

    method_box(
        """
        Reading guide: The project translates abstract democratic trust into more tangible dimensions:
        whether people trust institutions, feel politically heard, still participate, trust others and feel economically secure.
        """,
        title="Reading guide: how to read the dimensions"
    )

    st.markdown("### Starting observation: institutional trust differs strongly")
    
    trust_values = {
        "Trust in political parties": profiles_data["trstprt"].mean() if "trstprt" in profiles_data.columns else np.nan,
        "Democracy satisfaction": profiles_data["stfdem"].mean() if "stfdem" in profiles_data.columns else np.nan,
    }

    if not extended_data.empty:
        extended_trust_map = {
            "Trust in political parties": "trstprt",
            "Trust in politicians": "trstplt",
            "Trust in parliament": "trstprl",
            "Trust in legal system": "trstlgl",
            "Trust in police": "trstplc",
            "Trust in European Parliament": "trstep",
            "Trust in United Nations": "trstun",
            "Democracy satisfaction": "stfdem",
        }

        trust_rank_df = pd.DataFrame([
            {
                "indicator": label,
                "mean_score": extended_data[var].mean()
            }
            for label, var in extended_trust_map.items()
            if var in extended_data.columns
        ]).dropna()

        trust_rank_df = trust_rank_df.sort_values("mean_score", ascending=True)

        fig = px.bar(
            trust_rank_df,
            x="mean_score",
            y="indicator",
            orientation="h",
            text=trust_rank_df["mean_score"].round(2),
            color="indicator",
            color_discrete_map=COLOR_MAP,
            title="Institutional Trust Ranking in Germany",
            labels={
                "mean_score": "Mean score on 0–10 scale",
                "indicator": "Democratic satisfaction and institutional trust indicator"
            }
        )

        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(showlegend=False)
        fig.update_xaxes(range=[0, 10])
        fig = plot_layout(
            fig,
            title="Institutional Trust Ranking in Germany",
            height=560,
            x_title="Mean score on 0–10 scale",
            y_title="Indicator"
        )

        st.plotly_chart(fig, use_container_width=True)

        method_box(
            """
            Reading guide: Higher values indicate higher trust or satisfaction. The chart shows that trust in
            political parties and politicians is lower than trust in several other institutions, supporting the
            project's focus on party trust as a specific democratic connection issue.
            """
        )

    insight_box(
        """
        <b>Key takeaway for the presentation:</b> The project is not only about whether people vote.
        It asks whether people experience democracy as trustworthy, responsive and meaningful.
        """
    )

    st.markdown("### Analytical pipeline")

    pipeline_col1, pipeline_col2, pipeline_col3, pipeline_col4 = st.columns(4)

    with pipeline_col1:
        st.markdown(
            """
            **1. Evidence base**
            - ESS11 Germany subset
            - variable selection
            - index construction
            """
        )

    with pipeline_col2:
        st.markdown(
            """
            **2. Statistical validation**
            - hypothesis testing
            - effect sizes
            - regression models
            """
        )

    with pipeline_col3:
        st.markdown(
            """
            **3. Profile translation**
            - connection profiles
            - PCA visualization
            - strategic implications
            """
        )

    with pipeline_col4:
        st.markdown(
            """
            **4. Political transfer layer**
            - Wahl-O-Mat 2025 positions
            - party-position mapping
            - cautious alignment view
            """
        )


# =============================================================================
# TAB 2: HYPOTHESIS TESTING
# =============================================================================

with tabs[1]:
    st.subheader("Hypothesis Testing")

    insight_box(
        """
        <b>Key takeaway:</b> The project does not only visualize survey data.
        It tests predefined hypotheses using group comparisons, effect sizes and regression evidence.
        The results are interpreted as associations, not causal proof.
        """
    )

    method_box(
        """
        The project uses hypothesis-driven group comparisons, effect sizes and regression models.
        Hypotheses are therefore not “proven” in a causal sense, but statistically and substantively
        supported to different degrees.
        """
    )

    if hypothesis_summary.empty:
        st.warning(
            "Hypothesis testing summary was not found. Please create and export "
            "`data/processed/app_hypothesis_testing_summary.csv` from the notebook first."
        )
    else:
        h_col1, h_col2, h_col3 = st.columns(3)

        with h_col1:
            kpi_card(
                "Hypotheses tested",
                str(len(hypothesis_summary)),
                "Predefined analytical hypotheses tested with group comparisons and regression evidence."
            )

        with h_col2:
            kpi_card(
                "Strongest support",
                "Political efficacy",
                "Most consistent signal across group tests, correlations and regression models."
            )

        with h_col3:
            kpi_card(
                "Evidence type",
                "Associational",
                "Cross-sectional survey evidence, not causal identification."
            )

        st.markdown("### Hypothesis results")

        evidence_icon_map = {
            "Strongly supported": "🟢",
            "Supported": "🟢",
            "Supported, weaker": "🟡",
            "Partly supported": "🟠",
            "Not supported": "🔴"
        }

        for _, row in hypothesis_summary.iterrows():
            icon = evidence_icon_map.get(row.get("evidence_strength", ""), "⚪")

            title = (
                f"{icon} {row.get('hypothesis_id', '')} · "
                f"{row.get('hypothesis', '')} · "
                f"{row.get('evidence_strength', '')}"
            )

            with st.expander(title, expanded=row.get("hypothesis_id", "") == "H2"):
                st.markdown(f"**Expected pattern:** {row.get('expected_pattern', '')}")
                st.markdown(f"**Test used:** {row.get('test_used', '')}")
                st.markdown(f"**Main result:** {row.get('main_result', '')}")
                st.markdown(f"**Effect size summary:** {row.get('effect_size_summary', '')}")
                st.markdown(f"**Interpretation:** {row.get('interpretation', '')}")

    st.markdown("### Compact hypothesis summary")

    compact_cols = [
        col for col in [
            "hypothesis_id",
            "hypothesis",
            "evidence_strength",
            "test_used",
            "effect_size_summary"
        ]
        if col in hypothesis_summary.columns
    ]

    compact_hypothesis_table = hypothesis_summary[compact_cols].copy()

    st.dataframe(
        compact_hypothesis_table,
        use_container_width=True,
        hide_index=True
    )

    with st.expander("Show full hypothesis summary with detailed interpretation"):
        st.dataframe(
            hypothesis_summary,
            use_container_width=True,
            hide_index=True
        )

    st.info(
        "Main conclusion: The hypotheses are supported to different degrees. "
        "Political efficacy receives the strongest support, followed by social trust and participation. "
        "Economic security and political orientation are relevant, but weaker in this model setup."
    )

# =============================================================================
# TAB 3: TRUST GAPS
# =============================================================================

with tabs[2]:
    st.subheader("Validated Trust Gaps")

    insight_box(
        """
        <b>Key takeaway:</b> The strongest gap appears around political efficacy —
        the feeling that one's voice can make a difference. People with higher political efficacy
        show higher democratic satisfaction and higher trust.
        """
    )

    gap_choice = st.selectbox(
        "Select a trust gap",
        [
            "Participation Gap",
            "Political Efficacy Gap",
            "Social Trust Gap",
            "Economic Security Gap",
            "Political Orientation Pattern"
        ],
        index=1
    )

    gap_data_map = {
        "Participation Gap": participation_gap,
        "Political Efficacy Gap": efficacy_gap,
        "Social Trust Gap": social_gap,
        "Economic Security Gap": economic_gap,
        "Political Orientation Pattern": orientation_gap,
    }

    selected_gap_df = gap_data_map[gap_choice]

    st.markdown(f"### {gap_choice}")

    if gap_choice == "Participation Gap":
        plot_df = selected_gap_df[[
            "outcome", "mean_voted", "mean_did_not_vote", "cohens_d", "effect_size_interpretation"
        ]].copy()

        plot_long = plot_df.melt(
            id_vars=["outcome", "cohens_d", "effect_size_interpretation"],
            value_vars=["mean_voted", "mean_did_not_vote"],
            var_name="group",
            value_name="mean_score"
        )

        plot_long["group"] = plot_long["group"].map({
            "mean_voted": "Voted",
            "mean_did_not_vote": "Did not vote"
        })

        fig = px.bar(
            plot_long,
            x="outcome",
            y="mean_score",
            color="group",
            barmode="group",
            text=plot_long["mean_score"].round(2),
            color_discrete_map=COLOR_MAP,
            labels={
                "outcome": "Outcome variable",
                "mean_score": "Mean score on 0–10 scale",
                "group": "Voting behavior"
            }
        )

        fig.update_traces(textposition="outside")
        fig.update_yaxes(range=[0, 10])
        fig = plot_layout(
            fig,
            title="Participation Gap: Voters show higher democratic trust",
            height=560,
            x_title="Outcome variable",
            y_title="Mean score on 0–10 scale"
        )

        st.plotly_chart(fig, use_container_width=True)

        best = selected_gap_df.loc[selected_gap_df["cohens_d"].abs().idxmax()]
        method_box(
            f"""
            Test: Welch's t-test. Effect size: Cohen's d.
            Strongest outcome: <b>{best['outcome']}</b>.
            Cohen's d = <b>{best['cohens_d']:.2f}</b>,
            interpreted as <b>{best['effect_size_interpretation']}</b>.
            """
        )

    elif gap_choice == "Economic Security Gap":
        plot_df = selected_gap_df[[
            "outcome", "mean_secure_or_coping", "mean_economically_strained",
            "cohens_d", "effect_size_interpretation"
        ]].copy()

        plot_long = plot_df.melt(
            id_vars=["outcome", "cohens_d", "effect_size_interpretation"],
            value_vars=["mean_secure_or_coping", "mean_economically_strained"],
            var_name="group",
            value_name="mean_score"
        )

        plot_long["group"] = plot_long["group"].map({
            "mean_secure_or_coping": "Secure or coping",
            "mean_economically_strained": "Economically strained"
        })

        fig = px.bar(
            plot_long,
            x="outcome",
            y="mean_score",
            color="group",
            barmode="group",
            text=plot_long["mean_score"].round(2),
            color_discrete_map=COLOR_MAP,
            labels={
                "outcome": "Outcome variable",
                "mean_score": "Mean score on 0–10 scale",
                "group": "Economic security group"
            }
        )

        fig.update_traces(textposition="outside")
        fig.update_yaxes(range=[0, 10])
        fig = plot_layout(
            fig,
            title="Economic Security Gap: Economic strain is associated with lower trust",
            height=560,
            x_title="Outcome variable",
            y_title="Mean score on 0–10 scale"
        )

        st.plotly_chart(fig, use_container_width=True)

        best = selected_gap_df.loc[selected_gap_df["cohens_d"].abs().idxmax()]
        method_box(
            f"""
            Test: Welch's t-test. Effect size: Cohen's d.
            Strongest outcome: <b>{best['outcome']}</b>.
            Cohen's d = <b>{best['cohens_d']:.2f}</b>,
            interpreted as <b>{best['effect_size_interpretation']}</b>.
            """
        )

    else:
        if gap_choice == "Political Efficacy Gap":
            value_cols = [
                "mean_low_efficacy",
                "mean_medium_efficacy",
                "mean_high_efficacy"
            ]
            group_map = {
                "mean_low_efficacy": "Low efficacy",
                "mean_medium_efficacy": "Medium efficacy",
                "mean_high_efficacy": "High efficacy"
            }
            title = "Political Efficacy Gap: Trust rises with perceived political influence"

        elif gap_choice == "Social Trust Gap":
            value_cols = [
                "mean_low_social_trust",
                "mean_medium_social_trust",
                "mean_high_social_trust"
            ]
            group_map = {
                "mean_low_social_trust": "Low social trust",
                "mean_medium_social_trust": "Medium social trust",
                "mean_high_social_trust": "High social trust"
            }
            title = "Social Trust Gap: Democratic trust is linked to social confidence"

        else:
            value_cols = [
                "mean_left",
                "mean_center",
                "mean_right"
            ]
            group_map = {
                "mean_left": "Left (0–3)",
                "mean_center": "Center (4–6)",
                "mean_right": "Right (7–10)"
            }
            title = "Political Orientation Pattern: Trust differs across self-placement groups"

        plot_df = selected_gap_df[["outcome", "epsilon_squared", "effect_size_interpretation"] + value_cols].copy()

        plot_long = plot_df.melt(
            id_vars=["outcome", "epsilon_squared", "effect_size_interpretation"],
            value_vars=value_cols,
            var_name="group",
            value_name="mean_score"
        )

        plot_long["group"] = plot_long["group"].map(group_map)

        fig = px.bar(
            plot_long,
            x="outcome",
            y="mean_score",
            color="group",
            barmode="group",
            text=plot_long["mean_score"].round(2),
            color_discrete_map=COLOR_MAP,
            labels={
                "outcome": "Outcome variable",
                "mean_score": "Mean score on 0–10 scale",
                "group": "Group"
            }
        )

        fig.update_traces(textposition="outside")
        fig.update_yaxes(range=[0, 10])
        fig = plot_layout(
            fig,
            title=title,
            height=590,
            x_title="Outcome variable",
            y_title="Mean score on 0–10 scale"
        )

        st.plotly_chart(fig, use_container_width=True)

        best = selected_gap_df.loc[selected_gap_df["epsilon_squared"].idxmax()]
        method_box(
            f"""
            Test: Kruskal-Wallis test. Effect size: epsilon-squared.
            Strongest outcome: <b>{best['outcome']}</b>.
            epsilon-squared = <b>{best['epsilon_squared']:.3f}</b>,
            interpreted as <b>{best['effect_size_interpretation']}</b>.
            """
        )

    with st.expander("Show validation table"):
        st.dataframe(selected_gap_df, use_container_width=True)

    st.markdown("### Analytical priority overview")

    if not priority_table.empty:
        st.dataframe(priority_table, use_container_width=True, hide_index=True)


# =============================================================================
# TAB 4: REGRESSION EVIDENCE
# =============================================================================

with tabs[3]:
    st.subheader("Regression Evidence")

    insight_box(
        """
        <b>Key takeaway:</b> Political efficacy and social trust remain the strongest positive signals
        when several factors are considered at the same time. The dots show regression coefficients;
        the horizontal lines show 95% confidence intervals.
        """
    )

    plot_df = regression_results.copy()
    plot_df = plot_df[plot_df["term"] != "Intercept"].copy()

    term_labels = {
        "C(gndr)[T.2.0]": "Gender",
        "political_efficacy_index_z": "Political efficacy",
        "social_trust_index_z": "Social trust",
        "hincfel_z": "Income feeling",
        "lrscale_z": "Left-right placement",
        "eduyrs_z": "Education",
        "agea_z": "Age",
        "vote_binary": "Voted"
    }

    plot_df["label"] = plot_df["term"].map(term_labels).fillna(plot_df["term"])
    plot_df["significant"] = np.where(plot_df["p_value"] < 0.05, "p < 0.05", "not significant")

    order = (
        plot_df
        .groupby("label")["coefficient"]
        .apply(lambda x: x.abs().mean())
        .sort_values()
        .index
        .tolist()
    )

    fig = go.Figure()

    models = plot_df["model"].unique()

    model_colors = OUTCOME_COLORS

    model_offsets = {
        "Democracy satisfaction": -0.12,
        "Trust in political parties": 0.12
    }

    y_base = {label: i for i, label in enumerate(order)}

    for model in models:
        sub = plot_df[plot_df["model"] == model].set_index("label").loc[order].reset_index()
        sub["y_position"] = sub["label"].map(y_base) + model_offsets.get(model, 0)

        fig.add_trace(
            go.Scatter(
                x=sub["coefficient"],
                y=sub["y_position"],
                mode="markers",
                marker=dict(
                    size=12,
                    color=model_colors.get(model, "#F0E442"),
                    line=dict(width=1, color="white")
                ),
                error_x=dict(
                    type="data",
                    symmetric=False,
                    array=sub["conf_high"] - sub["coefficient"],
                    arrayminus=sub["coefficient"] - sub["conf_low"],
                    thickness=1.5,
                    width=4
                ),
                name=model,
                customdata=np.stack(
                    [
                        sub["label"],
                        sub["p_value"],
                        sub["conf_low"],
                        sub["conf_high"]
                    ],
                    axis=-1
                ),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Coefficient: %{x:.3f}<br>"
                    "p-value: %{customdata[1]:.5f}<br>"
                    "95% CI: [%{customdata[2]:.3f}, %{customdata[3]:.3f}]"
                    "<extra></extra>"
                )
            )
        )

    fig.update_yaxes(
        tickmode="array",
        tickvals=list(y_base.values()),
        ticktext=list(y_base.keys())
    ) 
    fig.add_vline(x=0, line_dash="dash", line_color="rgba(242,242,242,0.65)")

    fig = plot_layout(
        fig,
        title="Regression Coefficients with 95% Confidence Intervals",
        height=620,
        x_title="Regression coefficient",
        y_title="Predictor"
    )

    st.plotly_chart(fig, use_container_width=True)

    method_box(
        """
        Reading guide: Coefficients to the right of zero indicate a positive association with the outcome.
        Coefficients to the left indicate a negative association. Horizontal lines show 95% confidence intervals.
        Political efficacy and social trust stand out as the strongest positive predictors in both models.
        """
    )

    c1, c2 = st.columns([1.1, 0.9])

    with c1:
        st.markdown("### Model comparison")
        st.dataframe(regression_model_comparison, use_container_width=True, hide_index=True)

    with c2:
        st.markdown("### Core interpretation")
        st.markdown(
            """
            - Political efficacy remains the strongest predictor.
            - Social trust is the second strongest predictor.
            - The models explain around one quarter of the variation.
            - Results are associational, not causal.
            """
        )

    with st.expander("Show full regression results"):
        st.dataframe(regression_results, use_container_width=True, hide_index=True)

    if not diagnostic_summary.empty:
        with st.expander("Show regression diagnostics summary"):
            st.dataframe(diagnostic_summary, use_container_width=True, hide_index=True)

    if not vif_results.empty:
        with st.expander("Show multicollinearity diagnostics"):
            st.dataframe(vif_results, use_container_width=True, hide_index=True)


# =============================================================================
# TAB 5: PROFILES
# =============================================================================

with tabs[4]:
    st.subheader("Democratic Connection Profiles")

    insight_box(
        """
        <b>Key takeaway:</b> Democratic disengagement is not only about non-voters.
        A large group still votes, but shows low democratic satisfaction and low party trust.
        Voting alone is therefore not enough to understand democratic stability.
        """
    )

    size_df = profile_summary.copy()
    size_df = size_df.sort_values("percentage", ascending=True)

    fig = px.bar(
        size_df,
        x="percentage",
        y="democratic_connection_profile",
        orientation="h",
        color="democratic_connection_profile",
        color_discrete_map=COLOR_MAP,
        text=size_df.apply(
            lambda row: f"{row['percentage']:.1f}% | n={int(row['n_respondents'])}",
            axis=1
        ),
        labels={
            "percentage": "Share of respondents (%)",
            "democratic_connection_profile": "Democratic Connection Profile"
        }
    )

    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(range=[0, max(size_df["percentage"]) + 12])

    fig = plot_layout(
        fig,
        title="Profile Sizes: Three Forms of Democratic Connection",
        height=450,
        x_title="Share of respondents (%)",
        y_title="Profile"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Profile cards")

    card_cols = st.columns(3)

    for i, profile_name in enumerate([
        "Connected Democratic Core",
        "Disappointed Democratic Participants",
        "Disengaged Non-voters"
    ]):
        row = profile_summary[
            profile_summary["democratic_connection_profile"] == profile_name
        ]

        if row.empty:
            continue

        row = row.iloc[0]
        color = COLOR_MAP.get(profile_name, "#56B4E9")

        with card_cols[i]:
            st.markdown(
                f"""
                <div class="profile-card" style="border-top: 5px solid {color};">
                    <div class="profile-title" style="color:{color};">{profile_name}</div>
                    <div class="profile-meta">{row['percentage']:.1f}% of respondents · n={int(row['n_respondents'])}</div>
                    <div class="small-muted">
                        Democracy satisfaction: <b>{row['democracy_satisfaction']:.2f}</b><br>
                        Party trust: <b>{row['party_trust']:.2f}</b><br>
                        Political efficacy: <b>{row['political_efficacy']:.2f}</b><br>
                        Social trust: <b>{row['social_trust']:.2f}</b><br>
                        Voted share: <b>{row['voted_share']:.2f}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### What differentiates the profiles?")

    profile_vars = [
        "democracy_satisfaction",
        "party_trust",
        "political_efficacy",
        "social_trust",
        "income_feeling",
        "left_right_placement",
        "voted_share"
    ]

    profile_labels = {
        "democracy_satisfaction": "Democracy satisfaction",
        "party_trust": "Party trust",
        "political_efficacy": "Political efficacy",
        "social_trust": "Social trust",
        "income_feeling": "Income feeling",
        "left_right_placement": "Left-right placement",
        "voted_share": "Voted share"
    }

    char_long = profile_summary[
        ["democratic_connection_profile"] + profile_vars
    ].melt(
        id_vars="democratic_connection_profile",
        var_name="indicator",
        value_name="mean_value"
    )

    char_long["indicator"] = char_long["indicator"].map(profile_labels)

    fig = px.bar(
        char_long,
        x="indicator",
        y="mean_value",
        color="democratic_connection_profile",
        barmode="group",
        color_discrete_map=COLOR_MAP,
        text=char_long["mean_value"].round(2),
        labels={
            "indicator": "Profile indicator",
            "mean_value": "Mean value",
            "democratic_connection_profile": "Profile"
        }
    )

    fig.update_traces(textposition="outside")
    fig = plot_layout(
        fig,
        title="Profile Characteristics Using Original Mean Values",
        height=620,
        x_title="Profile indicator",
        y_title="Mean value"
    )

    st.plotly_chart(fig, use_container_width=True)

    if not profile_z.empty:
        st.markdown("### Standardized profile differences")

        z_long = profile_z.melt(
            id_vars="democratic_connection_profile",
            var_name="indicator",
            value_name="standardized_difference"
        )

        z_long["democratic_connection_profile"] = pd.Categorical(
            z_long["democratic_connection_profile"],
            categories=PROFILE_ORDER,
            ordered=True
        )

        fig = px.bar(
            z_long,
            x="standardized_difference",
            y="indicator",
            color="democratic_connection_profile",
            barmode="group",
            color_discrete_map=COLOR_MAP,
            labels={
                "standardized_difference": "Standardized difference from sample average",
                "indicator": "Indicator",
                "democratic_connection_profile": "Profile"
            }
        )

        fig.add_vline(x=0, line_dash="dash", line_color="#F2F2F2")

        fig = plot_layout(
            fig,
            title="Standardized Profile Differences from Sample Average",
            height=620,
            x_title="Standardized difference from sample average",
            y_title="Indicator"
        )

        st.plotly_chart(fig, use_container_width=True)

        method_box(
            """
            Reading guide: Values above zero mean that a profile scores above the sample average on that indicator.
            Values below zero mean that a profile scores below the sample average. This chart is better for comparing
            variables measured on different scales.
            """
        )

    with st.expander("Show profile summary table"):
        st.dataframe(profile_summary, use_container_width=True, hide_index=True)


# =============================================================================
# TAB 6: PCA EXPLORER
# =============================================================================

with tabs[5]:
    st.subheader("PCA Explorer")

    if pca_data.empty:
        st.warning(
            "PCA files were not found in `data/processed`. Run the PCA notebook section first and export the PCA outputs."
        )
    else:
        insight_box(
            """
            PCA reduces the multidimensional profile variables into visual components.
            It helps show the broad structure of democratic connection, but it does not prove cluster validity.
            """
        )

        method_box(
            """
            The original variables are measured on different scales, including 0–10 trust scales,
            index variables and binary voting participation. Before PCA, all variables were standardized
            using z-scores. This ensures that no variable dominates the PCA only because it has a larger
            numerical scale.
            """,
            title="Method note: Why standardization matters"
        )

        method_box(
            """
            PC1 summarizes the broad democratic connection dimension. Respondents further to the right
            tend to show higher democratic satisfaction, higher party trust, higher political efficacy and higher social trust.
            PC2 captures a secondary profile dimension, mainly helping to distinguish different forms of weaker connection.
            """,
            title="Reading guide: How to interpret PC1 and PC2"
        )

        st.caption(
            "In short: points further to the right generally indicate stronger democratic connection; profile overlap is expected in survey data."
        )

        pca_filtered = pca_data.copy()

        pc1_var = None
        pc2_var = None
        pc3_var = None

        if not pca_variance.empty and "explained_variance_percent" in pca_variance.columns:
            if len(pca_variance) >= 1:
                pc1_var = pca_variance.loc[pca_variance.index[0], "explained_variance_percent"]
            if len(pca_variance) >= 2:
                pc2_var = pca_variance.loc[pca_variance.index[1], "explained_variance_percent"]
            if len(pca_variance) >= 3:
                pc3_var = pca_variance.loc[pca_variance.index[2], "explained_variance_percent"]

        x_label = (
            f"PC1 – Democratic connection dimension ({pc1_var:.1f}% explained variance)"
            if pc1_var is not None
            else "PC1 – Democratic connection dimension"
        )

        y_label = (
            f"PC2 – secondary profile dimension ({pc2_var:.1f}% explained variance)"
            if pc2_var is not None
            else "PC2 – secondary profile dimension"
        )

        # -------------------------------------------------------------
        # 2D PCA Map: cleaner visual hierarchy
        # -------------------------------------------------------------

        fig = go.Figure()

        for profile in PROFILE_ORDER:
            sub = pca_filtered[
                pca_filtered["democratic_connection_profile"] == profile
            ].copy()

            if sub.empty:
                continue

            fig.add_trace(
                go.Scattergl(
                    x=sub["PC1"],
                    y=sub["PC2"],
                    mode="markers",
                    name=profile,
                    marker=dict(
                        size=5,
                        color=COLOR_MAP.get(profile, "#F2F2F2"),
                        opacity=0.46,
                        line=dict(width=0)
                    ),
                    customdata=np.stack(
                        [
                            sub[col] if col in sub.columns else pd.Series([np.nan] * len(sub))
                            for col in [
                                "Democracy satisfaction",
                                "Party trust",
                                "Political efficacy",
                                "Social trust",
                                "Income feeling",
                                "Left-right placement",
                                "Voting participation"
                            ]
                        ],
                        axis=-1
                    ),
                    hovertemplate=(
                        "<b>" + profile + "</b><br>"
                        "PC1: %{x:.2f}<br>"
                        "PC2: %{y:.2f}<br><br>"
                        "Democracy satisfaction: %{customdata[0]:.2f}<br>"
                        "Party trust: %{customdata[1]:.2f}<br>"
                        "Political efficacy: %{customdata[2]:.2f}<br>"
                        "Social trust: %{customdata[3]:.2f}<br>"
                        "Income feeling: %{customdata[4]:.2f}<br>"
                        "Left-right placement: %{customdata[5]:.2f}<br>"
                        "Voting participation: %{customdata[6]}"
                        "<extra></extra>"
                    )
                )
            )

        centroids = (
            pca_filtered
            .groupby("democratic_connection_profile")[["PC1", "PC2"]]
            .mean()
            .reset_index()
        )

        # White backing layer for centroid visibility
        fig.add_trace(
            go.Scatter(
                x=centroids["PC1"],
                y=centroids["PC2"],
                mode="markers",
                marker=dict(
                    size=25,
                    color="#F2F2F2",
                    symbol="diamond",
                    line=dict(width=0)
                ),
                name="Profile centroid",
                hoverinfo="skip",
                showlegend=True
            )
        )

        # Colored centroid layer on top
        fig.add_trace(
            go.Scatter(
                x=centroids["PC1"],
                y=centroids["PC2"],
                mode="markers",
                marker=dict(
                    size=18,
                    color=[
                        COLOR_MAP.get(profile, "#F2F2F2")
                        for profile in centroids["democratic_connection_profile"]
                    ],
                    symbol="diamond",
                    line=dict(width=2, color="#0E1117")
                ),
                name="Centroid highlight",
                hovertemplate=(
                    "<b>%{customdata}</b><br>"
                    "Profile centroid<br>"
                    "PC1: %{x:.2f}<br>"
                    "PC2: %{y:.2f}"
                    "<extra></extra>"
                ),
                customdata=centroids["democratic_connection_profile"],
                showlegend=False
            )
        )

        # Clean centroid labels as annotations
        for _, row in centroids.iterrows():
            fig.add_annotation(
                x=row["PC1"],
                y=row["PC2"],
                text=row["democratic_connection_profile"],
                showarrow=False,
                yshift=24,
                font=dict(size=12, color="#F2F2F2"),
                bgcolor="rgba(14,17,23,0.82)",
                bordercolor="rgba(255,255,255,0.16)",
                borderwidth=1,
                borderpad=4
            )

        fig.add_hline(
            y=0,
            line_width=1,
            line_dash="dash",
            line_color="rgba(255,255,255,0.25)"
        )

        fig.add_vline(
            x=0,
            line_width=1,
            line_dash="dash",
            line_color="rgba(255,255,255,0.25)"
        )

        fig = plot_layout(
            fig,
            title="2D PCA Map of Democratic Connection Profiles",
            height=700,
            x_title=x_label,
            y_title=y_label
        )

        fig.update_layout(
            margin=dict(l=30, r=30, t=150, b=55),
            title=dict(
                text="2D PCA Map of Democratic Connection Profiles",
                x=0.02,
                xanchor="left",
                y=0.97,
                font=dict(size=21)
            ),
            legend=dict(
                title=None,
                orientation="h",
                yanchor="top",
                y=1.04,
                xanchor="center",
                x=0.55,
                itemsizing="constant"
            )
        )

        fig.update_xaxes(
            zeroline=False,
            showline=False,
            gridcolor="rgba(255,255,255,0.07)"
        )

        fig.update_yaxes(
            zeroline=False,
            showline=False,
            gridcolor="rgba(255,255,255,0.07)"
        )

        st.plotly_chart(fig, use_container_width=True)

        method_box(
            """
            Reading guide: Each dot represents one respondent in a reduced two-dimensional space.
            Profile centroids show the average position of each profile. PC1 mainly represents a broad
            democratic connection dimension. Profile overlap is expected in social survey data.
            """
        )

        if {"PC1", "PC2", "PC3"}.issubset(pca_data.columns):
            st.markdown("### Interactive 3D PCA view")

            method_box(
                """
                This 3D view is an exploratory visualization. PC1, PC2 and PC3 are synthetic dimensions
                created from the original profile variables. The chart helps inspect profile overlap and
                separation, but the main interpretation should still rely on the validated trust gaps,
                regression models and profile summaries.
                """
            )

            pc1_short = f"PC1 ({pc1_var:.1f}%)" if pc1_var is not None else "PC1"
            pc2_short = f"PC2 ({pc2_var:.1f}%)" if pc2_var is not None else "PC2"
            pc3_short = f"PC3 ({pc3_var:.1f}%)" if pc3_var is not None else "PC3"

            fig_3d = px.scatter_3d(
                pca_filtered,
                x="PC1",
                y="PC2",
                z="PC3",
                color="democratic_connection_profile",
                color_discrete_map=COLOR_MAP,
                opacity=0.75,
                hover_data=[
                    col for col in [
                        "Democracy satisfaction",
                        "Party trust",
                        "Political efficacy",
                        "Social trust",
                        "Income feeling",
                        "Left-right placement",
                        "Voting participation"
                    ]
                    if col in pca_filtered.columns
                ],
                labels={
                    "PC1": pc1_short,
                    "PC2": pc2_short,
                    "PC3": pc3_short,
                    "democratic_connection_profile": "Profile"
                }
            )

            fig_3d.update_traces(
                marker=dict(
                    size=4,
                    line=dict(width=0)
                )
            )

            fig_3d.update_layout(
                template=PLOT_TEMPLATE,
                height=720,
                paper_bgcolor="#0E1117",
                plot_bgcolor="#0E1117",
                font=dict(color="#F2F2F2"),
                title=dict(
                    text="Interactive 3D PCA Map",
                    x=0.02,
                    xanchor="left",
                    font=dict(size=21)
                ),
                scene=dict(
                    xaxis_title=pc1_short,
                    yaxis_title=pc2_short,
                    zaxis_title=pc3_short,
                    bgcolor="#0E1117"
                ),
                legend=dict(title=None),
                margin=dict(l=0, r=0, b=0, t=70)
            )

            st.plotly_chart(fig_3d, use_container_width=True)

            explained_3d = None

            if pc1_var is not None and pc2_var is not None and pc3_var is not None:
                explained_3d = f"{pc1_var + pc2_var + pc3_var:.1f}%"
            else:
                explained_3d = "the majority"

            method_box(
                f"""
                Reading guide: The 3D map shows respondents in a simplified PCA space. 
                <b>PC1</b> is the main democratic connection dimension. Higher PC1 values generally indicate
                higher democratic satisfaction, higher party trust, higher political efficacy and higher social trust.
                <b>PC2</b> captures a secondary distinction between profile patterns.
                <b>PC3</b> adds another exploratory dimension, mainly useful for inspecting additional separation
                between the profiles. Together, the first three components explain approximately
                <b>{explained_3d}</b> of the variation in the selected profile variables.
                """
            )
            with st.expander("What variables are included in the PCA?"):
                st.markdown(
                    """
                    The PCA is based on the same core variables used to construct the Democratic Connection Profiles:

                    - **Democracy satisfaction**
                    - **Party trust**
                    - **Political efficacy**
                    - **Social trust**
                    - **Income feeling**
                    - **Left-right placement**
                    - **Voting participation**

                    These variables were standardized before PCA so that variables measured on different scales can be compared.
                    """
                )

                if not pca_loadings.empty:
                    st.markdown("#### PCA component loadings")

                    loadings_explainer = pca_loadings.copy()

                    if "Unnamed: 0" in loadings_explainer.columns:
                        loadings_explainer = loadings_explainer.rename(columns={"Unnamed: 0": "Indicator"})
                    elif loadings_explainer.columns[0] not in ["Indicator", "indicator", "variable"]:
                        loadings_explainer = loadings_explainer.rename(columns={loadings_explainer.columns[0]: "Indicator"})
                    elif loadings_explainer.columns[0] == "indicator":
                        loadings_explainer = loadings_explainer.rename(columns={"indicator": "Indicator"})
                    elif loadings_explainer.columns[0] == "variable":
                        loadings_explainer = loadings_explainer.rename(columns={"variable": "Indicator"})

                    st.dataframe(
                        loadings_explainer,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.markdown(
                        """
                        **How to read this table:**  
                        Loadings show how strongly each original variable contributes to each principal component.
                        Large positive or negative values mean that the variable strongly shapes that component.

                        **Interpretation:**  
                        PC1 is the clearest dimension because democratic satisfaction, party trust, political efficacy
                        and social trust all load strongly in the same direction.
                        """
                    )

        if not pca_loadings.empty:
            st.markdown("### PCA component loadings")

            loadings_plot = pca_loadings.copy()

            if "Unnamed: 0" in loadings_plot.columns:
                loadings_plot = loadings_plot.rename(columns={"Unnamed: 0": "indicator"})
            elif loadings_plot.columns[0] not in ["indicator", "variable"]:
                loadings_plot = loadings_plot.rename(columns={loadings_plot.columns[0]: "indicator"})
            elif loadings_plot.columns[0] == "variable":
                loadings_plot = loadings_plot.rename(columns={"variable": "indicator"})

            loading_cols = [col for col in loadings_plot.columns if "PC" in col]

            if loading_cols:
                selected_pc = st.selectbox(
                    "Select PCA component for loading chart",
                    options=loading_cols,
                    index=0
                )

                loading_sorted = loadings_plot.sort_values(selected_pc)

                fig_load = px.bar(
                    loading_sorted,
                    x=selected_pc,
                    y="indicator",
                    orientation="h",
                    text=loading_sorted[selected_pc].round(2),
                    labels={
                        selected_pc: "Component loading",
                        "indicator": "Original variable"
                    }
                )

                fig_load.add_vline(x=0, line_dash="dash", line_color="#F2F2F2")

                fig_load = plot_layout(
                    fig_load,
                    title=f"Variable Loadings for {selected_pc}",
                    height=500,
                    x_title="Component loading",
                    y_title="Original variable"
                )

                st.plotly_chart(fig_load, use_container_width=True)

            with st.expander("Show PCA tables"):
                c1, c2 = st.columns(2)

                with c1:
                    st.markdown("Explained variance")
                    st.dataframe(pca_variance, use_container_width=True, hide_index=True)

                with c2:
                    st.markdown("Component loadings")
                    st.dataframe(pca_loadings, use_container_width=True)

# =============================================================================
# TAB 7: STRATEGY
# =============================================================================

with tabs[6]:
    st.subheader("Strategy Implications")

    insight_box(
        """
        <b>Key takeaway:</b> If political efficacy is the strongest signal, democratic actors need more
        than better messaging. They need credible experiences of voice, responsiveness and social connection.
        """
    )

    for _, row in strategy_table.iterrows():
        profile = row["democratic_connection_profile"]
        color = COLOR_MAP.get(profile, "#56B4E9")

        st.markdown(
            f"""
            <div class="profile-card" style="border-left: 6px solid {color}; margin-bottom: 1rem;">
                <div class="profile-title" style="color:{color};">{profile}</div>
                <div class="small-muted"><b>Main pattern:</b> {row['main_pattern']}</div>
                <br>
                <div class="small-muted"><b>Strategic challenge:</b> {row['strategic_challenge']}</div>
                <br>
                <div class="small-muted"><b>Possible response:</b> {row['possible_response']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### From findings to action logic")

    action_df = pd.DataFrame(
        [
            {
                "Analytical finding": "Political efficacy is the strongest signal",
                "Strategic implication": "Strengthen voice, influence and meaningful participation."
            },
            {
                "Analytical finding": "Social trust is consistently associated with democratic trust",
                "Strategic implication": "Build social confidence through community-based and relational formats."
            },
            {
                "Analytical finding": "Disappointed voters are a large risk group",
                "Strategic implication": "Do not treat electoral participation as sufficient democratic connection."
            },
            {
                "Analytical finding": "Non-voters show low efficacy and low trust",
                "Strategic implication": "Use low-threshold outreach beyond traditional political channels."
            },
            {
                "Analytical finding": "Economic strain matters, but is not the only factor",
                "Strategic implication": "Connect material policy delivery with responsiveness and agency."
            },
        ]
    )

    st.dataframe(action_df, use_container_width=True, hide_index=True)

# =============================================================================
# TAB 8: PARTY POSITION TRANSFER LAYER
# =============================================================================

with tabs[7]:
    st.subheader("Party Position Transfer Layer")

    insight_box(
        """
        <b>Optional transfer layer:</b> This section connects the ESS-based findings with standardized
        Wahl-O-Mat 2025 party positions. It is an exploratory issue-alignment map, not a party ranking
        and not a full manifesto analysis.
        """
    )

    method_box(
        """
        Important: This is not a party ranking and not a claim that one party is more democratic than another.
        The heatmap only shows directional alignment between selected Wahl-O-Mat 2025 issue positions and
        the democratic connection dimensions coded for this project.

        The party-position layer is not based on full party manifestos. It uses a standardized set of
        Wahl-O-Mat 2025 issue positions, which improves comparability because all parties answer the same issues,
        but limits substantive completeness. Results are therefore issue-set dependent and exploratory.
        """,
        title="Important methodological note"
    )

    if party_alignment_matrix.empty or party_alignment_long.empty:
        st.warning(
            "Party alignment files were not found. Please export the app-ready party alignment files from the transfer-layer notebook first."
        )
    else:
        party_order = ["SPD", "CDU / CSU", "GRÜNE", "FDP", "Die Linke", "BSW", "AfD"]

        dimension_order = [
            "Democratic institutions and rule of law",
            "Institutional responsiveness",
            "Economic security",
            "Participation and civic inclusion",
            "Social trust and cohesion",
            "Direct participation / political voice"
        ]

        heatmap_df = party_alignment_matrix.copy()
        heatmap_df = heatmap_df.set_index("party")

        heatmap_df = heatmap_df.loc[
            [party for party in party_order if party in heatmap_df.index]
        ]

        heatmap_df = heatmap_df[
            [dimension for dimension in dimension_order if dimension in heatmap_df.columns]
        ]

        fig = px.imshow(
            heatmap_df,
            text_auto=".2f",
            color_continuous_scale=ALIGNMENT_COLOR_SCALE,
            zmin=-1,
            zmax=1,
            aspect="auto",
            labels=dict(
                x="Democratic connection dimension",
                y="Party",
                color="Alignment score"
            )
        )

        fig.update_layout(
            template=PLOT_TEMPLATE,
            height=620,
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font=dict(color="#F2F2F2"),
            title=dict(
                text="Party Positions and Democratic Connection Priorities",
                x=0.02,
                xanchor="left",
                font=dict(size=22)
            ),
            margin=dict(l=40, r=40, t=90, b=135),
            coloraxis_colorbar=dict(
                title="Alignment",
                tickvals=[-1, 0, 1],
                ticktext=["negative", "mixed", "positive"]
            )
        )

        fig.update_xaxes(tickangle=35)
        fig.update_traces(
            hovertemplate=(
                "<b>Party:</b> %{y}<br>"
                "<b>Dimension:</b> %{x}<br>"
                "<b>Alignment score:</b> %{z:.2f}<br>"
                "<extra></extra>"
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        method_box(
            """
            Reading guide: Positive values indicate visible alignment with the coded democratic connection priority.
            Negative values indicate visible misalignment. Values around zero indicate mixed or neutral positioning.
            The score is calculated as party position × issue alignment direction.
            """
        )

        st.markdown("### Evidence strength by dimension")

        if not party_dimension_evidence.empty:
            evidence_display = party_dimension_evidence.copy()

            evidence_display = evidence_display.rename(columns={
                "connection_dimension_label_refined": "Democratic connection dimension",
                "n_issues": "Number of issues",
                "n_party_positions": "Party positions coded",
                "evidence_strength": "Evidence strength"
            })

            st.dataframe(
                evidence_display.sort_values("Number of issues", ascending=False),
                use_container_width=True,
                hide_index=True
            )

            method_box(
                """
                Dimensions are not equally covered by the Wahl-O-Mat issue set.
                Economic security, democratic institutions and institutional responsiveness have stronger issue coverage.
                Social trust and direct participation are weakly covered and should be interpreted with extra caution.
                """
            )

        st.markdown("### Party-specific detail view")

        selected_party = st.selectbox(
            "Select party",
            options=[party for party in party_order if party in party_alignment_long["party"].unique()],
            index=0
        )

        party_detail = party_alignment_long[
            party_alignment_long["party"] == selected_party
        ].copy()

        party_detail = party_detail.sort_values("alignment_score", ascending=False)

        fig_party = px.bar(
            party_detail,
            x="alignment_score",
            y="democratic_connection_dimension",
            orientation="h",
            color="alignment_score",
            color_continuous_scale=ALIGNMENT_COLOR_SCALE,
            range_color=[-1, 1],
            text=party_detail["alignment_score"].round(2),
            labels={
                "alignment_score": "Alignment score",
                "democratic_connection_dimension": "Democratic connection dimension"
            },
            title=f"Alignment Profile: {selected_party}"
        )

        fig_party.add_vline(x=0, line_dash="dash", line_color="#F2F2F2")

        fig_party = plot_layout(
            fig_party,
            title=f"Alignment Profile: {selected_party}",
            height=480,
            x_title="Directional alignment score",
            y_title="Democratic connection dimension"
        )

        fig_party.update_layout(showlegend=False)
        fig_party.update_xaxes(range=[-1, 1])

        st.plotly_chart(fig_party, use_container_width=True)

        with st.expander("Show party alignment data"):
            st.dataframe(
                party_detail,
                use_container_width=True,
                hide_index=True
            )

        if not party_alignment_summary.empty:
            with st.expander("Show cautious party-level summary"):
                st.warning(
                    "This table can look like a ranking, but it should not be interpreted as a normative party ranking. "
                    "It only summarizes average alignment within the selected Wahl-O-Mat issue set."
                )
                st.dataframe(
                    party_alignment_summary,
                    use_container_width=True,
                    hide_index=True
                )
# =============================================================================
# TAB 9: METHOD NOTES
# =============================================================================

with tabs[8]:
    st.subheader("Method Notes and Interpretation Boundaries")

    st.markdown(
        """
        ### Data and scope

        This project uses the European Social Survey Round 11 Germany subset. The analysis focuses on
        selected variables related to democratic satisfaction, institutional trust, political efficacy,
        social trust, subjective income feeling, political orientation and voting behavior.

        The German ESS Round 11 fieldwork used a probability-based sampling design based on municipality
        population registers and computer-assisted face-to-face interviews. The official response rate for
        Germany is 26.7%. This is an important limitation because nonresponse may be systematic: people with
        lower political trust, lower institutional confidence or stronger disengagement may be less likely to
        participate in a political survey. The analysis therefore focuses on associational patterns in the
        achieved sample and avoids overclaiming population-level causal conclusions.

        ### Statistical interpretation

        The analysis is based on cross-sectional survey data. Therefore, all results are interpreted as
        associations, not causal effects.

        ### Effect sizes

        Statistical significance indicates whether a difference is unlikely to be random under the test assumptions.
        Effect sizes indicate whether a difference is practically meaningful.

        ### Regression models

        The regression models use robust HC3 standard errors and standardized predictors where useful.
        The models are intended to support careful interpretation, not individual-level prediction.

        ### Clustering

        K-Means clustering is exploratory. The Democratic Connection Profiles are segmentation patterns,
        not fixed identities or deterministic social groups.

        ### PCA

        PCA is used as a visualization aid. It helps show multidimensional structure, but it does not prove
        that clusters are objectively fixed or sharply separated.

        ### Party-position transfer layer

        The party-position transfer layer uses standardized Wahl-O-Mat 2025 party positions. This improves
        comparability because all included parties respond to the same issue set. However, it does not replace
        a full manifesto analysis and should not be interpreted as a complete representation of party ideology
        or party strategy.

        The alignment scores show how selected issue positions relate to the democratic connection dimensions
        coded for this project. They are exploratory and should not be interpreted as a normative party ranking.

        ### Ethical note

        The project does not classify individuals as democrats or anti-democrats. Political orientation is treated
        descriptively and without stigmatizing claims.
        """
    )

    st.markdown("### Available project outputs")

    output_summary = pd.DataFrame(
        {
            "Output type": [
                "Clean analysis data",
                "Validation tables",
                "Regression results",
                "Profile summaries",
                "PCA outputs",
                "Streamlit app"
            ],
            "Purpose": [
                "Reproducible analysis and dashboard input",
                "Document hypothesis tests and effect sizes",
                "Show controlled associations with democratic satisfaction and party trust",
                "Translate survey patterns into democratic connection profiles",
                "Visualize multidimensional profile structure",
                "Communicate the project interactively"
            ]
        }
    )

    st.dataframe(output_summary, use_container_width=True, hide_index=True)


# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown(
    """
    <div class="small-muted">
    Built with Streamlit · Data source: European Social Survey Round 11 · Germany subset.
    Results are exploratory and associational.
    </div>
    """,
    unsafe_allow_html=True
)
