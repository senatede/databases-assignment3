CREATE OR REPLACE TABLE stage.stg_restaurants AS
SELECT
  restaurant_id,
  address,
  city,
  region
FROM `raw_data.raw_restaurants`
WHERE restaurant_id IS NOT NULL
  AND address IS NOT NULL
  AND city IS NOT NULL
  AND region IS NOT NULL
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY restaurant_id
) = 1;