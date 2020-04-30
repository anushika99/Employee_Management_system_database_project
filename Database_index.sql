CREATE INDEX client_userID_indx on Client_UserID(id); /*Index for finding client id in Client_UserId table*/
CREATE INDEX client_project_indx on clients_project(id); /*Index for finding client id in Client_project table*/
CREATE INDEX tasks_info_id_indx on tasks_info(id); /*Index for finding task information by task id in tasks_info table*/
CREATE INDEX tasks_info_id_status_indx on tasks_info(id, status); /* Index on status and id in tasks_info table*/
CREATE INDEX employee_info_id_indx on employee_personal_info(employee_id); /*Index for finding employee information by employee id in employee_personal_info table*/
CREATE INDEX dept_name_indx on department(name); /* creating index on department name in department table*/
CREATE INDEX addr_id_indx on address(id);  /* creating index on address id in address table*/
CREATE INDEX client_id_indx on clients(id); /* creating index on client id in clients table*/
CREATE INDEX caller_id_indx on meetings(caller_id); /* creating index on caller id in meetings table*/
CREATE INDEX attende_id_indx on meetings_employee(employee_id); /* creating index on employee id in meetings_employee table*/
CREATE INDEX employee_userID_indx on Employee_UserID(id); /*Index for finding Employee id in Employee_UserId table*/
CREATE INDEX leave_employee_id_indx on leave_request(employee_id); /* Index for employee id in leave_request table*/
CREATE INDEX leave_manager_id_indx on leave_request(manager_id); /* Index for manager id in leave_request table*/
CREATE INDEX meeting_id_indx on Meetings(id); /* Index for meeting id in Meetings table*/
CREATE INDEX meeting_employee_id_indx on Meetings_employee(id); /* Index for meeting id in Meetings Employee table*/
CREATE INDEX tasks_employee_task_indx on tasks_employee(id); /* Index for task id in Tasks Employee table*/
CREATE INDEX tasks_employee_id_indx on tasks_employee(employee_id); /* Index for employee id in Tasks Employee table*/
CREATE INDEX employee_performance_id_indx on Employee_Performance(id); /*Index for employee id in employee performance table*/
CREATE INDEX employee_dept_id_indx on employee_personal_info(dept_id); /* Index for department id in employee personal info table*/
CREATE INDEX employee_dept_employee_id_indx on employee_personal_info(dept_id, employee_id); /* Index on employee id and department id in employee personal info table*/
