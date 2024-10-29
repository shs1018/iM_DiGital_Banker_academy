-- 1번
USE CLASSICMODELS;

select DISTINCT
	 state
    , city
from 
	customers
order by 1 DESC
;

-- 2번
USE CLASSICMODELS;

select 
	year(orderdate) 연도별
    , count(DISTINCT ordernumber) 구매자수
    , sum(quantityordered * priceeach) 매출액
    , sum(quantityordered * priceeach) / count(DISTINCT ordernumber) ATV
from orders
	left join orderdetails 
		using(ordernumber)
group by 1
order by 1
;

-- 3번
USE CLASSICMODELS;

SELECT 
     Case when ct.country in ('USA', 'Canada') then "북미지역"
           else "비북미지역" END as 지역구분
    , sum(quantityOrdered * priceEach)  as 매출액
from customers ct
right join orders od using(customernumber)
right join orderdetails odd using(orderNumber)
group by 1
order by 1
;

-- 4번
USE CLASSICMODELS;

SELECT 
	CASE WHEN DIFF >= 90 THEN "이탈고객" 
			when DIFF Between 30 and 89 then "마케팅대상고객"
            else "비이탈고객"
	END AS 이탈유무
    , COUNT(DISTINCT customernumber) AS 명수
FROM (
	SELECT 
		customernumber
		, mx_order
		, '2005-06-01'
		, DATEDIFF('2005-06-01', mx_order) AS DIFF
	FROM (
		SELECT 
			customernumber
			, MAX(orderdate) mx_order
		FROM 
			orders
		GROUP BY 1
	) A
) A
group by 1
order by 2 DESC
;

-- 5번 
USE CLASSICMODELS;

select 
	st.*,
	row_number() OVER (order by sales DESC)
from stat st
;

-- 6번
USE titanic;

select floor(AGE/10) * 10 as AGEBAND
	, SEX
	, count(*) as N_PASSENGERS
    , sum(survived) as N_SURVIVED
    , sum(survived)/count(*) as SURVIVED_RATE
from titanic
group by 1,2
order by 2
;

-- 7번
use dataset2;

select 
	`Department Name`,
    `Clothing ID`,
    AVG(Rating) AVG_RATE,
	row_number() OVER (order by (AVG(Rating)))
from dataset2
where `department Name` in ('BOTTOMS')
group by 1,2 LIMIT 5
;
