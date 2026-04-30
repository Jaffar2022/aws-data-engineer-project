#Manually create table using AWS Athena instead of AWS Glue using Crawler, 
#but the best way is to use Crawler to automatically create the table based on the data in S3.

CREATE EXTERNAL TABLE sales_db.sales (
    order_id INT,
    product STRING,
    category STRING,
    amount INT,
    order_date DATE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION 's3://your-bucket/sales-data/raw/';


-- Total revenue
SELECT SUM(amount) FROM sales_db.sales;

-- Revenue by category
SELECT category, SUM(amount)
FROM sales_db.sales
GROUP BY category;

-- Top products
SELECT product, SUM(amount) AS revenue
FROM sales_db.sales
GROUP BY product
ORDER BY revenue DESC;