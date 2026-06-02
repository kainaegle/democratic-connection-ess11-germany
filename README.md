- Here, we should provide all info to make sure other ppl are able to recreate the process/product based on information 
- Also check ppt on capstone with different steps
- Also check best practices
- Clean and spiced-up github repo


# What Builds Democratic Connection?

A data-driven capstone project analyzing party trust, political efficacy and social confidence in Germany using European Social Survey Round 11 data.

## 1. Project Summary

This project investigates where democratic connection weakens in Germany.

Instead of focusing only on general satisfaction with democracy, the analysis looks at:

- trust in political parties
- trust in politicians
- trust in parliament
- political efficacy
- social trust
- voting behavior
- subjective economic security
- political self-placement

The goal is to identify early patterns that may help democratic actors better understand different forms of democratic disconnection and develop more evidence-based political, civic and communication strategies.

## 2. Problem Statement

Democratic parties and institutions face increasing pressure from declining trust, political disengagement and the rise of anti-system narratives. However, low trust does not necessarily mean that people reject democracy itself.

The core problem addressed in this project is the gap between democratic satisfaction, trust in political actors and citizens’ perceived ability to influence politics.

The project therefore asks:

**Where does democratic connection weaken, and which social, political and participatory factors are associated with lower trust in democratic institutions and political parties?**

## 3. Core Advisory Logic

This project does not simply assume that parties need better communication.

The guiding logic is:

**Different trust problems may require different democratic responses.**

For example:

- Low party trust may require more transparency, credibility and accountability.
- Low political efficacy may require more visible participation and responsiveness.
- Low social trust may require broader social confidence-building.
- Low participation may require democratic re-engagement before election campaigns.
- Economic insecurity may require policy responses that connect material security with democratic trust.

## 4. Stakeholders

The project is relevant for:

- democratic political parties
- political foundations
- think tanks
- civic education organizations
- public institutions working on democratic resilience
- campaign, participation and strategy teams
- policy advisors
- political communication professionals

The primary target users are actors who need evidence-based insights into democratic trust, political participation and voter-oriented strategy.

## 5. Data Source

The main data source is the **European Social Survey Round 11 integrated dataset**.

Source: https://www.europeansocialsurvey.org/

The analysis currently focuses on the Germany subset.

Current dataset status:

- Full ESS11 dataset: 50,116 respondents
- Full ESS11 variables: 691 variables
- Germany subset: 2,420 respondents
- Extended clean analysis dataset: 2,004 respondents
- Raw format: SPSS `.sav`
- Main tools: Python, pandas, pyreadstat, matplotlib
- Planned tools: Tableau and/or Streamlit for dashboarding

Raw ESS data is not included in this repository. It can be downloaded from the official ESS Data Portal.

## 6. Key Variables

### 6.1 Main Outcome Variables

- `stfdem`: Satisfaction with the way democracy works
- `trstprl`: Trust in parliament
- `trstplt`: Trust in politicians
- `trstprt`: Trust in political parties

### 6.2 Main Explanatory and Segmentation Variables

- `vote`: Voting behavior in the last national election
- `hincfel`: Feeling about household income
- `lrscale`: Left-right political self-placement
- `eduyrs`: Years of education
- `agea`: Age
- `gndr`: Gender
- `ppltrst`: Most people can be trusted
- `pplfair`: Most people try to be fair
- `pplhlp`: Most people try to be helpful
- `psppsgva`: Political system allows people to have a say
- `psppipla`: Political system allows people to influence politics
- `cptppola`: Confidence in own ability to participate in politics
- `actrolga`: Ability to take active role in political group

## 7. Research Questions

1. Is trust in political parties and politicians lower than trust in other institutions?
2. Do non-voters show lower democratic satisfaction and lower institutional trust than voters?
3. Is perceived political efficacy associated with democratic satisfaction and institutional trust?
4. Is social trust associated with democratic satisfaction and institutional trust?
5. How are economic security, education, age and political orientation related to democratic trust patterns?
6. Can these patterns be translated into useful democratic trust profiles for strategic analysis?

