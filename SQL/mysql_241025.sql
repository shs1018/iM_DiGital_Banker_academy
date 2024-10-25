use dataset_2;

-- 성별에 따른 승객수와 생존자수 구하시오
-- 칼럼 -> 0 사망, 1생존

select * from titanic;

-- 출력값

select 
	Sex,
	count(DISTINCT passengerId) AS ID,
    sum(Survived) AS survNum,
    round(sum(Survived)/count(DISTINCT passengerId) * 100, 2)as ratio
from titanic
group by Sex
;

--
-- 연령에 따른 생존율 알아보기
-- SQL에서 연령대로 범주화 시키자
-- 0~ 10대 -> 0대, 10~19 -> 10대...

select 
	FLOOR(AGE/10) * 10 AS AGEBAND,
    count(DISTINCT passengerId) AS onBoard,
    sum(Survived) as survNum,
    ROUND(sum(Survived) / count(DISTINCT passengerId) * 100 , 2) as ratio
from 
	titanic
group by 
	1
order by 
	1
;

-- 더해보자

select 
	FLOOR(AGE/10) * 10 AS AGEBAND,
    Sex,
    count(DISTINCT passengerId) AS onBoard,
    sum(Survived) as survNum,
    ROUND(sum(Survived) / count(DISTINCT passengerId) * 100 , 2) as ratio
from 
	titanic
group by 
	1,2
order by 
	2,1
;

--

select 
	AGEBAND,
    man_plot.ratio as manSurv,
    woman_plot.ratio as womanSurv,
	round(woman_plot.ratio - man_plot.ratio, 2) as survDIff
from
(
select 
	FLOOR(AGE/10) * 10 AS AGEBAND,
    Sex,
    count(DISTINCT passengerId) AS onBoard,
    sum(Survived) as survNum,
    ROUND(sum(Survived) / count(DISTINCT passengerId) * 100 , 2) as ratio
from 
	titanic
group by 
	1,2
HAVING 
	sex = 'male'
) 
	as man_plot
left join 
(
select 
	FLOOR(AGE/10) * 10 AS AGEBAND,
    Sex,
    count(DISTINCT passengerId) AS onBoard,
    sum(Survived) as survNum,
    ROUND(sum(Survived) / count(DISTINCT passengerId) * 100 , 2) as ratio
from 
	titanic
group by 
	1,2
HAVING 
	sex = 'female'
) 
	as woman_plot
USING(AGEBAND)
;
--
-- 타이타닉 이외의 해상사고에서는 선장과 승무원의 생존율이 가장 높았음
-- 해상 승무원들의 책임감 재고

-- 등급별로 생존율 및 차이는?

SELECT 
    pclass AS cabinClass,
    Sex,
    FLOOR(AGE/10) * 10 AS AGEBAND,
    COUNT(passengerId) AS onBoard,
    SUM(Survived) AS survNum,
    ROUND(SUM(Survived) / COUNT(passengerId) * 100, 2) AS ratio
FROM 
    titanic
GROUP BY 
    pclass, Sex, 3
ORDER BY 
    Sex, pclass
;

--
-- 탑승객 분석
-- 출발지, 도착지별 승객 수

select
	Boarded,
    Destination,
    count(passengerID)
from titanic
group by 1,2
order by 3 DESC
;

-- 
-- 상위 5개 경로를 추출할 때, 탑승객 수로 순위를 매기기

select
	Boarded,
    Destination,
    count(passengerID) as passengerNum,
    ROUND(SUM(Survived) / COUNT(passengerId) * 100, 2) AS ratio,
    ROW_NUMBER() OVER (ORDER BY count(passengerID) DESC) As RNK
from titanic 
group by 1,2
order by 3 DESC LIMIT 5
;

--

SELECT * 
FROM (
    SELECT 
        *
        , ROW_NUMBER() OVER(ORDER BY N_PASSENGERS DESC) RNK
    FROM (
            SELECT 
                BOARDED
                , DESTINATION
                , COUNT(PASSENGERID) N_PASSENGERS
            FROM titanic
            GROUP BY BOARDED, DESTINATION
    ) BASE
) BASE
WHERE RNK BETWEEN 1 AND 5
;

