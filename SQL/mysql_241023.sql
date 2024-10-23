USE classicmodels;

-- SQL 순서
-- FROM => WHERE => GROUP BY => SELECT => DISTINCT => ORDER BY

-- GROUP BY vs DISTINCT 비교
-- 테이블명 : orders 
SELECT 
	status
FROM 
	orders
GROUP BY 
	status
;

-- DISTINCT 
SELECT 
	DISTINCT status
FROM 
	orders
;

-- GROUP BY : COUNT()
SELECT 
	status
    , COUNT(*)
FROM 
	orders
GROUP BY 
	status
;

-- 테이블명 : orderdetails
SELECT * FROM orderdetails;

SELECT 
	orderNumber
    , quantityOrdered * priceEach AS 매출액
FROM
	orderdetails
;

-- 주문번호당, 총매출액, 평균매출액을 구하세요 (~23분)
SELECT 
	orderNumber
    , SUM(quantityOrdered * priceEach) AS 총매출액
    , AVG(quantityOrdered * priceEach) AS 평균매출액
    , stddev_samp(quantityOrdered * priceEach) AS 표준편차
    , var_samp(quantityOrdered * priceEach) AS 분산
FROM
	orderdetails
GROUP BY 
	orderNumber
;

-- productCode, orderLineNumber 당 집계함수
-- 주문번호당, 총매출액, 평균매출액을 구하세요 (~23분)
SELECT 
	productCode
    , orderLineNumber
    , SUM(quantityOrdered * priceEach) AS 총매출액
    , AVG(quantityOrdered * priceEach) AS 평균매출액
    , stddev_samp(quantityOrdered * priceEach) AS 표준편차
    , var_samp(quantityOrdered * priceEach) AS 분산
FROM
	orderdetails
GROUP BY 
	productCode
    , orderLineNumber
ORDER BY
	productCode
    , orderLineNumber
;

-- HAVING
-- 순서 : FROM ==> WHERE ==> GROUP BY ==> HAVING ==> SELECT ==> ...
-- 위에 있는 코드에서 HAVING 절 추가
-- orderLineNumber에서 1만 별도로 조회
SELECT 
	productCode
    , orderLineNumber
    , SUM(quantityOrdered * priceEach) AS 총매출액
    , AVG(quantityOrdered * priceEach) AS 평균매출액
    , stddev_samp(quantityOrdered * priceEach) AS 표준편차
    , var_samp(quantityOrdered * priceEach) AS 분산
FROM
	orderdetails
GROUP BY 
	productCode
    , orderLineNumber
HAVING 
	orderLineNumber = 1 -- S10_1678 : 21889.92
    AND 총매출액 >= 10000 -- 메모 : 다른 DBMS에서는 에러 날 가능성 존재
ORDER BY
	productCode
    , orderLineNumber
;

-- 테이블명 : orderdetails
-- 출력값 
-- ordernumber 주문갯수 매출액 
-- 10100       151    10223.83 
-- 조건 : 주문갯수 700개 이상만 조회
-- 주문번호 : 10222
SELECT 
  ordernumber, 
  SUM(quantityOrdered) AS 주문갯수, 
  SUM(priceeach * quantityOrdered) AS 매출액 
FROM 
  orderdetails 
GROUP BY 
  ordernumber 
HAVING 
  주문갯수 > 700;

-- 테이블명 : orderdetails
-- 출력값 
-- ordernumber 주문갯수 매출액 
-- 10100       151    10223.83 
-- 조건 : 주문갯수 700개 이상만 조회
-- 주문번호 : 10222

SELECT 
  ordernumber, 
  SUM(quantityOrdered) AS totalOrder, 
  SUM(priceeach * quantityOrdered) AS TotalProfit 
FROM 
  orderdetails 
GROUP BY 
  ordernumber 
HAVING 
  totalOrder > 700;

--
-- JOIN
/*
CREATE TABLE members (
	member_id INT AUTO_INCREMENT
    , name varchar(100)
    , PRIMARY KEY (member_id)
)
;
*/
insert INTO members(name)
VALUES('A'), ('B'), ('C'), ('D'), ('E')
;

