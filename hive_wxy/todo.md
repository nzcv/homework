## 数据清洗

### 1. 删除重复记录
```sql
CREATE TABLE sales_prediction_cleaned AS
SELECT DISTINCT * FROM sales_prediction;
```
**分析总结**: 该查询删除了表中的重复记录，确保数据的唯一性。

### 2. 处理缺失值
```sql
CREATE TABLE sales_prediction_cleaned AS
SELECT 
    product_id,
    price,
    COALESCE(discount, 0) AS discount,
    COALESCE(season, 'Unknown') AS season,
    COALESCE(promotion, 'No') AS promotion,
    quantity_sold_last_quarter,
    stock_quantity,
    COALESCE(rating, 0) AS rating,
    COALESCE(reviews_count, 0) AS reviews_count,
    category,
    sales_forecast
FROM sales_prediction;
```
**分析总结**: 该查询使用默认值替换了缺失值，确保数据完整性。

### 3. 数据类型转换
```sql
CREATE TABLE sales_prediction_cleaned AS
SELECT 
    product_id,
    CAST(price AS DOUBLE) AS price,
    CAST(discount AS DOUBLE) AS discount,
    season,
    promotion,
    CAST(quantity_sold_last_quarter AS INT) AS quantity_sold_last_quarter,
    CAST(stock_quantity AS INT) AS stock_quantity,
    CAST(rating AS DOUBLE) AS rating,
    CAST(reviews_count AS INT) AS reviews_count,
    category,
    CAST(sales_forecast AS INT) AS sales_forecast
FROM sales_prediction;
```
**分析总结**: 该查询确保了每列的数据类型正确，避免数据类型不一致的问题。

### 4. 删除异常值
```sql
CREATE TABLE sales_prediction_cleaned AS
SELECT *
FROM sales_prediction
WHERE price > 0 AND discount >= 0 AND discount <= 1 AND rating >= 0 AND rating <= 5;
```
**分析总结**: 该查询删除了价格、折扣和评分中的异常值，确保数据的合理性。

### 5. 标准化数据
```sql
CREATE TABLE sales_prediction_cleaned AS
SELECT 
    product_id,
    (price - avg_price) / stddev_price AS price,
    discount,
    season,
    promotion,
    quantity_sold_last_quarter,
    stock_quantity,
    rating,
    reviews_count,
    category,
    sales_forecast
FROM (
    SELECT *,
        AVG(price) OVER () AS avg_price,
        STDDEV(price) OVER () AS stddev_price
    FROM sales_prediction
) t;
```
**分析总结**: 该查询对价格进行了标准化处理，确保数据的可比性。


# Hive Database Schema Design for Sales Prediction Data

## 表: sales_prediction

### 列:
- `product_id` INT
- `price` DOUBLE
- `discount` DOUBLE
- `season` STRING
- `promotion` STRING
- `quantity_sold_last_quarter` INT
- `stock_quantity` INT
- `rating` DOUBLE
- `reviews_count` INT
- `category` STRING
- `sales_forecast` INT

