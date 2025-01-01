-- 创建竞争对手分析表
CREATE TABLE competitor_analysis (
    competitor_id INT COMMENT '竞争对手ID',
    market_share DECIMAL(10,6) COMMENT '市场份额(0-1)',
    product_category STRING COMMENT '产品类别(Electronics/Clothing/Food)',
    customer_rating DECIMAL(4,2) COMMENT '客户评分(1-5)',
    sales_volume INT COMMENT '销售量',
    product_range INT COMMENT '产品种类数量',
    price_range DECIMAL(10,2) COMMENT '价格区间',
    location STRING COMMENT '地理位置(Asia/EU/US)',
    ad_spend DECIMAL(10,2) COMMENT '广告支出',
    social_media_engagement DECIMAL(10,2) COMMENT '社交媒体互动量'
)
COMMENT '竞争对手分析表'
PARTITIONED BY (year INT, quarter INT)
CLUSTERED BY (competitor_id) INTO 8 BUCKETS
STORED AS ORC
TBLPROPERTIES ('orc.compress'='SNAPPY'); 