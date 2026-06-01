# What I Already Did in the EDA

## 1. Loaded and inspected the ESS11 dataset

- Imported the official European Social Survey Round 11 integrated file into Python.
- Used `pyreadstat` to load the SPSS `.sav` file while keeping metadata such as variable labels.
- Checked the full dataset size:
  - 50,116 respondents
  - 691 variables

## 2. Filtered the dataset for Germany

- Created a Germany-only subset using `cntry == "DE"`.
- Confirmed the German sample size:
  - 2,420 respondents
  - 691 variables

## 3. Created a dataset snapshot

- Built an overview table of all German variables including:
  - column names
  - data types
  - variable labels
  - missing values
  - missing percentages
  - number of unique values
- Exported this snapshot to Excel for variable selection and documentation.

## 4. Selected first core variables

I selected a first set of variables relevant for the project:

- `stfdem` – satisfaction with democracy
- `trstprl` – trust in parliament
- `trstplt` – trust in politicians
- `trstprt` – trust in political parties
- `hincfel` – feeling about household income
- `lrscale` – left-right political placement
- `eduyrs` – years of education
- `agea` – age
- `gndr` – gender

## 5. Checked missing values and sample quality

- Checked missing values for the first core variables.
- Found that missing values are low for most key variables:
  - trust in parliament: around 0.7% missing
  - trust in politicians: around 0.8% missing
  - trust in political parties: around 1.2% missing
  - satisfaction with democracy: around 0.9% missing
- Confirmed that the core dataset remains large enough:
  - 2,267 complete cases before adding voting behavior

## 6. Inspected outcome variables

- Generated descriptive statistics for:
  - satisfaction with democracy
  - trust in parliament
  - trust in politicians
  - trust in political parties
- Checked means, medians, standard deviations and value ranges.

## 7. Ran first correlation checks

- Checked correlations between the main trust and democracy variables.
- Found that institutional trust variables are strongly related to each other.
- Democratic satisfaction is also clearly associated with institutional trust.

## 8. Explored first explanatory relationships

I checked first associations between trust/democratic satisfaction and:

- household income feeling
- left-right placement
- education years
- age

Early signals:

- worse income feeling is associated with lower trust
- higher education shows a moderate positive relationship with trust
- political orientation appears relevant
- age alone does not seem to be the strongest explanatory factor

## 9. Created simple age groups

- Grouped respondents into:
  - 18–29
  - 30–44
  - 45–59
  - 60+
- Compared democratic satisfaction across age groups.
- Early finding: younger people are not automatically less satisfied with democracy.

## 10. Explored income feeling and trust

- Compared trust in parliament across income-feeling categories.
- Early pattern:
  - people who feel more financially comfortable show higher trust in parliament
  - people under stronger financial pressure show lower trust

## 11. Explored left-right placement and democratic satisfaction

- Compared democratic satisfaction across the left-right scale.
- Early pattern:
  - democratic satisfaction appears lower toward the far-right end of the scale
- Methodological caution:
  - extreme categories have smaller sample sizes, so grouping will be needed later

## 12. Added voting behavior

- Found and inspected the `vote` variable.
- Checked value labels:
  - voted
  - did not vote
  - not eligible to vote
- Cleaned the variable into:
  - `Voted`
  - `Did not vote`
- Excluded `not eligible to vote` for voting-behavior analysis.

## 13. Created updated cleaned core dataset

- Added cleaned voting behavior to the core dataset.
- New cleaned core sample:
  - around 2,059 respondents

## 14. Compared voters and non-voters

First strong result:

- non-voters report lower democratic satisfaction than voters
- non-voters also report lower trust in:
  - parliament
  - politicians
  - political parties

Example early differences:

- democratic satisfaction:
  - non-voters: 4.42
  - voters: 5.76
- trust in parliament:
  - non-voters: 3.63
  - voters: 5.17
- trust in politicians:
  - non-voters: 2.84
  - voters: 4.11
- trust in political parties:
  - non-voters: 2.91
  - voters: 4.05

## 15. First conclusion from EDA

The data is feasible and promising.

The initial EDA suggests that democratic trust is not randomly distributed. There are early signs of:

- a Participation Gap
- an Economic Security Gap
- a possible Political Orientation Gap
- and a need to further test a Political Efficacy Gap