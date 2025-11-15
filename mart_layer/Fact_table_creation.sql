CREATE OR REPLACE TABLE mart.fact_order_items AS
SELECT
  FARM_FINGERPRINT(CONCAT(s.order_id, s.product_id)) AS order_item_key,
  
  dp.product_key,
  dr.restaurant_key,
  dd.date_key,
  
  s.order_id,
  
  s.quantity AS quantity_sold,
  s.total_revenue,
  s.total_cost,
  s.total_profit
FROM
  homework3-478220.stage.stg_orders AS s
JOIN
  homework3-478220.dim.dim_product AS dp
  ON s.product_id = dp.product_id
JOIN
  homework3-478220.dim.dim_restaurant AS dr
  ON s.restaurant_id = dr.restaurant_id
JOIN
  homework3-478220.dim.dim_date AS dd
  ON DATE(s.order_timestamp) = dd.full_date;