--
-- HOmetown 별 탑승객 수 생존율

Select *
from 
(select HomeTown from titanic) A
left join 
(select HOMETOWN, ROUND(SUM(Survived) / COUNT(passengerId) * 100, 2) AS ratio from titanic GROUP BY HOMETOWN) B
USING(HOMETOWN)
;
-- OR..
-- SUM(1)은 테이블의 행의 갯수를 구한다.

SELECT 
	HOMETOWN,
    sum(1) as passengerNum, -- 승객수
    round(sum(Survived) / sum(1),2) as survRate
from titanic
Group by HOMETOWN
HAVING passengerNum > 10 AND survRate > 0.5
;

--
-- 정규표현식
-- 데이터 생성

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20)
);

-- 샘플 데이터 삽입

INSERT INTO users (username, email, phone) VALUES
('john.doe', 'john.doe@example.com', '123-456-7890'),
('jane_smith', 'jane.smith@example.net', '555-1234'),
('alice99', 'alice123@wonderland.com', '987-654-3210'),
('bob-builder', 'bob.builder@construction.org', '321-654-0987'),
('charlie.brown', 'charlie.brown@example.com', '555-9876');

-- 내용:
-- 문자와 기호:
-- .: 임의의 단일 문자
-- ^: 문자열의 시작
-- $: 문자열의 끝
-- *: 0개 이상의 반복
-- +: 1개 이상의 반복
-- ?: 0개 또는 1개의 반복
-- |: 논리적 OR
-- []: 범위 또는 문자 클래스
-- (): 그룹화

select * from users;

-- 1. 임의의 단일 문자.
-- 문제 : username칼럼에서 임의의 한 문자 t가 있는 행만 추출하도록 하자.

select * from users where username REGEXP '.t';

-- ja로 시작하는 이름을 찾는 쿼리

select * from users where username REGEXP '^ja';

-- m으로 끝나는 이메일을 찾는 쿼리

select * from users where email regexp 'm$';

-- * : 0개 이상의 반복

select * from users where username regexp 'do.*';

