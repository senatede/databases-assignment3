CREATE OR REPLACE TABLE stage.stg_orders AS
SELECT
  ti.order_id,
  t.timestamp AS order_timestamp,
  t.restaurant_id,
  ti.product_id,
  
  ti.quantity,
  ti.price AS total_revenue,
  (ti.quantity * mi.unit_cost) AS total_cost,
  (ti.price - (ti.quantity * mi.unit_cost)) AS total_profit

FROM (
  SELECT *
  FROM `raw_data.raw_transaction_items`
  WHERE order_id IS NOT NULL 
    AND product_id IS NOT NULL
    AND quantity IS NOT NULL
    AND price IS NOT NULL
  QUALIFY ROW_NUMBER() OVER(PARTITION BY order_id, product_id ORDER BY quantity) = 1
) AS ti
JOIN (
  SELECT *
  FROM `raw_data.raw_transactions`
  WHERE order_id IS NOT NULL
    AND timestamp IS NOT NULL
    AND restaurant_id IS NOT NULL
  QUALIFY ROW_NUMBER() OVER(PARTITION BY order_id ORDER BY timestamp) = 1
) AS t
  ON ti.order_id = t.order_id
INNER JOIN
  `stage.stg_menu_items` AS mi
  ON ti.product_id = mi.product_id;