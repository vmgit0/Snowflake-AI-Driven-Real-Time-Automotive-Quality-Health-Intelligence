USE DATABASE EV_PROJECT_DB;
USE SCHEMA CURATED;
CREATE OR REPLACE VIEW EV_ROOT_CAUSE_AGENT AS
SELECT
    EVENT_TIMESTAMP,
    ANOMALY_TYPE,

    SNOWFLAKE.CORTEX.COMPLETE(
        'mixtral-8x7b',
        CONCAT(
            'Perform root cause analysis for EV anomaly. ',
            'Anomaly type: ', ANOMALY_TYPE,
            '. Battery health index: ', BATTERY_HEALTH_INDEX,
            ', Motor stress index: ', MOTOR_STRESS_INDEX,
            ', Usage stress score: ', USAGE_STRESS_SCORE,
            '. Suggest probable root cause.'
        )
    ) AS ROOT_CAUSE_ANALYSIS

FROM EV_ANOMALIES
WHERE IS_ANOMALY = 1;