select * from members;

--
/*
CREATE TABLE committees (
    committee_id INT AUTO_INCREMENT,
    name VARCHAR(100),
    PRIMARY KEY (committee_id)
);
*/
insert into committees(name)
values('A'),('B'),('C'),('F');

--
/*
SELECT *
FROM table_1
USING table_2
INNER JOIN table_2 USING (col_name)
*/

-- 원래는 NAME 안씀 -> NAME에는 중복값이 존재할 수 있다!
select *
from members m
INNER JOIN committees c USING (name);

--

select *
from members m
INNER JOIN committees c ON c.name = m.name;

--

select *
from members m
INNER JOIN committees c ON c.committee_id = m.member_id;

--

select *
from members m
LEFT JOIN committees c ON c.committee_id = m.member_id;

--

select *
from members m
RIGHT JOIN committees c ON c.name = m.name;

--

select *
from members m
RIGHT JOIN committees c USING(name)
WHERE m.member_id IS NULL
;
--

select m.name as mname
, c.name as cname
from members m
RIGHT JOIN committees c ON c.name = m.name;

--
/*
일별 매출액
*/

select 
	od.orderDate
	, sum(odd.priceEach*odd.quantityOrdered) as totalProfit
from orders od
Inner join orderdetails odd USING(ordernumber)
group by od.orderDate
Having totalProfit > 100000
order by totalProfit DESC
;

--

select od.orderDate
	, sum(odd.priceEach*odd.quantityOrdered) as totalProfit
    , sum(odd.quantityOrdered* pd.buyPrice) as originalCost
	, sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice) as netProfit
	, (sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice)) / sum(odd.quantityOrdered* pd.buyPrice) * 100 as marginRate
from orders od
inner join orderdetails odd USING(ordernumber)
inner join products pd USING(productCode)
group by od.orderDate
order by netProfit DESC
;

-- RIGHT JOIN

select 
	od.orderDate
	, sum(odd.priceEach*odd.quantityOrdered) as totalProfit
from orders od
Right join orderdetails odd USING(ordernumber)
group by od.orderDate
;

-- SUBSTR()로 월별 매출액을 고르시오

select substr(od.orderDate,1,7)
	, sum(odd.priceEach*odd.quantityOrdered) as totalProfit
    , sum(odd.quantityOrdered* pd.buyPrice) as originalCost
	, sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice) as netProfit
	, (sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice)) / sum(odd.quantityOrdered* pd.buyPrice) * 100 as marginRate
from orders od
inner join orderdetails odd USING(ordernumber)
inner join products pd USING(productCode)
group by substr(od.orderDate,1,7)
order by netProfit DESC
;

--

select substr(od.orderDate,6,2)
	, sum(odd.priceEach*odd.quantityOrdered) as totalProfit
    , sum(odd.quantityOrdered* pd.buyPrice) as originalCost
	, sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice) as netProfit
	, (sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice)) / sum(odd.quantityOrdered* pd.buyPrice) * 100 as marginRate
from orders od
left join orderdetails odd 
ON od.orderNumber = odd.orderNumber
left join products pd 
ON odd.productCode = pd.productCode
group by substr(od.orderDate,6,2)
order by netProfit DESC
;

-- 연도별 매출액

select YEAR(od.orderDate)
	, sum(odd.priceEach*odd.quantityOrdered) as totalProfit
    , sum(odd.quantityOrdered* pd.buyPrice) as originalCost
	, sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice) as netProfit
	, (sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice)) / sum(odd.quantityOrdered* pd.buyPrice) * 100 as marginRate
from orders od
left join orderdetails odd 
ON od.orderNumber = odd.orderNumber
left join products pd 
ON odd.productCode = pd.productCode
group by YEAR(od.orderDate)
order by netProfit DESC
;

--

