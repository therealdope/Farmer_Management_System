use wrms;

create table owner(
    Owner_id int(4)  not null primary key auto_increment, 
    O_Name varchar(20),
    O_Contact varchar(22),
    No_of_godown int(5)
);

create table Godown(
    Godown_id int(4)  not null primary key auto_increment,
    G_city varchar(15),
    G_state varchar(15),
    capacity int(22),
    G_type varchar(22),
    Owner_id int(4) references owner (Owner_id)
);

create table employee(
    Employee_id int(4) not null primary key auto_increment,
    E_Name varchar(20),
    E_Contact varchar(22),
    Salary int(15),
    joining_date date,
    Working_Godown int(4)  references Godown(Godown_id)
);

create table Farmer(
    Farmer_id int(4) not null primary key auto_increment,
    F_Name varchar(20),
    F_Contact varchar(22),
    F_City varchar(15),
    F_state varchar(15)
);

create table Product(
    Product_id int(4) not null primary key auto_increment,
    P_Name varchar(20),
    P_type varchar(22),
    quantity int(10),
    producer int(4)  references Farmer(Farmer_id)
);

create table Booking(
    Booking_id int(4) not null primary key auto_increment,
    Product_id int(4) references  product(Product_id),
    Godown_id int(4) references  Godown(Godown_id)
);
