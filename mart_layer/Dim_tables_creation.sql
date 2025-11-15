-- CREATE SCHEMA `homework3-478220`.dim;
CREATE OR REPLACE TABLE dim.dim_product AS
SELECT
    ROW_NUMBER() OVER (ORDER BY product_id) AS product_key,
    product_id,
    name AS product_name,
    category,
    unit_cost
FROM `homework3-478220.stage.stg_menu_items`;


CREATE OR REPLACE TABLE dim.dim_restaurant AS
SELECT
    ROW_NUMBER() OVER (ORDER BY restaurant_id) AS restaurant_key,
    restaurant_id,
    address,
    city,
    region
FROM `homework3-478220.stage.stg_restaurants`;


CREATE OR REPLACE TABLE dim.dim_date AS
SELECT
    CAST(FORMAT_DATE('%Y%m%d', order_date) AS INT64) AS date_key,
    order_date AS full_date,
    EXTRACT(YEAR FROM order_date) AS year,
    EXTRACT(MONTH FROM order_date) AS month_number,
    FORMAT_DATE('%B', order_date) AS month_name,
    EXTRACT(DAY FROM order_date) AS day_of_month,
    FORMAT_DATE('%A', order_date) AS day_of_week,
    CASE WHEN EXTRACT(DAYOFWEEK FROM order_date) IN (1,7) THEN TRUE ELSE FALSE END AS is_weekend,
    FALSE AS is_holiday
FROM (
    SELECT DISTINCT DATE(order_timestamp) AS order_date
    FROM `homework3-478220.stage.stg_orders`
)
ORDER BY full_date;
