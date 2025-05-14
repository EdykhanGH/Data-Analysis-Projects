WITH monthly_revenue AS (
    SELECT
        merchant_id,
        DATE_TRUNC('month', transaction_date)::date AS month,
        SUM(transaction_amount) AS monthly_revenue
    FROM transaction_analysis
    WHERE status = 'successful'
    GROUP BY merchant_id, DATE_TRUNC('month', transaction_date)::date
),

revenue_volatility AS (
    SELECT 
        merchant_id,
        ROUND(STDDEV(monthly_revenue), 2) AS revenue_stddev,
        ROUND(AVG(monthly_revenue), 2) AS avg_revenue,
        ROUND(
            STDDEV(monthly_revenue) / NULLIF(AVG(monthly_revenue), 0),
        2) AS volatility_index
    FROM monthly_revenue
    GROUP BY merchant_id
),

chargeback_rate AS (
    SELECT 
        merchant_id,
        COUNT(transaction_id) AS total_transactions,
        COUNT(chargeback_id) AS total_chargebacks,
        ROUND(
            COUNT(chargeback_id)::decimal / NULLIF(COUNT(transaction_id), 0), 
        2) AS chargeback_rate
    FROM transaction_analysis
    GROUP BY merchant_id
),

risk_score AS (
    SELECT
        rv.merchant_id,
        ROUND(((rv.volatility_index * 0.5) + (cb.chargeback_rate * 0.5)), 2) AS risk_score
    FROM revenue_volatility rv
    JOIN chargeback_rate cb ON rv.merchant_id = cb.merchant_id
)

SELECT DISTINCT
    merchant_id,
    risk_score,
    DENSE_RANK() OVER(ORDER BY risk_score DESC) AS risk_rank
FROM risk_score
ORDER BY risk_rank;
