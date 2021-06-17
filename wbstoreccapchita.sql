USE MASTER
GO

DROP DATABASE IF EXISTS DBCcaphita

CREATE DATABASE DBCcaphita
GO

USE DBCcaphita
GO

If OBJECT_ID('Usuarios','U') is not null
	Drop table  Usuarios
Go

Create table Usuarios(
	personid int IDENTITY(1,1) PRIMARY KEY,
	username varchar(30) not null,
	pass varchar(30) not null,
	email varchar(50) not null,
	distrito varchar(50),
	direccion varchar(150),
	fechanacimiento date,
	nCIP varchar(11),
	tipo varchar(1) not null, --1 si es persona, 2 si es institucion
)
Go

If OBJECT_ID('Carrito','U') is not null
	Drop table  Carrito
Go

Create table Carrito(
	personid int not null,
	numproductos int,
	idproductos varchar(100),
	idcarrito int IDENTITY(1,1) PRIMARY KEY,
	foreign key (personid) references Usuarios(personid)
)
Go

If OBJECT_ID('producto','U') is not null
	Drop table  producto
Go

Create table producto(
	idproducto int PRIMARY KEY not null,
	nombreproducto varchar(50) not null,
	descripcion varchar(100) not null,
	categoria varchar(50) not null,
	material varchar(50) not null,
	precio float not null,
	stock int,
	talla varchar(80)
)
Go

If OBJECT_ID('pedido','U') is not null
	Drop table  pedido
Go

Create table pedido(
	idpedido int IDENTITY(1,1) PRIMARY KEY,
	personid int not null,
	fechapedido date,
	canttotalproductos int,
	foreign key (personid) references Usuarios(personid)
)
Go

If OBJECT_ID('detallepedido','U') is not null
	Drop table  detallepedido
Go
select * from producto
Create table detallepedido(
	iddetallepedido int IDENTITY(1,1) PRIMARY KEY,
	idpedido int not null,
	idproducto int not null,
	cantidad int,
	foreign key (idpedido) references pedido(idpedido),
	foreign key (idproducto) references producto(idproducto)
)
Go

If OBJECT_ID('pago','U') is not null
	Drop table  pago
Go

Create table pago(
	idpago int IDENTITY(1,1) PRIMARY KEY,
	idpedido int not null,
	monto float,
	fechapago date,
	direccionfact varchar(150) not null,
	tipopago varchar(15) not null,
	foreign key (idpedido) references pedido(idpedido)
)
Go

If OBJECT_ID('boleta','U') is not null
	Drop table  boleta
Go

Create table boleta(
	idboleta int identity(1,1) primary key,
	productos int not null,
	fechaboleta date,
	ruc varchar(11),
	idpago int,
	foreign key (idpago) references pago(idpago),
)
Go

If OBJECT_ID('cantidadventas','U') is not null
	Drop table  cantidadventas
Go

Create table cantidadventas(
	idproducto int,
	cantidadcomprada int,
	fechaultimacompra date
)
Go
select * from boleta