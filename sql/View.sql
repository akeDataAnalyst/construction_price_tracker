-- 5. Create a small view for quick reporting
CREATE OR REPLACE VIEW v_recent_prices AS
SELECT 
    category,
    material,
    price_etb,
    unit,
    last_checked,
    DATEDIFF(CURDATE(), last_checked) AS days_old
FROM materials_prices
WHERE price_etb_valid = 1
  AND last_checked IS NOT NULL
ORDER BY last_checked DESC, price_etb DESC
LIMIT 100;