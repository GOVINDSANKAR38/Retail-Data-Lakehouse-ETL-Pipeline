-- =====================================================
-- VER TODOS LOS RESULTADOS PROCESADOS
-- =====================================================

SELECT *
FROM retail_analytics_db.processed;


-- =====================================================
-- PRODUCTOS POR CATEGORÍA
-- =====================================================

SELECT

    category,

    total_products

FROM retail_analytics_db.processed

ORDER BY total_products DESC;


-- =====================================================
-- PRECIO PROMEDIO POR CATEGORÍA
-- =====================================================

SELECT

    category,

    avg_price

FROM retail_analytics_db.processed

ORDER BY avg_price DESC;


-- =====================================================
-- TOP 5 CATEGORÍAS MÁS CARAS
-- =====================================================

SELECT

    category,

    avg_price

FROM retail_analytics_db.processed

ORDER BY avg_price DESC

LIMIT 5;


-- =====================================================
-- TOP 5 CATEGORÍAS CON MÁS PRODUCTOS
-- =====================================================

SELECT

    category,

    total_products

FROM retail_analytics_db.processed

ORDER BY total_products DESC

LIMIT 5;

-- =====================================================
-- COMPARACIÓN RAW VS PROCESSED
-- =====================================================

SELECT

    (SELECT COUNT(*) FROM retail_analytics_db.raw)
        AS raw_records,

    (SELECT SUM(total_products)
     FROM retail_analytics_db.processed)
        AS processed_records;
