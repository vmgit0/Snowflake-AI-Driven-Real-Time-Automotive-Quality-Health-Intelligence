USE DATABASE EV_PROJECT_DB;
USE SCHEMA CURATED;

CREATE OR REPLACE VIEW EV_QUALITY_MONITORING_AGENT AS
SELECT
    EVENT_TIMESTAMP,
    ANOMALY_TYPE,
    BATTERY_HEALTH_INDEX,
    MOTOR_STRESS_INDEX,
    USAGE_STRESS_SCORE,

    SNOWFLAKE.CORTEX.COMPLETE(
        'mixtral-8x7b',
        CONCAT(
            'Analyze vehicle quality issue. ',
            'Battery Health Index: ', BATTERY_HEALTH_INDEX,
            ', Motor Stress Index: ', MOTOR_STRESS_INDEX,
            ', Usage Stress Score: ', USAGE_STRESS_SCORE,
            '. Identify potential quality risk.'
        )
    ) AS AI_QUALITY_INSIGHT

FROM EV_ANOMALIES
WHERE IS_ANOMALY = 1;


