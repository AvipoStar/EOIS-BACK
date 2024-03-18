TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`localhost` TRIGGER trg_insert_userevent \n    AFTER INSERT \n    ON event \n    FOR EACH ROW \nBEGIN \n    DECLARE balance DECIMAL(10, 2); \n    IF NEW.event_type_id = 1 THEN \n        SET balance = COALESCE((SELECT current_balance FROM userevent WHERE user_id = NEW.target_user_id ORDER BY id DESC LIMIT 1), 0); \n        SET balance = balance - NEW.amount; \n    ELSEIF NEW.event_type_id = 2 THEN \n        SET balance = COALESCE((SELECT current_balance FROM userevent WHERE user_id = NEW.target_user_id ORDER BY id DESC LIMIT 1), 0); \n        SET balance = balance + NEW.amount; \n    END IF; \n    INSERT INTO userevent (user_id, event_id, current_balance) VALUES (NEW.target_user_id, NEW.id_event, balance); \nEND'
sql_modes=1436549152
definers='root@localhost'
client_cs_names='utf8'
connection_cl_names='utf8_general_ci'
db_cl_names='utf8mb4_general_ci'
created=170953722229
