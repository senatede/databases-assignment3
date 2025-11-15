CREATE OR REPLACE TABLE stage.stg_menu_items AS
SELECT
  product_id,
  name,
  category,
  unit_cost
FROM
  `raw_data.raw_menu_items`
WHERE
  product_id IS NOT NULL
  AND name IS NOT NULL
  AND category IS NOT NULL
  AND unit_cost IS NOT NULL
QUALIFY ROW_NUMBER() OVER(PARTITION BY product_id ORDER BY name) = 1;