select quarter(od.orderDate)
	, sum(odd.priceEach*odd.quantityOrdered) as totalProfit
    , sum(odd.quantityOrdered* pd.buyPrice) as originalCost
	, sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice) as netProfit
	, (sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice)) / sum(odd.quantityOrdered* pd.buyPrice) * 100 as marginRate
from orders od
left join orderdetails odd 
ON od.orderNumber = odd.orderNumber
left join products pd 
ON odd.productCode = pd.productCode
group by quarter(od.orderDate)
order by netProfit DESC
;

--

select weekofyear(od.orderDate)
	, sum(odd.priceEach*odd.quantityOrdered) as totalProfit
    , sum(odd.quantityOrdered* pd.buyPrice) as originalCost
	, sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice) as netProfit
	, (sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice)) / sum(odd.quantityOrdered* pd.buyPrice) * 100 as marginRate
from orders od
left join orderdetails odd 
ON od.orderNumber = odd.orderNumber
left join products pd 
ON odd.productCode = pd.productCode
group by weekofyear(od.orderDate)
order by netProfit DESC
;

--

select year(od.orderDate), quarter(od.orderDate)
	, sum(odd.priceEach*odd.quantityOrdered) as totalProfit
    , sum(odd.quantityOrdered* pd.buyPrice) as originalCost
	, sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice) as netProfit
	, (sum(odd.priceEach*odd.quantityOrdered) - sum(odd.quantityOrdered* pd.buyPrice)) / sum(odd.quantityOrdered* pd.buyPrice) * 100 as marginRate
from orders od
left join orderdetails odd 
ON od.orderNumber = odd.orderNumber
left join products pd 
ON odd.productCode = pd.productCode
group by year(od.orderDate), quarter(od.orderDate)
order by netProfit DESC
;

-- 가정: 한 명의 고객이 여러 번 구매할 수 있다. => 중복값을 제거해야 한다!

select count(Distinct ordernumber)
	,count(ordernumber)
from orders
;
--
select quarter(orderdate)
	, count(distinct customernumber)
	, count(distinct ordernumber)
from orders
group by 1
order by 1
;

-- AMV(인당매출액)

select 
	year(orderDate) as year
    , count(distinct od.customernumber) as numCustomer
    , sum(quantityOrdered * priceEach)  as totalsales
    , (sum(quantityOrdered * priceEach))/count(distinct od.customernumber) as AMV
from orderdetails odd
	right join orders od using(ordernumber)
group by 1
order by 1
;

-- 건당매출액

select 
	year(orderDate) as year
    , count(distinct od.ordernumber) as numOrder
    , sum(quantityOrdered * priceEach)  as totalsales
    , (sum(quantityOrdered * priceEach))/count(distinct od.ordernumber) as AMV
from orderdetails odd
	right join orders od using(ordernumber)
group by 1
order by 1
;

-- 국가별, 도시별 매출액

select 
	ct.country
    , ct.city
    , count(distinct od.ordernumber) as numOrder
    , sum(quantityOrdered * priceEach)  as totalsales
    , (sum(quantityOrdered * priceEach))/count(distinct od.ordernumber) as meanOrderSales
from customers ct
right join orders od using(customernumber)
right join orderdetails odd using(orderNumber)
group by 1,2
order by 1,2
;

-- CASE WHEN: IF-ELSE 조건문

SELECT 
	ordernumber
    , quantityOrdered
    , Case when quantityordered > 30 then "30 OVER"
		   when quantityordered  = 30 then "Just 30"
           else "Less than 30"
	   END as 조건문
from orderdetails
;

--

SELECT 
     Case when ct.country in ('USA', 'Canada') then "North America"
           else "Rest of the world" END as region
	, count(distinct od.ordernumber) as numOrder
    , sum(quantityOrdered * priceEach)  as totalsales
    , (sum(quantityOrdered * priceEach))/count(distinct od.ordernumber) as meanOrderSales
from customers ct
right join orders od using(customernumber)
right join orderdetails odd using(orderNumber)
group by 1
order by 1
;

select Distinct country from customers;

