# Farmer Management System (FRMS)

## Overview
The Farmer Management System (WRMS) is designed to efficiently manage warehouse operations by tracking owners, godowns (warehouses), employees, farmers, products, and bookings. The system ensures smooth workflow for booking products, managing inventory, and tracking ownership of godowns and products.

## Database Schema

1. **Owner Table (`owner`)**
   - `Owner_id`: Primary key, auto-incremented.
   - `O_Name`: Owner's name (up to 20 characters).
   - `O_Contact`: Owner's contact information (up to 22 characters).
   - `No_of_godown`: Number of godowns owned by the owner.

2. **Godown Table (`godown`)**
   - `Godown_id`: Primary key, auto-incremented.
   - `G_city`: City where the godown is located (up to 15 characters).
   - `G_state`: State where the godown is located (up to 15 characters).
   - `Capacity`: Capacity of the godown (up to 22 digits).
   - `G_type`: Type of the godown (up to 22 characters).
   - `Owner_id`: Foreign key referencing `owner(Owner_id)`.

3. **Employee Table (`employee`)**
   - `Employee_id`: Primary key, auto-incremented.
   - `E_Name`: Employee's name (up to 20 characters).
   - `E_Contact`: Employee's contact information (up to 22 characters).
   - `Salary`: Employee's salary (up to 15 digits).
   - `Joining_date`: Date the employee joined.
   - `Working_Godown`: Foreign key referencing `godown(Godown_id)`.

4. **Farmer Table (`farmer`)**
   - `Farmer_id`: Primary key, auto-incremented.
   - `F_Name`: Farmer's name (up to 20 characters).
   - `F_Contact`: Farmer's contact information (up to 22 characters).
   - `F_City`: City where the farmer resides (up to 15 characters).
   - `F_state`: State where the farmer resides (up to 15 characters).

5. **Product Table (`product`)**
   - `Product_id`: Primary key, auto-incremented.
   - `P_Name`: Product's name (up to 20 characters).
   - `P_type`: Type of product (up to 22 characters).
   - `Quantity`: Quantity of the product (up to 10 digits).
   - `Producer`: Foreign key referencing `farmer(Farmer_id)`.

6. **Booking Table (`booking`)**
   - `Booking_id`: Primary key, auto-incremented.
   - `Product_id`: Foreign key referencing `product(Product_id)`.
   - `Godown_id`: Foreign key referencing `godown(Godown_id)`.

## Installation
1. Clone the repository:
   ```bash
   git clone [<repository_url>](https://github.com/therealdope/Farmer_Management_System/edit/main/README.md)
2. Install required dependencies (if applicable).

## Usage
1. Set up the database using the provided schema.
2. Start the server or application.
3. Interact with the WRMS via the user interface or database queries.
