# NorthStar Urban Mobility Analytics Project

## Overview
This project analyses operational inefficiencies in NorthStar Urban Mobility using a combination of SQL, R, Python, and MongoDB.

## Technologies Used
- Python (data cleaning and feature engineering)
- SQL (relational data analysis via R)
- R (analytics and visualization)
- MongoDB (NoSQL database design and querying)

## Key Features
- Integrated structured and semi-structured data
- Delivery delay analysis
- Customer complaint correlation
- Cost and efficiency analysis
- NoSQL document-based modeling using MongoDB

## Project Structure
- notebooks/ → data processing and analysis
- mongodb/ → database scripts
- data/ → cleaned dataset

## Key Insights
- Delays strongly linked to route overrides and poor planning
- Customer complaints are correlated with delayed deliveries
- Certain zones show high cost inefficiency

## MongoDB Design
A document-based model was used to integrate:
- deliveries
- complaints
- incidents
- app events

This allowed flexible querying of operational cases.

