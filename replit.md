# Overview

Dicarta Livraria is a bookstore management system with a dual-role architecture supporting both customers and technicians. The system provides a complete digital bookstore solution with inventory management, order processing, and user role-based access control. Customers can browse catalogs, manage shopping carts, and place orders, while technicians can manage book inventory, handle service orders, and oversee system operations.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The frontend is built using Flask with Jinja2 templating and Bootstrap for responsive UI. The application follows a traditional server-side rendering approach with:

- **Template Structure**: Base template with role-specific dashboards and feature pages
- **Styling**: Dark theme Bootstrap with custom CSS enhancements and Font Awesome icons
- **Client-side Logic**: Minimal JavaScript for form handling, modal interactions, and UI enhancements
- **Responsive Design**: Mobile-first approach using Bootstrap grid system

## Backend Architecture
The system implements a microservices-like architecture with clear separation between presentation and business logic:

- **Flask Application**: Serves as the presentation layer and API gateway
- **Spring Boot Backend**: Handles business logic, data persistence, and REST API endpoints (running on port 8000)
- **Session Management**: Flask sessions for user state and shopping cart persistence
- **API Communication**: RESTful communication between Flask frontend and Spring Boot backend

## Data Models
The system manages four core entities:
- **Cliente**: Customer information with personal and contact details
- **Tecnico**: Technical staff with employment details and hourly rates
- **Livro**: Book catalog with pricing, inventory, and metadata
- **OrdemDeServico**: Service orders for business operations tracking

## Authentication & Authorization
Role-based access control with two distinct user types:
- **Cliente**: Access to catalog browsing, shopping cart, and order placement
- **Tecnico**: Administrative access to inventory management and service order processing
- Session-based authentication with role persistence

## Business Logic Patterns
- **Shopping Cart**: Session-based cart management with add/remove functionality
- **Inventory Control**: Real-time stock tracking and management
- **Order Processing**: Service order lifecycle management with status tracking
- **Data Validation**: Form validation on both client and server sides

# External Dependencies

## Backend Services
- **Spring Boot Application**: Business logic and data access layer (localhost:8000)
- **PostgreSQL Database**: Primary data persistence layer
- **JPA/Hibernate**: Object-relational mapping and database operations

## Frontend Libraries
- **Bootstrap**: UI framework with dark theme support
- **Font Awesome**: Icon library for enhanced user interface
- **jQuery/JavaScript**: Client-side interactivity and form handling

## Infrastructure
- **Flask**: Python web framework for presentation layer
- **Werkzeug**: WSGI utilities and proxy handling
- **Requests**: HTTP client library for backend communication
- **Session Storage**: Flask built-in session management

## Development Tools
- **Maven**: Build automation for Spring Boot backend
- **Jinja2**: Template engine for dynamic content rendering
- **CSS3**: Custom styling and responsive design enhancements