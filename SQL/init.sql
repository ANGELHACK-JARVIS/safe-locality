
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
DELIMITER;

--Coordinates Table

CREATE TABLE Coordinates(
    Loc_id BIGINT NULL AUTO_INCREMENT,
    Loc_name VARCHAR(255),
    Loc_lat Float,
    Loc_long Float,
    PRIMARY KEY (`Loc_id`)
);

CREATE TABLE LifeStyle(
    UserId BIGINT NULL,
    Loc_id BIGINT NULL,
    Water INT NULL,
    Electricity  INT NULL,
    Network_Availability  INT NULL,
    Cleanliness  INT NULL,
    Green_space  INT NULL,
    Local_Entertainment  INT NULL,
    NightLife INT NULL,
    Repairmen_avail  INT NULL,
    Education  INT NULL,
    Neighbourhood INT NULL,
    PRIMARY KEY(`UserId`),
    FOREIGN KEY(UserId) REFERENCES User(UserId),
    FOREIGN KEY(Loc_id) REFERENCES Coordinates(Loc_id)
);

CREATE TABLE Security(
    UserId BIGINT NULL,
    Loc_id BIGINT NULL,
    Theft BIGINT NULL,
    Violence BIGINT NULL,
    Harassment BIGINT NULL,
    PRIMARY KEY(`UserId`),
    FOREIGN KEY(UserId) REFERENCES User(UserId),
    FOREIGN KEY(Loc_id) REFERENCES Coordinates(Loc_id)  
);