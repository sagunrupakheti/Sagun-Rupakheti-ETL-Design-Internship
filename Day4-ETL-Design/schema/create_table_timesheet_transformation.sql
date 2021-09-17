CREATE TABLE transform_timesheet(
    employee_id  VARCHAR(255),
    department_Id VARCHAR(255),
    shift_start_time TIMESTAMP,
    shift_end_time TIMESTAMP,
    shift_date DATE,
    shift_type VARCHAR(255),
    hours_worked FLOAT,
    attendance bool,
    has_taken_break bool,
    break_hour FLOAT,
    was_charge bool,
    charge_hour FLOAT,
    was_on_call bool,
    on_call_hour FLOAT,
    num_teammates_absent INT
)