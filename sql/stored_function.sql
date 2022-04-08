CREATE FUNCTION transformed_time(arg INTEGER) RETURNS VARCHAR(5) AS $$ 
BEGIN
	IF arg < 10 THEN
		RETURN concat('00.0',CAST(arg as VARCHAR(4)));
    	ELSIF arg BETWEEN 10 AND 59 THEN
		RETURN concat('00.',CAST(arg as VARCHAR(4)));
	ELSIF arg BETWEEN 100 AND 959 THEN
		RETURN concat('0',substring(CAST(arg as VARCHAR(4)) from 1 for 1),'.',substring(CAST(arg as VARCHAR(4)) from 2 for 2));
	ELSE 
		RETURN concat(substring(CAST(arg as VARCHAR(4)) from 1 for 2),'.',substring(CAST(arg as VARCHAR(4)) from 3 for 2));
	END IF;
END; $$ LANGUAGE plpgsql;
