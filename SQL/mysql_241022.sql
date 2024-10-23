/*
여러줄을주
석처리해요
*/
-- 한 줄을 주석처리해요

-- sample하나 가져오기
select * from classicmodels.employees;

-- 더 범용적으로 샘플 하나 가져오기
USE classicmodels;
select * from employees;

-- SQL 기본문법
/*
SELECT 컬럼
FROM 테이븖명
WHERE 조건절
GROUP BY 범주 컬럼
HAVING 그룹바이 이후 조건절(단독사용 불가)
ORDER BY 값 정렬
*/

-- LastName만 출력하자
SELECT lastName from employees;

-- DESC
DESC employees;

-- MULTI

SELECT
	lastName
    , firstName
    , jobTitle
FROM
employees
;

-- SELECT olny without table
-- example as python: print(1+1)
-- 'AS" called as 'ALIAS"
select 
	1+1 
AS 
	COL_A
;

-- 그 외의 메서드
select rtrim('barbar   ');
select ltrim('     no THanks!') as res;

-- 날짜 구하기 함수
SELECT NOW();
SELECT CURDATE();

-- 글자 이어 붙이기
SELECT Concat('chris', '    ', "evans")AS NAME;

-- orderby: 칼럼 정렬
DESC customers;
SELECT 
 salesRepEMployeeNumber
, lastName 
, firstName
from customers
order by 
	salesRepEmployeeNumber ASC
    , contactLastNameavs
    
-- ------------------------------------

-- From => SELECT => Order-by를 순차적으롱 (FROM -> SELECT -> OrderBy)

SELECT 
 salesRepEMployeeNumber
, lastName 
, firstName
From 
	employees
Where 
	jobtitle = 'Sales Rep'
;

-- OR
SELECT 
 jobtitle
, lastName 
, firstName
, officecode
From 
	employees
WHere 
	jobtitle = 'Sales Rep' or
    officeCode = 1
;
    
-- AND

SELECT 
 jobtitle
, lastName 
, firstName
, officecode
From 
	employees
WHere 
	jobtitle = 'Sales Rep' and
    officeCode = 1
;

-- Between 

SELECT 
	firstName
    , lastName
    , officeCode
From
	employees
where 
	officeCode Between 1 and 5
;

-- LIKE: 문자 칼럼을 조회할 때 자주 사용함
-- 패턴을 조회, %, _ : wild card
-- %: any String, 위치에 상관 없음, 1개 또는 그 이상을 매칭
-- _: Single Character, 1개만 매칭

-- firstname에서 a로 시작하는 이름만 조회
select
	employeeNumber
    , lastName
    , firstName
FROM
	employees
where
	firstName Like '%a%' -- 정규표현식
;

select
	employeeNumber
    , lastName
    , firstName
FROM
	employees
where
	firstName Like '%e__' -- 정규표현식
;

select
	employeeNumber
    , lastName
    , firstName
FROM
	employees
where
	firstName NOT Like '%a%' -- 정규표현식
;

-- LIKE ESCAPE 

-- IN 연산자
-- 칼럼명 IN (값1, 값2, 값3)

SELECT
	firstName
    , lastName
    , officeCode
From
	employees
where
	officeCode in (1,2,3)
;

SELECT
	firstName
    , lastName
    , officeCode
From
	employees
where
	officeCode = 1 or 
    officeCode = 2 or
    officeCode = 3
;

SELECT
	firstName
    , lastName
    , officeCode
From
	employees
where
	officeCode != 4 AND
    officeCode != 5 AND
    officeCode != 6 AND
    officeCode != 7
;

-- 

SELECT
	employeeNumber
	, firstName
    , lastName
    , reportsTo
From
	employees
where
	reportsTo IS NULL
;

--
SELECT
	lastname
    , firstname
    , jobtitle
from
	employees
where 
	jobtitle = 'Sales Rep' -- !=, <> , Not Equal.
;

-- DISTINCT ==> Select 다음에 온다! 중복되는 것을 방지할 때 자주 쓰인다.
select
	distinct lastname
from
	employees
order by 
	lastname
;

-- DISTINCT & NULL 값 사용

select
	distinct state
from
	customers
;

-- state, city 조회
-- table: customers

select
	state
    , city
from 
	customers
where
	state IS NOT NULL
group by 
	state
    , city
;

-- 집계함수
select
	productLine,
	AVG(buyPrice)
from
	products
group by
	productLine
order by 
	AVG(buyPrice) DESC
;