-- + : 1개 이상의 반복
-- 0을 하나 이상 포함하는 이메일 찾기`

select * from users where PHONE regexp '[0]+';

-- a부터 e까지의 알파벳으로 시작하는 이름을 가진 새럼
select * from users where username regexp '^[a-e]';

-- 리뷰 데이터
ALTER TABLE dataset2 
RENAME COLUMN `癤풠lothing ID` TO `CLOTHING ID`;

select * from dataset2;

select `Review Text` from dataset2 where `Review Text` regexp '.hate';

-- 문제: Department 별 평균 평점 구하기
-- DIVISION NAME별 평균 평점 구하기!!

select 
	`DIVISION NAME`, 
    AVG(Rating) as avg
from dataset2 
group by `DIVISION NAME`
order by 2 DESC
; 

select 
	`DEPARTMENT NAME`, 
    AVG(Rating) as avg
from dataset2 
group by `DEPARTMENT NAME`
order by 2 DESC
; 

-- TREND 의 평점 3점 이하 출력

select 
	*
from dataset2 
where `DEPARTMENT NAME` = 'TREND'
	and rating <= 3
; 

-- 위 sql에서 연령대깔즤

select 
	FLOOR(AGE/10) * 10 as generation,
    AVG(rating) as AVGR,
    count(*) as customerNum
from dataset2 
where `DEPARTMENT NAME` = 'TREND'
	and rating <= 3
group by 1
order by 3 DESC
; 

-- DEPARTMENT 별 연령별 리뷰 수

select 
	FLOOR(AGE/10) * 10 as generation,
    AVG(rating) as AVGR,
    count(*) as customerNum
from dataset2 
where `DEPARTMENT NAME` = 'TREND'
group by 1
order by 1
; 

-- 50대, 3점이하 TREND만 조사해보자.

select
	title,
    `review text`
from dataset2
where `Department name` = 'trend'
	and rating <= 3
	and age between 50 and 59
;

-- 집계 TRUE / FALSE 로 구분하기

select
    `review text`,
    case when `review text` Like '%size%' then 1 else 0
    end Size_YN
from dataset2
;

-- 전체 리뷰 개수 중에서 SIZE에 관한 리뷰는 대략적으로 몇 %인가?

select sum(case when `review text` Like '%size%' then 1 else 0
    end) / sum(1) as sizeReview
from dataset2;

-- 더 세부적으로 들어가보자.

select sum(case when `review text` Like '%size%' then 1 else 0
    end)/ sum(1) as sizeReview,
    sum(case when `review text` Like '%Large%' then 1 else 0
    end)/ sum(1) as largeReview,
    sum(case when `review text` Like '%small%' then 1 else 0
    end)/ sum(1) as smallReview,
    sum(case when `review text` Like '%tight%' then 1 else 0
    end)/ sum(1) as tightReview,
    sum(case when `review text` Like '%loose%' then 1 else 0
    end)/ sum(1) as looseReview,
    sum(case when `review text` Like '%mission%' then 1 else 0
    end)/ sum(1) as missionReview,
    sum(case when `review text` Like '%reward%' then 1 else 0
    end)/ sum(1) as rewardReview,
    sum(1) as totalReview
from dataset2
;

-- department name별로, 연령대별로 집계
-- 각각의 비율을 구할 수 있음
-- sum(case when ~) / sum(1)

select `department name`,
	sum(case when `review text` Like '%size%' then 1 else 0
    end)/ sum(1) as sizeReview,
    sum(case when `review text` Like '%Large%' then 1 else 0
    end)/ sum(1) as largeReview,
    sum(case when `review text` Like '%small%' then 1 else 0
    end)/ sum(1) as smallReview,
    sum(case when `review text` Like '%tight%' then 1 else 0
    end)/ sum(1) as tightReview,
    sum(case when `review text` Like '%loose%' then 1 else 0
    end)/ sum(1) as looseReview,
    sum(case when `review text` Like '%mission%' then 1 else 0
    end)/ sum(1) as missionReview,
    sum(case when `review text` Like '%reward%' then 1 else 0
    end)/ sum(1) as rewardReview,
    sum(1) as totalReview
from dataset2
group by `Department name`
;

select floor(age/10) * 10 as ages,
	sum(case when `review text` Like '%size%' then 1 else 0
    end)/ sum(1) as sizeReview,
    sum(case when `review text` Like '%Large%' then 1 else 0
    end)/ sum(1) as largeReview,
    sum(case when `review text` Like '%small%' then 1 else 0
    end)/ sum(1) as smallReview,
    sum(case when `review text` Like '%tight%' then 1 else 0
    end)/ sum(1) as tightReview,
    sum(case when `review text` Like '%loose%' then 1 else 0
    end)/ sum(1) as looseReview,
    sum(case when `review text` Like '%mission%' then 1 else 0
    end)/ sum(1) as missionReview,
    sum(case when `review text` Like '%reward%' then 1 else 0
    end)/ sum(1) as rewardReview,
    sum(1) as totalReview
from dataset2
group by floor(age/10) * 10
order by 1
;

-- 최종분

select 
	`Department name`,
	floor(age/10) * 10 as ages,
	sum(case when `review text` Like '%size%' then 1 else 0
    end)/ sum(1) as sizeReview,
    sum(case when `review text` Like '%Large%' then 1 else 0
    end)/ sum(1) as largeReview,
    sum(case when `review text` Like '%small%' then 1 else 0
    end)/ sum(1) as smallReview,
    sum(case when `review text` Like '%tight%' then 1 else 0
    end)/ sum(1) as tightReview,
    sum(case when `review text` Like '%loose%' then 1 else 0
    end)/ sum(1) as looseReview,
    sum(1) as totalReview
from dataset2
group by 1,2
order by 2,1
;
