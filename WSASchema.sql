DROP TABLE IF EXISTS TestEvent CASCADE;
DROP TABLE IF EXISTS TestStatus CASCADE;
DROP TABLE IF EXISTS Employee CASCADE;
DROP TABLE IF EXISTS Aircraft CASCADE;

CREATE TABLE Aircraft
(
	RegNo			VARCHAR(8)		PRIMARY KEY,
	Model			VARCHAR(12)		NOT NULL,
	AirlineOwner	VARCHAR(20)		NOT NULL
);

INSERT INTO Aircraft VALUES ('AC-ACAB','A321-200'  ,'Air Canada');
INSERT INTO Aircraft VALUES ('CA-CCAD','B747-400'  ,'Air China');
INSERT INTO Aircraft VALUES ('BA-EUPG','A319-100'  ,'British Airways');
INSERT INTO Aircraft VALUES ('JA-BNAS','A330-300'  ,'Japan Airlines');
INSERT INTO Aircraft VALUES ('KE-KALA','B777-200ER','Korean Air');
INSERT INTO Aircraft VALUES ('QF-APAC','A330-300'  ,'Qantas Airways');
INSERT INTO Aircraft VALUES ('SQ-CSEA','A380-800'  ,'Singapore Airlines');
INSERT INTO Aircraft VALUES ('TG-THAI','B777-300ER','Thai Airways');

CREATE TABLE Employee
(
	UserID			SERIAL			PRIMARY KEY,
	UserName		VARCHAR(20)		NOT NULL UNIQUE,
	Name			VARCHAR(100)	NOT NULL,
	Password		VARCHAR(20)		NOT NULL,
	Email			VARCHAR(50)     NOT NULL,
	Role			VARCHAR(20)		CHECK (Role in ('Technician','TestEngineer'))
);

INSERT INTO Employee (UserName,Name,Password,Email,Role) VALUES ('jkoi'		,'Jerry Koi'	,'000','jkoi@wsa.com.au'	,'Technician');		-- 1
INSERT INTO Employee (UserName,Name,Password,Email,Role) VALUES ('jaddison'	,'Jo Addison'	,'111','jaddison@wsa.com.au','Technician');		-- 2
INSERT INTO Employee (UserName,Name,Password,Email,Role) VALUES ('kagena'	,'Keiko Agena'	,'222','kagena@wsa.com.au'	,'Technician');		-- 3
INSERT INTO Employee (UserName,Name,Password,Email,Role) VALUES ('sali'		,'Spiroz Ali'	,'333','sali@wsa.com.au'	,'Technician');		-- 4
INSERT INTO Employee (UserName,Name,Password,Email,Role) VALUES ('sallen'	,'Steve Allen'	,'444','sallen@wsa.com.au'	,'Technician');		-- 5
INSERT INTO Employee (UserName,Name,Password,Email,Role) VALUES ('famaro'	,'Fiona Amaro'	,'555','famaro@wsa.com.au'	,'Technician');		-- 6
INSERT INTO Employee (UserName,Name,Password,Email,Role) VALUES ('abailey'	,'Alan Bailey'	,'666','abailey@wsa.com.au'	,'TestEngineer');	-- 7
INSERT INTO Employee (UserName,Name,Password,Email,Role) VALUES ('cburr'	,'Carol Burr'	,'777','cburr@wsa.com.au'	,'TestEngineer');	-- 8
INSERT INTO Employee (UserName,Name,Password,Email,Role) VALUES ('acarey'	,'Adam Carey'	,'888','acarey@wsa.com.au'	,'TestEngineer');	-- 9
INSERT INTO Employee (UserName,Name,Password,Email,Role) VALUES ('cchapman'	,'Colin Chapman','999','cchapman@wsa.com.au','TestEngineer');	-- 10

CREATE TABLE TestStatus
(
	TestStatusCode	VARCHAR(10)		PRIMARY KEY,
	TestStatusDesc	VARCHAR(30)		NOT NULL UNIQUE
);

INSERT INTO TestStatus (TestStatusCode,TestStatusDesc) VALUES ('TODO'  ,'Test to be performed');		-- 1
INSERT INTO TestStatus (TestStatusCode,TestStatusDesc) VALUES ('INPROG','Test in progress');			-- 2
INSERT INTO TestStatus (TestStatusCode,TestStatusDesc) VALUES ('PASS'  ,'Test completed and passed');	-- 3
INSERT INTO TestStatus (TestStatusCode,TestStatusDesc) VALUES ('FAIL'  ,'Test completed and failed');	-- 4

CREATE TABLE TestEvent
(
	TestID			SERIAL 			PRIMARY KEY,
	TestDate		DATE			NOT NULL,
	RegNo			VARCHAR(8)		NOT NULL,
	Status			VARCHAR(10)		NOT NULL REFERENCES TestStatus,
	Technician		INTEGER 		NOT NULL REFERENCES Employee,
	TestEngineer	INTEGER	 		NOT NULL REFERENCES Employee
);

INSERT INTO TestEvent (TestDate,RegNo,Status,Technician,TestEngineer) VALUES ('19/01/2022','BA-EUPG','INPROG',4,7);	-- 1
INSERT INTO TestEvent (TestDate,RegNo,Status,Technician,TestEngineer) VALUES ('17/03/2022','KE-KALA','TODO'  ,2,7);	-- 2
INSERT INTO TestEvent (TestDate,RegNo,Status,Technician,TestEngineer) VALUES ('26/02/2022','QF-APAC','FAIL'  ,5,9);	-- 3
INSERT INTO TestEvent (TestDate,RegNo,Status,Technician,TestEngineer) VALUES ('02/03/2022','AC-ACAB','PASS'  ,3,7);	-- 4
INSERT INTO TestEvent (TestDate,RegNo,Status,Technician,TestEngineer) VALUES ('02/03/2022','TG-THAI','INPROG',3,10);-- 5
INSERT INTO TestEvent (TestDate,RegNo,Status,Technician,TestEngineer) VALUES ('10/03/2022','SQ-CSEA','INPROG',2,8);	-- 6
INSERT INTO TestEvent (TestDate,RegNo,Status,Technician,TestEngineer) VALUES ('25/01/2022','BA-EUPG','TODO'  ,2,8);	-- 7

COMMIT;


create or replace function update_event(test_date date, regno varchar, status varchar, test_id int, technician varchar, testengineer varchar)
returns void as $$
begin
        UPDATE testevent t1 SET testdate=Date($1), regno=$2, status = t2.teststatuscode, technician = t3.userid, testengineer = t4.userid 
		FROM teststatus t2,employee t3,employee t4 
		WHERE t2.teststatusdesc=$3  and t1.testid=$4 and t3.username=$5 and t4.username = $6;
end;
$$ language plpgsql;

create or replace function addEvent(td date, rg varchar, st varchar, te int, ten int) 
returns void 
AS $$
begin
		INSERT INTO TestEvent (TestDate,RegNo,Status,Technician,TestEngineer) VALUES (td,rg,st,te,ten);
end
$$language plpgsql;