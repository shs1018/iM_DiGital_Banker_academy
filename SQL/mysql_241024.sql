USE classicmodels;

SELECT
	customerName
	, count(*) as NumOfOrders
from
	orders od
    inner join customers cs USING(customerNumber)
group by
	customerName
Having
	count(*) >= 5
order by 
	count(*) DESC
;

-- 서브쿼리 
-- employees, offices
-- FIND employees who working at USA!

SELECT * FROM employees;

select 
	*
from 
employees ep 
	left join offices ofs USING (officeCode)
where country = 'USA'
;

-- USE subquery to NOT using JOIN()

select lastname, firstname, email from employees WHERE OFFICECODE in (1,2,3);

select 
	firstName
	, lastName
    , email
from
	employees
where
	officecode IN 
    (SELECT officecode FROM offices WHERE country = 'USA')
;

-- 최소 금액 경제 고객 찾기
-- 메인 쿼리: 고객 출력
-- 서브 쿼리: 최소 금액 결제

select * from payments;
select * from customers;

select
	customernumber,
    checknumber,
    amount
from payments
where amount = (select MIN(amount) from payments)
;

--

select
	customernumber,
    checknumber,
    amount
from payments
where 
	amount > (select 
				AVG(amount) 
				from payments)
order by 
	amount DESC
;

-- 주문번호 50개 초과, 주문번호와 주문날짜
-- 서브쿼리와 메인 쿼리를 따로 짜고 합치자!!
select * from orders;

Select 
	distinct ordernumber,
    orderdate
from 
	orders
where
	Ordernumber IN (select 
						ordernumber
					from 
						orderdetails
					where
						quantityordered > 50)
;

--

select customername
from customers
where customernumber NOT IN 
					(select distinct customernumber 
					from orders)
;

--

select productname from products
where productcode not in (select distinct productcode from orderdetails) ;

-- 인라인 뷰, FROM절 서브쿼리
-- 임시 테이블 생성같은 느낌?
-- 최대, 최소, 평균 등을 함께 나타내고 싶을 때

select MAX(items), MIN(items), AVG(items) as AVGorder
from(
	select ordernumber, count(ordernumber) AS items
	from orderdetails
	group by ordernumber
) A
;

-- 가장 비싼 생산품 5개를 출력하시오.
-- FROM절 서브쿼리(인라인 뷰)를 활용할 것
-- PRODUCTNAME, BUYPRICE를 사용해야 함.

-- 출력 갯수 정하기: LIMIT Number -> FROM절에 사용

select productname, buyprice
from
(
select productname,
	buyprice
from 
	products
order by
	buyprice DESC
) 
A LIMIT 5
;

--

select *
from (
select 
	productcode, AVG(quantityordered) as avgq
from 
	orderdetails
group by 
	productcode
order by avgq DESC
) A
LIMIT 5
;

--

-- 외출


--

USE temp;

CREATE TABLE sales(
    sales_employee VARCHAR(50) NOT NULL,
    fiscal_year INT NOT NULL,
    sale DECIMAL(14,2) NOT NULL,
    PRIMARY KEY(sales_employee,fiscal_year)
);

INSERT INTO sales(sales_employee,fiscal_year,sale)
VALUES('Bob',2016,100),
      ('Bob',2017,150),
      ('Bob',2018,200),
      ('Alice',2016,150),
      ('Alice',2017,100),
      ('Alice',2018,200),
       ('John',2016,200),
      ('John',2017,150),
      ('John',2018,250);

SELECT * FROM sales;

--

select sum(sale) from sales;
select fiscal_year, sum(sale) from sales group by 1;


-- 윈도우 함수 사용
select 
	fiscal_year,
    sales_employee,
    sale,
    sum(sale) over (partition by fiscal_year) as total_sales,
    sum(sale) over () as total_total_sales,
    sum(sale) over ( order by fiscal_year) as total_total_total_sales
    
from
	sales
;

---\	fiscal_year
    , sales_employee
    , sale
    -- , SUM(sale) OVER (PARTITION BY fiscal_year) total_sales
    -- , SUM(sale) OVER () total_sales
    -- , SUM(sale) OVER (PARTITION BY fiscal_year ORDER BY sale) total_sales
    -- , SUM(sale) OVER (ORDER BY fiscal_year) total_sales
    , SUM(sale) OVER (PARTITION BY fiscal_year ORDER BY sale ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS 복잡스럽다
FROM 
	sal
    	fiscal_year
    , sales_employee
    , sale
    -- , SUM(sale) OVER (PARTITION BY fiscal_year) total_sales
    -- , SUM(sale) OVER () total_sales
    -- , SUM(sale) OVER (PARTITION BY fiscal_year ORDER BY sale) total_sales
    -- , SUM(sale) OVER (ORDER BY fiscal_year) total_sales
    , SUM(sale) OVER (PARTITION BY fiscal_year ORDER BY sale ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS 복잡스럽다
FROM 
	sales
    
    	sal
    	fiscal_year
    , sales_employee
    , sale
    -- , SUM(sale) OVER (PARTITION BY fiscal_year) total_sales
    -- , SUM(sale) OVER () total_sales
    -- , SUM(sale) OVER ()pedPARTITION BY fiscal_year ORDER BY sale) total_sales
    -- , SUM(sale) OVER (ORDER BY fiscal_year) total_sales
    , SUM(sale) OVER (PARTITION BY fiscal_year ORDER BY sale ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS 복잡스럽다
FROM 
	SELECT 
	fiscal_year
    , sales_employee
    , sale
    -- , SUM(sale) OVER (PARTITION BY fiscal_year) total_sales
    -- , SUM(sale) OVER () total_sales
    -- , SUM(sale) OVER (PARTITION BY fiscal_year ORDER BY sale) total_sales
    -- , SUM(sale) OVER (ORDER BY fiscal_year) total_sales
    -- , SUM(sale) OVER (ORDER BY fiscal_year ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS 복잡스럽다
    -- , SUM(sale) OVER (ORDER BY fiscal_year ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS 복잡스럽다2
	, SUM(sale) OVER (ORDER BY fiscal_year ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS 복잡스럽다3
FROM 
	sales
;
    
    
-- LAG
USE classic;


SELECT 
	fiscal_year,
	sale,
	sales_employee,
	LAG(sale, 1, 0) OVER (partition by sales_employee
						order by fiscal_year) as "privious_dat"
From sales
;