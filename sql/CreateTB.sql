-- 3. Create the materials_prices table
CREATE TABLE IF NOT EXISTS materials_prices (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    category          VARCHAR(100)                NULL,
    material          TEXT                        NULL,
    material_clean    TEXT                        NULL,
    price_etb         FLOAT                       NULL,
    unit              VARCHAR(50)                 NULL,
    unit_standard     VARCHAR(50)                 NULL,
    last_checked      DATE                        NULL,
    detail_url        TEXT                        NULL,
    scraped_at        DATETIME                    NULL,
    is_outdated       TINYINT(1)                  NULL DEFAULT 0,
    days_since_update INT                         NULL,
    price_etb_valid   TINYINT(1)                  NULL DEFAULT 1,

    -- Optional useful indexes
    INDEX idx_category       (category),
    INDEX idx_last_checked   (last_checked),
    INDEX idx_is_outdated    (is_outdated),
    INDEX idx_price_etb      (price_etb)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;