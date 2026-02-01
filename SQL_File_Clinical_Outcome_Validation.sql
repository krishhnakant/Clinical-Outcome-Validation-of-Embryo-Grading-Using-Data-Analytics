CREATE DATABASE Clinical_Outcome_Validation; 
USE Clinical_Outcome_Validation;

-- Load Dataset into MYSQL 
SELECT * FROM clinical_outcome_validation_cleaned_dataset; 

-- Basic Data Validation 
# Total Records 
SELECT COUNT(*) AS total_records
FROM clinical_outcome_validation_cleaned_dataset;

# Distinct Embryos 
SELECT COUNT(DISTINCT EmbryoID) AS unique_embryos
FROM clinical_outcome_validation_cleaned_dataset;

# Check missing critical fields 
SELECT
    SUM(CASE WHEN MorphologyGrade IS NULL THEN 1 ELSE 0 END) AS missing_morphology,
    SUM(CASE WHEN ClinicalPregnancy_01 IS NULL THEN 1 ELSE 0 END) AS missing_outcomes
FROM clinical_outcome_validation_cleaned_dataset;

-- Day Wise Seggregation 
# Records by day 
SELECT Day, COUNT(*) AS records
FROM clinical_outcome_validation_cleaned_dataset
GROUP BY Day;

# Pregnancy Rate by Day 
SELECT
    Day,
    ROUND(AVG(ClinicalPregnancy_01) * 100, 2) AS pregnancy_rate_percent
FROM clinical_outcome_validation_cleaned_dataset 
GROUP BY Day;

-- Morphology Grade Validation 
# Pregnancy rate by morphology grade 
SELECT
    MorphologyGrade,
    COUNT(*) AS total_cases,
    ROUND(AVG(ClinicalPregnancy_01) * 100, 2) AS success_rate
FROM clinical_outcome_validation_cleaned_dataset 
GROUP BY MorphologyGrade
ORDER BY success_rate DESC;

# Day wise morphology grade effectiveness 
SELECT
    Day,
    MorphologyGrade,
    ROUND(AVG(ClinicalPregnancy_01) * 100, 2) AS success_rate
FROM clinical_outcome_validation_cleaned_dataset 
GROUP BY Day, MorphologyGrade
ORDER BY Day, success_rate DESC;

-- 	AI grade and Human grade comparison 
# ai grade and morphology grade aggreement 
SELECT
    MorphologyGrade,
    AIGrade,
    COUNT(*) AS cases
FROM clinical_outcome_validation_cleaned_dataset 
GROUP BY MorphologyGrade, AIGrade;

# performance of AI prediction 
SELECT
    AIGrade,
    ROUND(AVG(ClinicalPregnancy_01) * 100, 2) AS success_rate
FROM clinical_outcome_validation_cleaned_dataset 
GROUP BY AIGrade
ORDER BY success_rate DESC;

-- Embryologist consistency analysis 
# Number of grades given by each embryologist 
SELECT
    EmbryologistID,
    COUNT(*) AS graded_cases
FROM clinical_outcome_validation_cleaned_dataset 
GROUP BY EmbryologistID;

# Pregnancy success by embryologist 
SELECT
    EmbryologistID,
    ROUND(AVG(ClinicalPregnancy_01) * 100, 2) AS success_rate
FROM clinical_outcome_validation_cleaned_dataset 
GROUP BY EmbryologistID;

-- Advanced Analytics 
# Rank morphology grades by success rate (GLOBALLY) 
SELECT
    MorphologyGrade,
    ROUND(AVG(ClinicalPregnancy_01) * 100, 2) AS success_rate,
    RANK() OVER (ORDER BY AVG(ClinicalPregnancy_01) DESC) AS grade_rank
FROM clinical_outcome_validation_cleaned_dataset 
GROUP BY MorphologyGrade;

# Rank grades within each Day 
SELECT
    Day,
    MorphologyGrade,
    ROUND(AVG(ClinicalPregnancy_01) * 100, 2) AS success_rate,
    RANK() OVER (
        PARTITION BY Day
        ORDER BY AVG(ClinicalPregnancy_01) DESC
    ) AS day_rank
FROM clinical_outcome_validation_cleaned_dataset 
GROUP BY Day, MorphologyGrade;

-- PATIENT-LEVEL DUPLICATION & DATA QUALITY 
# Same EmbryoID with different ages (data issue) 
SELECT EmbryoID, COUNT(DISTINCT PatientAge) AS age_variations
FROM clinical_outcome_validation_cleaned_dataset 
GROUP BY EmbryoID
HAVING COUNT(DISTINCT PatientAge) > 1;

# Duplicate embryo assessments 
SELECT EmbryoID, COUNT(*) AS assessment_count
FROM clinical_outcome_validation_cleaned_dataset 
GROUP BY EmbryoID
HAVING COUNT(*) > 1;

-- TEMPORAL ANALYSIS (REAL OPERATIONS) 
# Monthly pregnancy trend 
SELECT
    AssessmentDate AS month,
    ROUND(AVG(ClinicalPregnancy_01) * 100, 2) AS pregnancy_rate
FROM clinical_outcome_validation_cleaned_dataset
GROUP BY month
ORDER BY month;

# Grading drift over time 
SELECT
    AssessmentDate AS month,
    MorphologyGrade,
    COUNT(*) AS cases
FROM clinical_outcome_validation_cleaned_dataset
GROUP BY month, MorphologyGrade
ORDER BY month;

-- EXECUTIVE-LEVEL SUMMARY QUERY 
SELECT
    Day,
    MorphologyGrade,
    COUNT(*) AS total_cases,
    ROUND(AVG(ClinicalPregnancy_01) * 100, 2) AS pregnancy_rate
FROM clinical_outcome_validation_cleaned_dataset 
GROUP BY Day, MorphologyGrade
ORDER BY Day, pregnancy_rate DESC;


-- CORRELATION-READY METRICS (FOR DATA SCIENCE) [OPTIONAL] 
# Encoded morphology score (for modeling) 
SELECT
    *,
    CASE MorphologyGrade
        WHEN 'A' THEN 4
        WHEN 'B' THEN 3
        WHEN 'C' THEN 2
        ELSE 1
    END AS MorphologyScore
FROM clinical_outcome_validation_cleaned_dataset;

# Outcome vs morphology score 
SELECT
    MorphologyScore,
    ROUND(AVG(ClinicalPregnancy_01) * 100, 2) AS success_rate
FROM (
    SELECT
        ClinicalPregnancy_01,
        CASE MorphologyGrade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            ELSE 1
        END AS MorphologyScore
    FROM clinical_outcome_validation_cleaned_dataset 
) t
GROUP BY MorphologyScore
ORDER BY MorphologyScore DESC;

-- Completed 