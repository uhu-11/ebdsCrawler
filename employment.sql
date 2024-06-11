drop database  if exists `employment`;
create database `employment`;
use `employment`;
drop table if exists `info`;
create  TABLE `info`
(
    `job_name` varchar(255) not null,
    `salary` varchar(255) not null,
    `comp_name` varchar(255) not null,
    `comp_type` varchar(255) not null,
    `comp_size` varchar(255) not null,
    `position` varchar(255) not null,
    `experience` varchar(255) not null,
    `degree` varchar(255) not null,
    `job_type` varchar(255) not null,
    `headcount` varchar(255) not null,
    `industry` varchar(255) not null,
    `description` varchar(255) not null
)ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;