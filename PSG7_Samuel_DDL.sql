create table table_g7(
id serial primary key,
"Timestamp" date,
"Choose your gender" varchar(50),
"Age" int,
"What is your course?" varchar(50),
"Your current year of Study" varchar(50),
"What is your CGPA?" varchar(50),
"Marital status" varchar(50),
"Do you have Depression?" bool,
"Do you have Anxiety?" bool,
"Do you have Panic attack?" bool,
"Did you seek any specialist for a treatment?" bool);

copy table_g7("Timestamp", "Choose your gender", "Age", "What is your course?", "Your current year of Study", "What is your CGPA?", "Marital status",
             "Do you have Depression?", "Do you have Anxiety?", "Do you have Panic attack?", "Did you seek any specialist for a treatment?")
FROM 'C:\tmp\P2G7_Samuel_data_raw.csv'
DELIMITER ','
CSV HEADER;

select * from table_g7