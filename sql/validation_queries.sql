-- =====================================================
-- VALIDAR TABLA RAW
-- =====================================================

SELECT COUNT(*) AS total_rows
FROM retail_analytics_db.raw;


-- =====================================================
-- VALIDAR TABLA PROCESSED
-- =====================================================

SELECT COUNT(*) AS total_rows
FROM retail_analytics_db.processed;


-- =====================================================
-- VALIDAR CATEGORÍAS NULAS
-- =====================================================

SELECT COUNT(*) AS null_categories

FROM retail_analytics_db.processed

WHERE category IS NULL;


-- =====================================================
-- VALIDAR PRECIOS PROMEDIO NULOS
-- =====================================================

SELECT COUNT(*) AS null_avg_price

FROM retail_analytics_db.processed

WHERE avg_price IS NULL;


-- =====================================================
-- VALIDAR PRECIOS NEGATIVOS
-- =====================================================

SELECT COUNT(*) AS negative_prices

FROM retail_analytics_db.processed

WHERE avg_price < 0;


-- =====================================================
-- VALIDAR TOTAL PRODUCTS NEGATIVOS
-- =====================================================

SELECT COUNT(*) AS invalid_products

FROM retail_analytics_db.processed

WHERE total_products < 0;


-- =====================================================
-- VALIDAR DUPLICADOS
-- =====================================================

SELECT

    category,

    COUNT(*) AS duplicates

FROM retail_analytics_db.processed

GROUP BY category

HAVING COUNT(*) > 1;