## 8. Working Hypotheses

### H1: Party-Trust Gap

Trust in political parties and politicians is lower than trust in other institutions and lower than general satisfaction with democracy.

### H2: Participation Gap

Respondents who did not vote in the last national election show lower democratic satisfaction and lower institutional trust than respondents who voted.

### H3: Political Efficacy Gap

Respondents with lower perceived political efficacy show lower democratic satisfaction and lower trust in parliament, politicians and political parties.

### H4: Social Trust Gap

Respondents with lower social trust show lower democratic satisfaction and lower institutional trust.

### H5: Economic Security Gap

Respondents who feel economically strained show lower institutional trust than respondents who feel economically secure.

### H6: Political Orientation Gap

Democratic satisfaction and institutional trust differ across left-right self-placement groups.

This will be interpreted carefully and without stigmatizing political groups.

## 9. KPIs and Analytical Metrics

This project uses analytical KPIs rather than business KPIs. The KPIs are designed to measure where democratic connection appears stronger or weaker in the ESS11 Germany data.

| KPI | SMART Formulation | ESS Variables | Purpose |
|---|---|---|---|
| Party-Trust Gap | Measure the mean difference between trust in political parties/politicians and trust in other institutions in the ESS11 Germany sample. | `trstprt`, `trstplt`, `trstprl`, `trstlgl`, `trstplc` | Identify whether trust is especially weak toward political actors. |
| Participation Gap | Compare mean democratic satisfaction and institutional trust between voters and non-voters in the cleaned Germany dataset. | `vote_clean`, `stfdem`, `trstprl`, `trstplt`, `trstprt` | Assess whether non-voting is associated with weaker democratic connection. |
| Political Efficacy Gap | Compare mean democratic satisfaction and institutional trust across low, medium and high political efficacy groups. | `political_efficacy_index`, `efficacy_group`, `stfdem`, `trstprl`, `trstplt`, `trstprt` | Assess whether perceived political influence is associated with democratic trust. |
| Social Trust Gap | Compare mean democratic satisfaction and institutional trust across low, medium and high social trust groups. | `social_trust_index`, `social_trust_group`, `stfdem`, `trstprl`, `trstplt`, `trstprt` | Explore whether democratic trust is linked to broader social confidence. |
| Economic Security Gap | Compare mean democratic satisfaction and institutional trust across household income-feeling groups. | `hincfel`, `stfdem`, `trstprl`, `trstplt`, `trstprt` | Assess whether subjective economic strain is associated with lower democratic trust. |
| Political Orientation Pattern | Compare democratic satisfaction and institutional trust across grouped left-right self-placement categories. | `lr_group`, `lrscale`, `stfdem`, `trstprl`, `trstplt`, `trstprt` | Explore whether trust patterns differ across political self-placement groups. |
| Statistical Validation | Validate the strongest EDA patterns using appropriate statistical tests and effect sizes before final interpretation. | selected cleaned variables | Ensure that conclusions are not based only on visual inspection. |
| Dashboard Readiness | Produce at least one dashboard-ready clean dataset and a set of clear visual outputs for final presentation. | `df_extended`, exported CSV, PNG visualizations | Support communication of findings to political and civic stakeholders. |

## 10. Data Pipeline Draft

The project follows a structured data analytics pipeline..

### 10.1 Collect

Download the official ESS11 integrated dataset.

### 10.2 Store

Store raw data locally in `data/raw/`.

Raw ESS data is excluded from GitHub.

### 10.3 Load

Load the SPSS `.sav` file into Python using `pyreadstat`.

### 10.4 Inspect

Check:

- dataset size
- variable labels
- value labels
- missing values
- data types
- country coverage

### 10.5 Clean

Clean and prepare the data by:

- filtering the dataset for Germany
- selecting relevant variables
- checking missing values
- recoding voting behavior
- exporting clean working datasets

