# app/app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="What Builds Democratic Connection?",
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
        padding: 2.1rem 2.3rem;
        border-radius: 24px;
        background:
            radial-gradient(circle at top left, rgba(86,180,233,0.25), transparent 35%),
            radial-gradient(circle at bottom right, rgba(204,121,167,0.18), transparent 35%),
            linear-gradient(135deg, #111827 0%, #161B22 55%, #0E1117 100%);
        border: 1px solid var(--border-soft);
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

COLOR_MAP = {
    "Connected Democratic Core": "#009E73",
    "Disappointed Democratic Participants": "#CC79A7",
    "Disengaged Non-voters": "#F0E442",
    "Political efficacy": "#56B4E9",
    "Social trust": "#009E73",
    "Income feeling": "#F0E442",
    "Left-right placement": "#CC79A7",
    "Voted": "#56B4E9",
    "Democracy satisfaction": "#56B4E9",
    "Trust in political parties": "#CC79A7",
    "Trust in parliament": "#009E73",
    "Trust in politicians": "#F0E442",
}

PROFILE_ORDER = [
    "Disengaged Non-voters",
    "Disappointed Democratic Participants",
    "Connected Democratic Core",
]

PLOT_TEMPLATE = "plotly_dark"


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


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

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


def method_box(text):
    st.markdown(f"""<div class="method-box">{text}</div>""", unsafe_allow_html=True)


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

st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">ESS Round 11 · Germany · Democratic Trust Analysis</div>
        <div class="hero-title">What Builds Democratic Connection?</div>
        <div class="hero-subtitle">
            A data-driven analysis of democratic satisfaction, party trust, political efficacy,
            social trust and political participation in Germany. The project translates survey evidence
            into exploratory democratic connection profiles and strategic implications.
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
    "Hypothesis Testing",
    "Trust Gaps",
    "Regression Evidence",
    "Democratic Connection Profiles",
    "PCA Explorer",
    "Strategy Implications",
    "Method Notes"
])


# =============================================================================
# TAB 1: OVERVIEW
# =============================================================================

with tabs[0]:
    st.subheader("Overview: From democratic attitudes to democratic connection")

    insight_box(
        """
        <b>Core idea:</b> Democratic disconnection is not one single problem.
        The analysis therefore combines democratic satisfaction, institutional trust,
        perceived political efficacy, social trust, economic security and political participation.
        """
    )

    method_box(
        """
        Data source: European Social Survey Round 11, Germany subset. All results are interpreted as
        associations, not causal effects. Survey scales usually range from 0 to 10, where higher values
        indicate higher satisfaction or trust unless stated otherwise.
        """
    )

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

    st.markdown("### Analytical pipeline")

    pipeline_col1, pipeline_col2, pipeline_col3 = st.columns(3)

    with pipeline_col1:
        st.markdown(
            """
            **1. Evidence base**
            - ESS11 Germany subset
            - variable selection
            - cleaning and index construction
            """
        )

    with pipeline_col2:
        st.markdown(
            """
            **2. Statistical validation**
            - group comparisons
            - effect sizes
            - regression models
            """
        )

    with pipeline_col3:
        st.markdown(
            """
            **3. Strategic translation**
            - democratic connection profiles
            - PCA visualization
            - engagement implications
            """
        )


# =============================================================================
# TAB 2: HYPOTHESIS TESTING
# =============================================================================

