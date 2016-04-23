
--database

drop database safelocality;
create database safelocality;

use safelocality;

--User table

CREATE TABLE `User` (
`UserId` BIGINT NULL AUTO_INCREMENT,
`UserName` VARCHAR(255) NULL,
`FirstName` VARCHAR(255) NULL,
`LastName` VARCHAR(255) NULL,
`Useremail` VARCHAR(255) NULL,
`UserPassword` VARCHAR(255) NULL,
PRIMARY KEY (`UserId`));

--select database


--User storedprocedure

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(255),
    IN p_firstname VARCHAR(255),
    IN p_lastname   VARCHAR(255), 
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(255)
)
BEGIN
    if ( select exists (select 1 from User where Useremail = p_email) ) THEN

        select 'User Exists !!';

    ELSE

        insert into User
        (
            UserName,
            FirstName,
            LastName,
            Useremail,
            UserPassword
        )
        values
        (
            p_name,
            p_firstname,
            p_lastname,
            p_email,
            p_password
        );

    END IF;
END$$
DELIMITER ;

--Validate Sign in
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
IN p_useremail VARCHAR(255)
)
BEGIN
    select * from User where Useremail = p_useremail;
END$$
DELIMITER ;
