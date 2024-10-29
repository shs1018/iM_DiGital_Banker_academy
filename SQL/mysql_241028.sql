show DATABASES;

USE book_ratings;

CREATE TABLE books(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    genre VARCHAR(100),
    release_year YEAR(4)
)
;

describe books;
-- DROP TABLE books;


USE classicmodels;

SELECT
	productline,
	count(*)
from products
group by 1
;

select * from orderdetails;


-- -----------------------------------------------

use classicmodels;

CREATE TABLE sales
SELECT
    productLine,
    YEAR(orderDate) orderYear,
    SUM(quantityOrdered * priceEach) orderValue
FROM
    orderDetails
        INNER JOIN
    orders USING (orderNumber)
        INNER JOIN
    products USING (productCode)
GROUP BY
    productLine ,
    YEAR(orderDate);
    
    -- Group by
    -- Roll up Method
    Select 
		productline,
        sum(ordervalue) as sumVal
	from 
		sales
	group by 
		1
	;
    
    -- -----
    
    select NULL, sum(ordervalue) as sumVal from sales;
    
    -- ROLL UP => 안쓰고 대신 UNION을 사용하면?
    -- UNION ALL
    
        Select 
		productline,
        sum(ordervalue) as sumVal
	from 
		sales
	group by 
		1
	UNION ALL
	select NULL, sum(ordervalue) as sumVal from sales;
    -- 두 개의 쿼리를 합친 효과

-- ROLLUP: Grouping 함수
select 
	productline,
    sum(ordervalue) as Total
from sales
group by 
	productline with ROLLUP
;
    
-- orderyear 같이 Grouping
select 
	orderyear,
	productline,
    sum(ordervalue) as Total
from sales
group by 
	orderyear,
    productline with rollup
;

-- -------------------------------------------
-- 출력: 매니저, 보고대상자
select * from employees;

-- SELF JOIN
select 
	concat(m.lastname, ',', m.firstname) as worker,
    concat(e.lastname, ',', e.firstname) as superviser
from
	employees e
inner join employees m
on e.employeenumber = m.reportsTo
;

-- 

select 
	*
from 
(
select 
	C.country
    , sum(B.priceEach * B.quantityOrdered) AS sales
From
	orders A
    left Join orderdetails B
		USING(ordernumber)
	left join customers C
		USING(customerNumber)
	group by 1
    order by 2 DESC
)A
;