with tabs[1]:
    st.subheader("Hypothesis Testing")

    insight_box(
        """
        This section summarizes the predefined analytical hypotheses tested in the project.
        The results should be read as associational evidence, not as causal proof.
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

        st.markdown("### Full hypothesis summary table")

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
        This section summarizes the main trust gap hypotheses. The goal is to identify which forms of
        democratic disconnection are statistically visible and practically meaningful.
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
            color_discrete_map={
                "Voted": "#009E73",
                "Did not vote": "#CC79A7"
            },
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
            color_discrete_map={
                "Secure or coping": "#009E73",
                "Economically strained": "#CC79A7"
            },
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
        Regression models test whether political efficacy and social trust remain associated with
        democratic satisfaction and party trust when other variables are considered at the same time.
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

    model_colors = {
        "Democracy satisfaction": "#56B4E9",
        "Trust in political parties": "#CC79A7"
    }

    for model in models:
        sub = plot_df[plot_df["model"] == model].set_index("label").loc[order].reset_index()

        fig.add_trace(
            go.Scatter(
                x=sub["coefficient"],
                y=sub["label"],
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
                        sub["p_value"],
                        sub["conf_low"],
                        sub["conf_high"]
                    ],
                    axis=-1
                ),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Coefficient: %{x:.3f}<br>"
                    "p-value: %{customdata[0]:.5f}<br>"
                    "95% CI: [%{customdata[1]:.3f}, %{customdata[2]:.3f}]"
                    "<extra></extra>"
                )
            )
        )

    fig.add_vline(x=0, line_dash="dash", line_color="#F0E442")

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
        The profile analysis translates variable-level findings into an exploratory segmentation.
        The key insight is that democratic disconnection is not only visible among non-voters.
        A large group still votes while showing low democratic satisfaction and low party trust.
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
        Reading guide: PC1 summarizes the broad democratic connection dimension. Respondents further to the right
        tend to show higher democratic satisfaction, higher party trust, higher political efficacy and higher social trust.
        PC2 captures a secondary profile dimension, mainly helping to distinguish different forms of weaker connection.
        """
        )

        pca_filtered = pca_data.copy()

        pc1_var = None
        pc2_var = None

        if not pca_variance.empty:
            if "explained_variance_percent" in pca_variance.columns:
                pc1_var = pca_variance.loc[pca_variance.index[0], "explained_variance_percent"]
                pc2_var = pca_variance.loc[pca_variance.index[1], "explained_variance_percent"] if len(pca_variance) > 1 else None

        x_label = f"PC1 – Democratic connection dimension ({pc1_var:.1f}% explained variance)" if pc1_var is not None else "PC1 – Democratic connection dimension"
        y_label = f"PC2 – secondary profile dimension ({pc2_var:.1f}% explained variance)" if pc2_var is not None else "PC2 – secondary profile dimension"

        fig = px.scatter(
            pca_filtered,
            x="PC1",
            y="PC2",
            color="democratic_connection_profile",
            color_discrete_map=COLOR_MAP,
            opacity=0.72,
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
                "PC1": x_label,
                "PC2": y_label,
                "democratic_connection_profile": "Profile"
            }
        )

        centroids = (
            pca_filtered
            .groupby("democratic_connection_profile")[["PC1", "PC2"]]
            .mean()
            .reset_index()
        )

        fig.add_trace(
            go.Scatter(
                x=centroids["PC1"],
                y=centroids["PC2"],
                mode="markers+text",
                marker=dict(
                    size=18,
                    color=[
                        COLOR_MAP.get(profile, "#FFFFFF")
                        for profile in centroids["democratic_connection_profile"]
                    ],
                    line=dict(width=2, color="white"),
                    symbol="diamond"
                ),
                text=centroids["democratic_connection_profile"],
                textposition="top center",
                name="Profile centroid",
                hovertemplate="<b>%{text}</b><br>Centroid<extra></extra>"
            )
        )

        fig = plot_layout(
            fig,
            title="2D PCA Map of Democratic Connection Profiles",
            height=680,
            x_title=x_label,
            y_title=y_label
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
            st.markdown("### Optional 3D PCA view")

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
                    "PC1": "PC1",
                    "PC2": "PC2",
                    "PC3": "PC3",
                    "democratic_connection_profile": "Profile"
                }
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
                    xaxis_title="PC1",
                    yaxis_title="PC2",
                    zaxis_title="PC3",
                    bgcolor="#0E1117"
                ),
                legend=dict(title=None)
            )

            st.plotly_chart(fig_3d, use_container_width=True)

        if not pca_loadings.empty:
            st.markdown("### PCA component loadings")

            loadings_plot = pca_loadings.copy()

            if loadings_plot.columns[0] not in ["indicator", "variable"]:
                loadings_plot = loadings_plot.reset_index().rename(columns={"index": "indicator"})
            elif loadings_plot.columns[0] != "indicator":
                loadings_plot = loadings_plot.rename(columns={loadings_plot.columns[0]: "indicator"})

            loading_cols = [col for col in loadings_plot.columns if "PC" in col]

            if loading_cols:
                selected_pc = st.selectbox(
                    "Select PCA component for loading chart",
                    options=loading_cols,
                    index=0
                )

                fig_load = px.bar(
                    loadings_plot.sort_values(selected_pc),
                    x=selected_pc,
                    y="indicator",
                    orientation="h",
                    text=loadings_plot.sort_values(selected_pc)[selected_pc].round(2),
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
        The strategic translation is evidence-informed, not causal. The profiles suggest that democratic
        actors should distinguish between maintaining connection, rebuilding trust among disappointed
        participants and lowering barriers for disengaged non-voters.
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
# TAB 8: METHOD NOTES
# =============================================================================

with tabs[7]:
    st.subheader("Method Notes and Interpretation Boundaries")

    st.markdown(
        """
        ### Data and scope

        This project uses the European Social Survey Round 11 Germany subset. The analysis focuses on
        selected variables related to democratic satisfaction, institutional trust, political efficacy,
        social trust, subjective income feeling, political orientation and voting behavior.

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