### 10.6 Transform

Create derived variables and indices:

- clean voting behavior variable
- social trust index
- social trust groups
- political efficacy index
- political efficacy groups
- grouped left-right political orientation
- extended clean analysis dataset

### 10.7 Analyze

Conduct:

- exploratory data analysis
- descriptive statistics
- correlation analysis
- group comparisons
- first analytical interpretation

### 10.8 Visualize

Create early visualizations for core trust gaps:

- institutional trust ranking
- political efficacy gap
- social trust gap
- participation gap

### 10.9 Validate

Planned next step:

- statistical group comparison tests
- effect sizes
- regression models
- robustness checks

### 10.10 Communicate

Translate findings into:

- dashboard
- final presentation
- evidence-based strategic interpretation
- cautious policy and strategy recommendations

## 11. Current Status

Completed:

- loaded and inspected ESS11 integrated data
- filtered Germany subset
- created a variable overview and descriptive statistics snapshot
- exported dataset snapshot to Excel
- selected first core variables
- checked missing values and valid sample sizes
- cleaned voting behavior variable
- created social trust index
- created political efficacy index
- created grouped political orientation variable
- built extended clean analysis dataset
- created first early visualizations
- set up GitHub repository structure

## 12. Early EDA Findings

The first exploratory analysis suggests several relevant patterns.

### 12.1 Party-Trust Gap

Trust in political parties and politicians is lower than trust in parliament, the legal system and the police.

This suggests that the project should not only focus on general democratic satisfaction, but especially on trust in political actors and representative institutions.

### 12.2 Participation Gap

Non-voters show lower democratic satisfaction and lower trust in parliament, politicians and political parties than voters.

This suggests that non-voting may be linked to weaker democratic connection.

### 12.3 Political Efficacy Gap

Respondents with higher perceived political efficacy show higher democratic satisfaction and higher institutional trust.

This suggests that perceived political influence may be an important factor in democratic trust-building.

### 12.4 Social Trust Gap

Respondents with higher social trust also report higher democratic satisfaction and higher institutional trust.

This suggests that democratic confidence may be connected not only to institutions, but also to broader social confidence.

### 12.5 Methodological Caution

These findings are exploratory and show associations, not causality.

The next analytical step is statistical validation.

## 13. Early Visualizations

The current notebook includes early visualizations on:

- institutional trust ranking
- political efficacy gap
- social trust gap
- participation gap

Visual outputs are stored in the `visualizations/` folder.

## 14. Repository Structure

```text
capstone-democratic-connection-ess11/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   ├── clean/
│   └── processed/
│
├── notebooks/
│   └── 01_ess11_germany_eda.ipynb
│
├── visualizations/
│
├── reports/
│
├── docs/
│
└── presentation/
```

## 16. Planned Next Steps

The next project phase will move from exploratory data analysis to statistical validation, dashboard development and strategic interpretation.

### 16.1 Statistical Validation

The first EDA results show promising patterns, but they still need to be tested more systematically.

Planned methods:

- group comparison tests
- confidence intervals
- effect sizes
- correlation analysis
- regression models

The goal is to assess whether the observed trust gaps are robust enough to support careful interpretation.

### 16.2 Group Comparison Tests

Planned group comparisons:

- voters vs. non-voters
- low, medium and high political efficacy groups
- low, medium and high social trust groups
- income-feeling groups
- left, center and right self-placement groups

Possible tests:

- Welch’s t-test for two-group comparisons
- ANOVA or Kruskal-Wallis tests for three or more groups
- post-hoc comparisons if group differences are meaningful

### 16.3 Effect Sizes

Statistical significance alone is not enough.

The project will also calculate effect sizes to understand how large and practically relevant the observed differences are.

Possible effect size indicators:

- Cohen’s d for two-group comparisons
- eta-squared or epsilon-squared for multi-group comparisons
- standardized regression coefficients for regression models

