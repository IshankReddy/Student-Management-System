# Project Description: Student Management System

The Student Management System is a full-stack web application built with FastAPI for backend services, PostgreSQL with docker for database management, and HTML, CSS, and JavaScript for the frontend. This application provides an intuitive interface to manage student records, offering CRUD (Create, Read, Update, Delete) functionalities with real-time data updates and responsive design. The project is designed for ease of use and scalability, enabling educational institutions or developers to handle student data effectively.

# How to run?

docker pull postgres

docker run --name my_postgres -e POSTGRES_USER-my_postgres -e POSTGRES_PASSWORD=ishank123 - e POSTGRES_DB=FullStackProjectDb -p 5432:5432 -d postgres

Table Schema: Find in db/schema.sql (fake)