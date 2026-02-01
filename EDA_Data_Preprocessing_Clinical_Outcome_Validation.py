# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 22:35:11 2026

@author: krish
"""

import pandas as pd 
import numpy as np 

import matplotlib.pyplot as plt 


data = pd.read_csv(r"C:\Users\krish\.spyder-py3\1st_Project_(Clinical Outcome Validation of Embryo Grading Using Data Analytics)\Updated_Correct_Dataset\Clinical outcome validation Dataset.csv") 

print(data.head()) 
print(data.shape)
print(data.columns) 
print(data.describe()) 
print(data.info()) 

print(data.isnull().sum()) 
print(data.duplicated().sum())
 
number_cols = ['PatientAge', 'Fragmentation', 'BlastocystExpansion']
for col in number_cols: 
    data[col] = data[col].fillna(data[col].median()) 

# data['PatientAge'] = data['PatientAge'].fillna(data['PatientAge'].median()) # Doubt: PatientAge 

data.drop_duplicates(inplace = True) 

data['EmbryologistID'] = data['EmbryologistID'].str.upper() 
print(data['EmbryologistID'])

# =============================================================================
# import pandas as pd
# import re
# 
# 
# # Function to convert alphanumeric IVF grades
# def convert_morphology_grade(grade):
#     if pd.isna(grade):
#         return grade
# 
#     grade = str(grade).strip()
# 
#     # If already qualitative, return as is
#     qualitative = ["Excellent", "Good", "Fair", "Poor"]
#     if grade in qualitative:
#         return grade
# 
#     # Match patterns like 1AA, 2AB, 3BB, etc.
#     match = re.match(r"\d*([A-C])([A-C])", grade)
#     if not match:
#         return grade  # return original if unexpected format
# 
#     icm, te = match.groups()
# 
#     # Pure morphological ranking
#     if icm == "A" and te == "A":
#         return "A"
#     elif "A" in [icm, te] and "B" in [icm, te]:
#         return "B"
#     elif icm == "B" and te == "B":
#         return "B"
#     elif "C" in [icm, te]:
#         return "C"
#     else:
#         return "D"
# 
# # Apply conversion
# data["MorphologyGrade"] = data["MorphologyGrade"].apply(convert_morphology_grade)
# data['MorphologyGrade'].value_counts()
# 
# =============================================================================

import seaborn as sns 
import re
import pandas as pd


# Function to convert alphanumeric IVF grades using PURE IVF morphology
def convert_morphology_grade(grade):
    if pd.isna(grade):
        return grade

    grade = str(grade).strip()

    # Do NOT change qualitative grades (Day 3 morphology)
    qualitative = ["Excellent", "Good", "Fair", "Poor"]
    if grade in qualitative:
        return grade

    # Match pure IVF blastocyst grades like 1AA, 2AB, 3BB, 4BC, etc.
    match = re.match(r"(\d)([A-C])([A-C])", grade)
    if not match:
        return grade  # keep original if format is unexpected

    expansion, icm, te = match.groups()
    expansion = int(expansion)

    # PURE IVF MORPHOLOGICAL GRADING LOGIC
    if expansion >= 4 and icm == "A" and te == "A":
        return "A"

    elif expansion >= 3 and icm in ["A", "B"] and te in ["A", "B"]:
        return "B"

    elif expansion >= 3 and ("C" in [icm, te]):
        return "C"

    else:
        return "D"

# Apply conversion
data["MorphologyGrade"] = data["MorphologyGrade"].apply(convert_morphology_grade)

data["MorphologyGrade"].value_counts()


# Create Day Group label
import pandas as pd

# Step 1: Normalize Day values
data["Day"] = data["Day"].replace({
    3: "Day 3",
    5: "Day 5",
    "3": "Day 3",
    "5": "Day 5"
})

# Step 2: Apply ordered categorical sorting
data["Day"] = pd.Categorical(
    data["Day"],
    categories=["Day 5", "Day 3"],
    ordered=True
)

# Step 3: Sort
data = data.sort_values(by="Day")

day_count = data['Day'].value_counts()

print(day_count)


# Outlier Analysis 
excluded_cols = [
    'EmbryoID', 'Day', 'EmbryologistID',
    'MorphologyGrade', 'AIGrade',
    'SelectedforTransfer_01',
    'ClinicalPregnancy_01',
    'AssessmentDate'
]

outlier_cols = [col for col in number_cols if col not in excluded_cols]
outlier_cols

import seaborn as sns 

for col in outlier_cols:
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    data = data[(data[col] >= lower) & (data[col] <= upper)]


for col in outlier_cols:
    plt.figure(figsize=(6,4))
    sns.boxplot(x=data[col])
    plt.title(f"Boxplot of {col}")
    plt.show()


for col in outlier_cols:
    plt.figure(figsize=(6,4))
    sns.histplot(data[col], kde=True)
    plt.title(f"Distribution of {col}")
    plt.show()


corr_cols = outlier_cols + ['SelectedforTransfer_01', 'ClinicalPregnancy_01']

plt.figure(figsize=(8,6))
sns.heatmap(data[corr_cols].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()


data["AssessmentDate"] = pd.to_datetime(
    data["AssessmentDate"],
    errors="coerce"
).dt.date

print(data["AssessmentDate"].dtype)
print(data["AssessmentDate"].head())




# Mapping dictionary
binary_map = {0: 'No', 1: 'Yes'}

# Create new categorical columns
data['SelectedforTransfer'] = data['SelectedforTransfer_01'].map(binary_map)
data['ClinicalPregnancyOutcome'] = data['ClinicalPregnancy_01'].map(binary_map)

data['SelectedforTransfer'].value_counts()
data['ClinicalPregnancyOutcome'].value_counts()


# Cleaned Dataset Checking 
print(data.shape) 
print(data.info()) 
print(data.describe) 
print(data.head())
print(data.isnull().sum()) 
print(data.duplicated().sum())


# Save the cleaned data 
data.to_excel(r"C:\Users\krish\.spyder-py3\1st_Project_(Clinical Outcome Validation of Embryo Grading Using Data Analytics)\Cleaned_Dataset_Folder\Clinical_Outcome_Validation_Cleaned_Dataset.xlsx", index=False)

datacleaned = pd.read_excel(r"C:\Users\krish\.spyder-py3\1st_Project_(Clinical Outcome Validation of Embryo Grading Using Data Analytics)\Cleaned_Dataset_Folder\Clinical_Outcome_Validation_Cleaned_Dataset.xlsx") 
print(datacleaned)


# COMPLETED PREPROCESSING