### 创建表语句:
```sql
CREATE TABLE sales_prediction (
    product_id INT,
    price DOUBLE,
    discount DOUBLE,
    season STRING,
    promotion STRING,
    quantity_sold_last_quarter INT,
    stock_quantity INT,
    rating DOUBLE,
    reviews_count INT,
    category STRING,
    sales_forecast INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

## 表的物理设计

| 字段名称                     | 类型   | 长度 | 是否为空 | 注释                           |
|-----------------------------|--------|------|----------|--------------------------------|
| `product_id`                | INT    | -    | 否       | 产品的唯一标识符               |
| `price`                     | DOUBLE | -    | 否       | 产品价格                       |
| `discount`                  | DOUBLE | -    | 是       | 产品折扣                       |
| `season`                    | STRING | -    | 是       | 产品季节                       |
| `promotion`                 | STRING | -    | 是       | 促销详情                       |
| `quantity_sold_last_quarter`| INT    | -    | 否       | 上季度销售数量                 |
| `stock_quantity`            | INT    | -    | 否       | 库存数量                       |
| `rating`                    | DOUBLE | -    | 是       | 产品评分                       |
| `reviews_count`             | INT    | -    | 是       | 评论数量                       |
| `category`                  | STRING | -    | 否       | 产品类别                       |
| `sales_forecast`            | INT    | -    | 否       | 销售预测                       |


## 创建表
### 创建表的步骤

1. **连接到Hive**:
    ```bash
    hive
    ```

2. **创建数据库**
```sql
CREATE DATABASE sale_db;
```

2. **使用数据库**:
    ```sql
    USE sale_db;
    ```

3. **创建表**:
    ```sql
    CREATE TABLE sales_prediction (
         product_id INT,
         price DOUBLE,
         discount DOUBLE,
         season STRING,
         promotion STRING,
         quantity_sold_last_quarter INT,
         stock_quantity INT,
         rating DOUBLE,
         reviews_count INT,
         category STRING,
         sales_forecast INT
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE;
    ```

4. **验证表创建**:
    ```sql
    SHOW TABLES;
    ```
    
    
    ```bash
    docker cp /home/chew/Documents/hive_task_01/sales_prediction_data.csv <container_id>:/data.csv
    ```

5. **加载数据**:

    ```sql
    LOAD DATA LOCAL INPATH '/data.csv' INTO TABLE sales_prediction;
    ```

6. **查询数据**:
    ```sql
    SELECT * FROM sales_prediction;
    ```

    ## 数据分析

    ### 1. 产品价格分布
    ```sql
    SELECT price, COUNT(*) as count
    FROM sales_prediction
    GROUP BY price
    ORDER BY price;
    ```
    **分析总结**: 该查询展示了不同价格的产品数量分布，帮助了解价格区间的集中程度。

    ### 产品价格分布总结
    根据产品价格分布查询结果，我们可以观察到以下几点：

    1. **价格区间集中**: 大部分产品的价格集中在某些特定区间，这些区间可能是市场上较为常见的价格范围。
    2. **高价产品较少**: 高价产品的数量相对较少，可能是因为高价产品的市场需求较低或目标客户群体较小。
    3. **低价产品较多**: 低价产品的数量较多，可能是因为低价产品更容易被消费者接受，市场需求较大。

    通过这些观察，我们可以进一步分析不同价格区间的产品销售情况，优化定价策略，提高销售额。


    ### 2. 折扣对销售的影响
    ```sql
    SELECT discount, AVG(sales_forecast) as avg_sales_forecast
    FROM sales_prediction
    GROUP BY discount
    ORDER BY discount;
    ```
    **分析总结**: 该查询展示了不同折扣下的平均销售预测，帮助评估折扣策略的有效性。
    
    ### 折扣对销售的影响总结
    根据折扣对销售的影响查询结果，我们可以观察到以下几点：

    1. **折扣与销售预测的正相关性**: 一般来说，较高的折扣会带来较高的销售预测。这表明折扣策略在一定程度上能够刺激销售增长。
    2. **折扣效果的边际递减**: 在某些情况下，折扣的增加对销售预测的提升效果逐渐减弱。这可能是因为消费者对折扣的敏感度有限，过高的折扣并不能显著增加销售。
    3. **最佳折扣区间**: 通过分析不同折扣下的平均销售预测，可以识别出一个最佳折扣区间，在该区间内，折扣对销售的提升效果最为显著。

    通过这些观察，我们可以优化折扣策略，选择合适的折扣幅度，以最大化销售额和利润。


    ### 3. 季节性销售趋势
    ```sql
    SELECT season, SUM(sales_forecast) as total_sales_forecast
    FROM sales_prediction
    GROUP BY season
    ORDER BY season;
    ```
    **分析总结**: 该查询展示了不同季节的总销售预测，帮助识别季节性销售趋势。




    ### 4. 促销活动效果
    ```sql
    SELECT promotion, SUM(sales_forecast) as total_sales_forecast
    FROM sales_prediction
    GROUP BY promotion
    ORDER BY total_sales_forecast DESC;
    ```
    **分析总结**: 该查询展示了不同促销活动的总销售预测，帮助评估促销活动的效果。

    ### 5. 库存与销售预测关系
    ```sql      
    SELECT stock_quantity, AVG(sales_forecast) as avg_sales_forecast
    FROM sales_prediction
    GROUP BY stock_quantity
    ORDER BY stock_quantity;
    ```
    **分析总结**: 该查询展示了库存数量与平均销售预测的关系，帮助优化库存管理。

    ### 6. 产品评分与销售预测关系
    ```sql
    SELECT rating, AVG(sales_forecast) as avg_sales_forecast
    FROM sales_prediction
    GROUP BY rating
    ORDER BY rating;
    ```
    **分析总结**: 该查询展示了产品评分与平均销售预测的关系，帮助了解评分对销售的影响。

    ### 7. 评论数量与销售预测关系
    ```sql
    SELECT reviews_count, AVG(sales_forecast) as avg_sales_forecast
    FROM sales_prediction
    GROUP BY reviews_count
    ORDER BY reviews_count;
    ```
    **分析总结**: 该查询展示了评论数量与平均销售预测的关系，帮助了解用户反馈对销售的影响。

    ### 8. 产品类别销售分析
    ```sql
    SELECT category, SUM(sales_forecast) as total_sales_forecast
    FROM sales_prediction
    GROUP BY category
    ORDER BY total_sales_forecast DESC;
    ```
    **分析总结**: 该查询展示了不同产品类别的总销售预测，帮助识别畅销类别。

    ### 9. 上季度销售与销售预测关系
    ```sql
    SELECT quantity_sold_last_quarter, AVG(sales_forecast) as avg_sales_forecast
    FROM sales_prediction
    GROUP BY quantity_sold_last_quarter
    ORDER BY quantity_sold_last_quarter;
    ```
    **分析总结**: 该查询展示了上季度销售数量与平均销售预测的关系，帮助预测未来销售。

    ### 10. 综合分析
    ```sql
    SELECT category, season, AVG(price) as avg_price, AVG(discount) as avg_discount, AVG(sales_forecast) as avg_sales_forecast
    FROM sales_prediction
    GROUP BY category, season
    ORDER BY category, season;
    ```
    **分析总结**: 该查询综合展示了不同类别和季节的平均价格、折扣和销售预测，帮助进行全面的市场分析。



    ## 使用 Sqoop 导出数据

    ### 1. 导出数据到 MySQL
    ```bash
    sqoop export \
    --connect jdbc:mysql://localhost/sale_db \
    --username root \
    --password password \
    --table sales_prediction \
    --export-dir /user/hive/warehouse/sale_db.db/sales_prediction \
    --input-fields-terminated-by ',' \
    --input-lines-terminated-by '\n'
    ```
    **分析总结**: 该命令使用 Sqoop 将 Hive 中的 `sales_prediction` 表数据导出到 MySQL 数据库中的 `sales_prediction` 表。
    