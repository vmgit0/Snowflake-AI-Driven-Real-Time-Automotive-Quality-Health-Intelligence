USE DATABASE EV_PROJECT_DB;
USE SCHEMA CURATED;
CREATE OR REPLACE VIEW EV_PREDICTIVE_MAINTENANCE_AGENT AS
SELECT
    EVENT_TIMESTAMP,
    FAILURE_RISK_LEVEL,
    FAILURE_PROBABILITY,
    RUL,

    SNOWFLAKE.CORTEX.COMPLETE(
        'mixtral-8x7b',
        CONCAT(
            'Predict vehicle maintenance needs. ',
            'Failure risk: ', FAILURE_RISK_LEVEL,
            ', Failure probability: ', FAILURE_PROBABILITY,
            ', Remaining Useful Life: ', RUL,
            '. Recommend preventive action.'
        )
    ) AS MAINTENANCE_RECOMMENDATION

FROM EV_FAILURE_FORECAST_30D
WHERE FAILURE_RISK_LEVEL <> 'LOW_RISK';



