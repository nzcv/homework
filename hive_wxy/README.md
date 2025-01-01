1. 竞争对手分析


背景介绍：在电商行业，了解竞争对手的市场表现至关重要。通过分析竞争对手的市场份额、产品种类和客户满意度，商家能够识别自身的市场定位，并制定更有效的竞争策略。
数据集名称：competitor_analysis_data.csv

第2章  源数据介绍

2.1 数据来源	1

在电商行业，了解竞争对手的市场表现至关重要。通过分析竞争对手的市场份额、产品种类和客户满意度，商家能够识别自身的市场定位，并制定更有效的竞争策略。本数据集来源于某大型电商平台的竞争对手分析系统,包含了2023年第三季度的竞争对手相关数据

2.2 数据介绍	1

数据涵盖了多个维度:
- 竞争对手基本信息(competitor_id)
- 市场表现指标(market_share, sales_volume) 
- 产品维度(product_category, product_range, price_range)
- 客户反馈(customer_rating)
- 地理分布(location)
- 营销投入(ad_spend, social_media_engagement)
数据通过该平台的商业智能系统自动采集和汇总,经过脱敏处理后供分析使用。采集频率为每日更新,本数据集选取了季度汇总数据进行分析。

2.3 数据清洗

通过分析数据发现存在一些重复行，需要进行数据清洗。使用以下shell命令删除重复行:

```shell
awk '!seen[$0]++' competitor_analysis_data.csv > competitor_analysis_data_cleaned.csv
```

第3章  Hive数据库设计	1
3.1 表的物理设计

根据competitor_analysis.sql中的表结构设计, 各字段的物理设计如下:

字段名称	类型	长度	是否为空	注释
competitor_id	INT	4	NOT NULL	竞争对手ID
market_share	DECIMAL	10,6	NOT NULL	市场份额(0-1)
product_category	STRING	20	NOT NULL	产品类别(Electronics/Clothing/Food)
customer_rating	DECIMAL	4,2	NOT NULL	客户评分(1-5)
sales_volume	INT	8	NOT NULL	销售量
product_range	INT	4	NOT NULL	产品种类数量
price_range	DECIMAL	10,2	NOT NULL	价格区间
location	STRING	10	NOT NULL	地理位置(Asia/EU/US)
ad_spend	DECIMAL	10,2	NOT NULL	广告支出
social_media_engagement	DECIMAL	10,2	NOT NULL	社交媒体互动量
year	INT	4	NOT NULL	年份(分区字段)
quarter	INT	1	NOT NULL	季度(分区字段)

## Hive连接

https://github.com/big-data-europe/docker-hive

```
  $ docker-compose exec hive-server bash
  # /opt/hive/bin/beeline -u jdbc:hive2://localhost:10000
  > CREATE TABLE pokes (foo INT, bar STRING);
  > LOAD DATA LOCAL INPATH '/opt/hive/examples/files/kv1.txt' OVERWRITE INTO TABLE pokes;
```

3.2 创建数据库
使用以下命令创建数据库:

```sql
CREATE DATABASE IF NOT EXISTS competitor_analysis;
```

3.3 创建表
使用以下命令创建表:

```sql
CREATE TABLE IF NOT EXISTS competitor_analysis.competitor_analysis_data (
  competitor_id INT,
  market_share DECIMAL(10,6),
  product_category STRING,
  customer_rating DECIMAL(4,2),
  sales_volume INT,
  product_range INT,
  price_range DECIMAL(10,2),
  location STRING,
  ad_spend DECIMAL(10,2),
  social_media_engagement DECIMAL(10,2)
);
```

第4章  数据导入
4.1 导入方法
使用hive导入数据

```sql
LOAD DATA INPATH '/user/hive/warehouse/competitor_analysis_data_cleaned.csv' INTO TABLE competitor_analysis.competitor_analysis_data;
``` 

4.2 数据确认

```sql
SELECT * FROM competitor_analysis.competitor_analysis_data;
```


第5章  数据分析
5.1 分析数据

1. 各产品类别的市场份额分析
```sql
SELECT 
    product_category,
    ROUND(AVG(market_share) * 100, 2) as avg_market_share,
    COUNT(*) as competitor_count
FROM competitor_analysis.competitor_analysis_data
GROUP BY product_category
ORDER BY avg_market_share DESC;
```

