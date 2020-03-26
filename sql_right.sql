CREATE USER 'yy_jimmy'@'127.0.0.1' IDENTIFIED BY 'yyjimmy';
GRANT ALL PRIVILEGES ON yyostech.* TO 'yy_jimmy'@'127.0.0.1';
FLUSH PRIVILEGES;

CREATE USER 'yy_raspi'@'192.168.0.30' IDENTIFIED BY 'yyraspi';
GRANT ALL PRIVILEGES ON yyostech.* TO 'yy_raspi'@'192.168.0.30';
FLUSH PRIVILEGES;

select * from yyostech.series_data;