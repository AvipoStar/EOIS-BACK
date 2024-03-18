TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`localhost` TRIGGER session_insert_trigger\n	AFTER INSERT\n	ON session\n	FOR EACH ROW\nBEGIN\n    DECLARE i INT DEFAULT 0;\n    WHILE i < NEW.firm_count DO\n        INSERT INTO firm (number, session_id)\n        SELECT MAX(number) + 1, NEW.id_session FROM (SELECT number FROM firm) AS temp;\n        SET i = i + 1;\n    END WHILE;\nEND'
sql_modes=1436549152
definers='root@localhost'
client_cs_names='utf8'
connection_cl_names='utf8_general_ci'
db_cl_names='utf8mb4_general_ci'
created=169854173120
