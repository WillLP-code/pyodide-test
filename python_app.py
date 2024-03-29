"""
Plots to do:
Normalised ethnicity breakdown vs national results
Plot national age/gender breakdown on age plot
"""

import pandas as pd
import js
from js import files
import pyodide_js
import json
import io
import plotly.express as px
import numpy as np

dfs = {}
for i, v in enumerate(files):
    dfs[i] = pd.read_csv(io.StringIO(files[i]))

# df = px.data.iris()
# fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

# fig = fig.to_html(include_plotlyjs=False, full_html=False, default_height="350px")

# js.document.fig = fig

module_columns = {
    "m1": [
        "Person ID",
        "Surname",
        "Forename",
        "Dob (ccyy-mm-dd)",
        "Gender",
        "Ethnicity",
        "Postcode",
        "UPN - Unique Pupil Number",
        "ULN - Young Persons Unique Learner Number",
        "UPN and ULN unavailable reason",
    ],
    "m2": [
        "Person ID",
        "Requests Record ID",
        "Date Request Was Received",
        "Initial Request Whilst In RYA",
        "Request Outcome Date",
        "Request Outcome",
        "Request Mediation",
        "Request Tribunal",
        "Exported - Child Or Young Person Moves Out Of LA Before Assessment Is Completed",
        "New start date",
    ],
    "m3": [
        "Person ID",
        "Requests Record ID",
        "Assessment Outcome To Issue EHCP",
        "Assessment Outcome Date",
        "Assessment Mediation",
        "Assessment Tribunal",
        "Other Mediation",
        "Other Tribunal",
        "Twenty Weeks Time Limit Exceptions Apply",
    ],
    "m4": [
        "Person ID",
        "Request Records ID",
        "EHC Plan Start Date",
        "Residential Settings",
        "Worked based learning activity",
        "Personal budget taken up",
        "Personal budget - organised arrangements",
        "Personal budget - direct payments",
        "Date EHC Plan Ceased",
        "Reason EHC Plan Ceased",
    ],
    "m5": [
        "Person ID",
        "Request Records ID",
        "EHC Plan (Transfer)",
        "Residential Settings",
        "Worked based learning activity",
        "EHCP review decisions date",
    ],
}

modules = {}

for key, df in dfs.items():
    for module_name, column_list in module_columns.items():
        if list(df.columns) == column_list:
            modules[module_name] = df


if len(modules.keys()) != 5:
    js.alert(f"Modules found {modules.keys()}, please check column names.")

modules["m1"]["Dob (ccyy-mm-dd)"] = pd.to_datetime(
    modules["m1"]["Dob (ccyy-mm-dd)"], format="%d/%m/%Y", errors="coerce"
)
modules["m1"]["Age"] = (
    pd.to_datetime("today") - modules["m1"]["Dob (ccyy-mm-dd)"]
) / np.timedelta64(1, "Y")
modules["m1"]["Age"] = modules["m1"]["Age"].round().astype("int", errors="ignore")

# print(modules["m1"]["Age"])

gender_plot = px.histogram(
    (modules["m1"][modules["m1"]["Gender"] != 9]),
    x="Age",
    category_orders=dict(Age=list(modules["m1"]["Age"].unique())),
    color="Gender",
)
gender_plot = gender_plot.to_html(
    include_plotlyjs=False, full_html=False, default_height="350px"
)
js.document.gender_plot = gender_plot

ethnicity_plot = px.histogram(
    (modules["m1"]),
    x="Ethnicity",
    category_orders=dict(Age=list(modules["m1"]["Ethnicity"].unique())),
)
ethnicity_plot = ethnicity_plot.to_html(
    include_plotlyjs=False, full_html=False, default_height="350px"
)
js.document.ethnicity_plot = ethnicity_plot


ass_outcomes = modules["m3"][modules["m3"]["Assessment Outcome To Issue EHCP"] != "H"]
ass_outcomes = (
    ass_outcomes.groupby(["Assessment Outcome To Issue EHCP"])[
        "Assessment Outcome To Issue EHCP"
    ]
    .count()
    .reset_index(name="count")
)

assessment_outcome_plot = px.pie(
    ass_outcomes, values="count", names="Assessment Outcome To Issue EHCP"
)
assessment_outcome_plot = assessment_outcome_plot.to_html(
    include_plotlyjs=False, full_html=False, default_height="350px"
)
js.document.assessment_outcome_plot = assessment_outcome_plot

# Request to outcome timeliness
requests = modules["m2"][modules["m2"].notna()]

requests["Request Timeliness"] = pd.to_datetime(
    requests["Request Outcome Date"], format="%d/%m/%Y"
) - pd.to_datetime(requests["Date Request Was Received"], format="%d/%m/%Y")

requests["Request Timeliness"] = (
    (requests["Request Timeliness"] / np.timedelta64(1, "D"))
    .round()
    .astype("int", errors="ignore")
)

request_timeliness_plot = px.histogram(requests, x="Request Timeliness")
js.document.request_timeliness_plot = request_timeliness_plot.to_html(
    include_plotlyjs=False, full_html=False, default_height="350px"
)