2. 客户评分与销售量的相关性分析
```sql
SELECT 
    CASE 
        WHEN customer_rating <= 2 THEN '低评分(1-2)'
        WHEN customer_rating <= 4 THEN '中评分(2-4)'
        ELSE '高评分(4-5)'
    END as rating_category,
    ROUND(AVG(sales_volume), 0) as avg_sales,
    COUNT(*) as count
FROM competitor_analysis.competitor_analysis_data
GROUP BY CASE 
    WHEN customer_rating <= 2 THEN '低评分(1-2)'
    WHEN customer_rating <= 4 THEN '中评分(2-4)'
    ELSE '高评分(4-5)'
END
ORDER BY avg_sales DESC;
```

3. 不同地区的竞争格局分析
```sql
SELECT 
    location,
    product_category,
    COUNT(*) as competitor_count,
    ROUND(AVG(market_share) * 100, 2) as avg_market_share,
    ROUND(AVG(customer_rating), 2) as avg_rating
FROM competitor_analysis.competitor_analysis_data
GROUP BY location, product_category
ORDER BY location, avg_market_share DESC;
```

4. 广告支出与社交媒体互动关系分析
```sql
SELECT 
    NTILE(4) OVER (ORDER BY ad_spend) as ad_spend_quartile,
    ROUND(AVG(ad_spend), 2) as avg_ad_spend,
    ROUND(AVG(social_media_engagement), 2) as avg_social_engagement,
    ROUND(AVG(market_share) * 100, 2) as avg_market_share
FROM competitor_analysis.competitor_analysis_data
GROUP BY NTILE(4) OVER (ORDER BY ad_spend)
ORDER BY ad_spend_quartile;
```

5. 产品多样性与市场表现分析
```sql
SELECT 
    CASE 
        WHEN product_range <= 100 THEN '小规模(≤100)'
        WHEN product_range <= 150 THEN '中规模(101-150)'
        ELSE '大规模(>150)'
    END as range_category,
    COUNT(*) as competitor_count,
    ROUND(AVG(market_share) * 100, 2) as avg_market_share,
    ROUND(AVG(sales_volume), 0) as avg_sales
FROM competitor_analysis.competitor_analysis_data
GROUP BY CASE 
    WHEN product_range <= 100 THEN '小规模(≤100)'
    WHEN product_range <= 150 THEN '中规模(101-150)'
    ELSE '大规模(>150)'
END
ORDER BY avg_market_share DESC;
```

6. 价格策略分析
```sql
SELECT 
    product_category,
    ROUND(MIN(price_range), 2) as min_price,
    ROUND(AVG(price_range), 2) as avg_price,
    ROUND(MAX(price_range), 2) as max_price,
    ROUND(AVG(market_share) * 100, 2) as avg_market_share
FROM competitor_analysis.competitor_analysis_data
GROUP BY product_category
ORDER BY avg_market_share DESC;
```

7. top10竞争对手综合分析
```sql
SELECT 
    competitor_id,
    ROUND(market_share * 100, 2) as market_share_pct,
    product_category,
    customer_rating,
    sales_volume,
    location
FROM competitor_analysis.competitor_analysis_data
ORDER BY market_share DESC
LIMIT 10;
```

8. 客户评分最高的竞争对手特征分析
```sql
SELECT 
    competitor_id,
    customer_rating,
    product_category,
    product_range,
    ROUND(price_range, 2) as price_range,
    ROUND(ad_spend, 2) as ad_spend,
    location
FROM competitor_analysis.competitor_analysis_data
WHERE customer_rating > 4.5
ORDER BY customer_rating DESC;
```

9. 各地区市场集中度分析
```sql
SELECT 
    location,
    COUNT(DISTINCT competitor_id) as competitor_count,
    ROUND(SUM(market_share) * 100, 2) as total_market_share,
    ROUND(MAX(market_share) * 100, 2) as max_market_share
FROM competitor_analysis.competitor_analysis_data
GROUP BY location
ORDER BY total_market_share DESC;
```

10. 营销效率分析
```sql
SELECT 
    competitor_id,
    ROUND(ad_spend / sales_volume, 2) as cost_per_sale,
    ROUND(social_media_engagement / ad_spend * 100, 2) as engagement_rate,
    market_share,
    product_category,
    location
FROM competitor_analysis.competitor_analysis_data
WHERE sales_volume > 0
ORDER BY cost_per_sale ASC
LIMIT 10;
```

这些分析可以帮助我们:
- 了解不同产品类别的市场竞争状况
- 发现客户评分与销售量的关系
- 识别不同地区的市场特点
- 评估营销投入的效果
- 分析产品策略的影响
- 找出成功竞争对手的共同特征

第6章  结论导出
6.1 Sqoop命令

6.2 导出截图
6.3 MySQL中查询分析结果
第7章  总  结
