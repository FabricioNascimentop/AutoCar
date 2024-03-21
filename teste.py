carros_db = """id	int	NO	PRI		auto_increment
nome	varchar(60)	NO			
modelo	varchar(60)	NO			
preco	decimal(10,2)	NO			
registro	date	NO			
combustivel	enum('gasolina','etanol','diesel','biodiesel','GNV','eletricidade','hibrido','flex')	NO			
motor	varchar(20)	NO			
transmissao	enum('automática','manual','automatizada')	NO			
origem	varchar(40)	NO			
Co2	smallint	NO			
estado	enum('usado','novo')	NO			
quilometros	mediumint	NO			
garantia	varchar(40)	NO			
tipo	varchar(30)	NO			
portas	tinyint	NO			
cor	varchar(30)	NO			
lugares	tinyint	NO	"""
carros_casa = """id	int(11)	NO	PRI		auto_increment
nome	varchar(60)	NO			
modelo	varchar(60)	NO			
preco	decimal(10,2)	NO			
registro	date	NO			
combustivel	enum('gasolina','etanol','diesel','biodiesel','GNV','eletricidade','hibrido','flex')	YES			
motor	varchar(20)	NO			
transmissao	enum('automática','manual','automatizada')	NO			
origem	varchar(40)	NO			
Co2	smallint(6)	NO			
estado	enum('usado','novo')	NO			
quilometros	mediumint(9)	NO			
garantia	varchar(40)	NO			
tipo	varchar(30)	NO			
portas	tinyint(4)	NO			
cor	varchar(30)	NO			
lugares	tinyint(4)	NO"""



print(carros_db,carros_casa)