### 16.4 Regression Models

Regression models will be used to assess whether key associations remain visible when controlling for other variables.

Possible outcome variables:

- `stfdem`: satisfaction with democracy
- `trstprt`: trust in political parties
- `trstplt`: trust in politicians
- `trstprl`: trust in parliament

Possible explanatory variables:

- political efficacy index
- social trust index
- voting behavior
- household income feeling
- left-right self-placement
- education
- age
- gender

### 16.5 Weighted Robustness Checks

ESS includes survey weights.

The project should test whether core descriptive findings remain similar when applying relevant ESS weights.

This is especially important if results are interpreted as representative patterns for Germany.

### 16.6 Optional Country Comparison

If time allows, the project may compare Germany with selected European countries.

Possible comparison countries:

- France
- Italy
- Spain
- Poland
- Sweden
- Netherlands

This extension should only be included if the Germany analysis is already stable and well explained.

### 16.7 Optional Clustering

A simple clustering approach may be explored to identify democratic trust profiles.

Possible input variables:

- democratic satisfaction
- trust in parties
- trust in politicians
- political efficacy index
- social trust index
- voting behavior
- income feeling

This is optional and should only be used if it produces interpretable and methodologically defensible profiles.

### 16.8 Dashboard Development

The final project output should include a dashboard prototype.

Possible tools:

- Tableau
- Streamlit

The dashboard should show:

- institutional trust ranking
- participation gap
- political efficacy gap
- social trust gap
- income/security patterns
- optional country comparison
- optional trust profiles

### 16.9 Strategic Interpretation

The strongest validated findings will be translated into cautious strategic implications for democratic actors.

The project will avoid causal overclaims.

The final interpretation should focus on:

- where democratic connection appears weaker
- which groups show lower trust or lower efficacy
- which trust gaps may require different democratic responses
- how democratic parties and civic actors can prioritize engagement strategies more evidence-based

## 17. Limitations

This project is exploratory and should be interpreted carefully.

### 17.1 No Causal Claims

The analysis is based on observational survey data.

This means that the project can identify associations, but it cannot prove causal effects.

For example, the analysis may show that low political efficacy is associated with lower trust, but it cannot prove that low efficacy causes lower trust.

### 17.2 Self-Reported Survey Data

ESS data is based on self-reported answers.

Respondents may answer differently due to memory, social desirability, interpretation of questions or current political mood.

### 17.3 Ordinal Variables

Many ESS variables use ordinal scales.

Examples include:

- trust scales from 0 to 10
- political efficacy scales from 1 to 5
- household income feeling from 1 to 4

Means and correlations are useful for exploration, but some variables require careful interpretation and may need non-parametric tests.

### 17.4 Exploratory Indices

The social trust index and political efficacy index are simple constructed indicators.

They are useful for exploratory analysis, but they should be interpreted as analytical approximations rather than perfect measures.

Further validation may be needed.

### 17.5 No Full Causal Model of Voting Behavior

The project does not claim to explain voting behavior or party choice fully.

Voting behavior is used mainly as an indicator of political participation, not as a complete electoral model.

### 17.6 Political Sensitivity

Political trust, party trust and political orientation are sensitive topics.

The analysis will avoid stigmatizing groups and will use careful, non-sensationalist wording.

### 17.7 Limited Scope

The first project phase focuses on Germany and ESS11.

Additional countries, earlier ESS rounds, party manifestos or programme comparisons may add value, but they can also increase complexity.

These extensions will only be included if time allows and if they strengthen the main analytical storyline.

### 17.8 Recommendations Depend on Validation

Final recommendations will only be based on patterns that remain meaningful after further analysis.

The project will avoid statements such as:

- “X causes distrust.”
- “Group Y rejects democracy.”
- “Parties simply need better communication.”

Instead, the project will use cautious wording such as:

- “X is associated with lower trust.”
- “This pattern suggests a possible engagement challenge.”
- “Different trust gaps may require different democratic responses.”