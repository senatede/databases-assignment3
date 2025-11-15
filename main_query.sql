SELECT
  p.category,
  SUM(f.total_profit) AS total_category_profit
FROM
  `homework3-478220.mart.fact_order_items` AS f
JOIN
  `homework3-478220.dim.dim_product` AS p
  ON f.product_key = p.product_key
JOIN
  `homework3-478220.dim.dim_restaurant` AS r
  ON f.restaurant_key = r.restaurant_key
JOIN
  `homework3-478220.dim.dim_date` AS d
  ON f.date_key = d.date_key
WHERE
  -- Last 3 months of the year (Oct, Nov, Dec)
  d.month_number IN (10, 11, 12)
  -- Kyiv region
  AND r.region = 'Kyiv'
GROUP BY
  p.category
ORDER BY
  total_category_profit DESC;