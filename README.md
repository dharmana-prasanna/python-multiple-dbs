# Multi-Database Business Validation Tool

This tool provides a framework for connecting to multiple databases (PostgreSQL, Oracle, Teradata, and Snowflake) and performing business validations across them. The tool is designed with security in mind, using environment variables for sensitive credentials.

## Prerequisites

- Python 3.8 or higher
- Access to the following databases:
  - PostgreSQL
  - Oracle
  - Teradata
  - Snowflake
- Required database clients/drivers installed:
  - Oracle Instant Client (for cx_Oracle)
  - PostgreSQL client libraries
  - Teradata drivers
  - Snowflake connector dependencies

## Setup

1. Clone the repository and create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory using `.env.example` as a template:
```bash
cp .env.example .env
```

4. Edit the `.env` file with your database credentials:
```
# Never commit the .env file to version control
# PostgreSQL Configuration
PG_HOST=your_postgres_host
PG_DATABASE=your_database
...
```

## Usage

The tool provides two sample business validations:

1. Customer Data Validation
   - Compares customer counts across all databases for the last month
   - Ensures data consistency across systems

2. Revenue Data Validation
   - Compares daily revenue between PostgreSQL and Snowflake
   - Identifies discrepancies larger than 1%

To run the validations:

```bash
python src/business_validations.py
```

## Security Notes

- Never commit the `.env` file to version control
- Use read-only database users for validations
- Regularly rotate database credentials
- Consider using a secrets management service in production

## Customizing Validations

To add new business validations:

1. Add new methods to the `BusinessValidator` class in `src/business_validations.py`
2. Follow the existing pattern of:
   - Writing clear SQL queries
   - Implementing proper error handling
   - Returning structured validation results

## Error Handling

The tool implements comprehensive error handling:
- Connection errors are caught and reported
- Query execution errors are handled gracefully
- Resources are properly closed using context managers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License 