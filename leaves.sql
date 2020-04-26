create table leave_request(employee_id int, manager_id int, startDate Date, EndDate Date, Reason varchar(100) , status int, FOREIGN KEY (manager_id) REFERENCES employee_personal_info(employee_id), FOREIGN KEY (employee_id) REFERENCES employee_personal_info(employee_id));

insert into leave_request values(9, 1,  "2019-11-01",    "2020-02-01", "Family Function", 0 );