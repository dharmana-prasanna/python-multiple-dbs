from db_connectors.database import get_connector
from typing import Dict, List, Any
import pandas as pd

class BusinessValidator:
    def __init__(self):
        self.postgres = get_connector('postgres')
        self.oracle = get_connector('oracle')
        self.teradata = get_connector('teradata')
        self.snowflake = get_connector('snowflake')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.postgres.close()
        self.oracle.close()
        self.teradata.close()
        self.snowflake.close()

    def validate_customer_data(self) -> Dict[str, Any]:
        """
        Sample business validation that compares customer data across different databases
        """
        # Query customer counts from different systems
        pg_query = """
        SELECT COUNT(*) as customer_count 
        FROM customers 
        WHERE created_date >= CURRENT_DATE - INTERVAL '1 month'
        """
        
        oracle_query = """
        SELECT COUNT(*) as customer_count 
        FROM customers 
        WHERE created_date >= ADD_MONTHS(TRUNC(SYSDATE), -1)
        """
        
        teradata_query = """
        SELECT COUNT(*) as customer_count 
        FROM customers 
        WHERE created_date >= ADD_MONTHS(CURRENT_DATE, -1)
        """
        
        snowflake_query = """
        SELECT COUNT(*) as customer_count 
        FROM customers 
        WHERE created_date >= DATEADD(month, -1, CURRENT_DATE())
        """

        try:
            pg_result = self.postgres.execute_query(pg_query)[0]
            oracle_result = self.oracle.execute_query(oracle_query)[0]
            teradata_result = self.teradata.execute_query(teradata_query)[0]
            snowflake_result = self.snowflake.execute_query(snowflake_query)[0]

            results = {
                'postgres_count': pg_result['customer_count'],
                'oracle_count': oracle_result['customer_count'],
                'teradata_count': teradata_result['customer_count'],
                'snowflake_count': snowflake_result['customer_count']
            }

            # Validate if counts match across systems
            counts = list(results.values())
            if len(set(counts)) != 1:
                results['validation_status'] = 'FAILED'
                results['message'] = 'Customer counts do not match across systems'
            else:
                results['validation_status'] = 'PASSED'
                results['message'] = 'Customer counts match across all systems'

            return results

        except Exception as e:
            return {
                'validation_status': 'ERROR',
                'message': f'Error during validation: {str(e)}'
            }

    def validate_revenue_data(self) -> Dict[str, Any]:
        """
        Sample business validation that compares revenue data across systems
        """
        # Query to get daily revenue for last 7 days
        pg_query = """
        SELECT date_trunc('day', transaction_date) as date,
               SUM(amount) as daily_revenue
        FROM transactions
        WHERE transaction_date >= CURRENT_DATE - INTERVAL '7 days'
        GROUP BY date_trunc('day', transaction_date)
        ORDER BY date
        """

        snowflake_query = """
        SELECT DATE_TRUNC('day', transaction_date) as date,
               SUM(amount) as daily_revenue
        FROM transactions
        WHERE transaction_date >= DATEADD(day, -7, CURRENT_DATE())
        GROUP BY DATE_TRUNC('day', transaction_date)
        ORDER BY date
        """

        try:
            # Get data from both systems
            pg_data = pd.DataFrame(self.postgres.execute_query(pg_query))
            snowflake_data = pd.DataFrame(self.snowflake.execute_query(snowflake_query))

            # Compare the results
            merged_data = pd.merge(
                pg_data, 
                snowflake_data, 
                on='date', 
                suffixes=('_pg', '_sf')
            )

            # Calculate difference percentage
            merged_data['diff_percentage'] = abs(
                (merged_data['daily_revenue_pg'] - merged_data['daily_revenue_sf']) / 
                merged_data['daily_revenue_pg']
            ) * 100

            # Check if any day has more than 1% difference
            discrepancies = merged_data[merged_data['diff_percentage'] > 1]

            if len(discrepancies) > 0:
                return {
                    'validation_status': 'FAILED',
                    'message': f'Found {len(discrepancies)} days with revenue discrepancy > 1%',
                    'discrepancies': discrepancies.to_dict('records')
                }
            else:
                return {
                    'validation_status': 'PASSED',
                    'message': 'Revenue data matches within 1% tolerance across systems'
                }

        except Exception as e:
            return {
                'validation_status': 'ERROR',
                'message': f'Error during validation: {str(e)}'
            }

    def validate_inventory_levels(self) -> Dict[str, Any]:
        """
        Sample business validation that compares inventory levels
        across PostgreSQL and Oracle databases
        """
        pg_query = """
        SELECT 
            product_id,
            product_name,
            current_stock,
            last_updated
        FROM inventory
        WHERE current_stock < reorder_point
        """
        
        oracle_query = """
        SELECT 
            product_id,
            product_name,
            current_stock,
            last_updated
        FROM inventory
        WHERE current_stock < reorder_point
        """

        try:
            # Get data from both systems
            pg_data = pd.DataFrame(self.postgres.execute_query(pg_query))
            oracle_data = pd.DataFrame(self.oracle.execute_query(oracle_query))

            # Compare the results
            merged_data = pd.merge(
                pg_data,
                oracle_data,
                on=['product_id', 'product_name'],
                suffixes=('_pg', '_oracle')
            )

            # Find discrepancies
            discrepancies = merged_data[
                merged_data['current_stock_pg'] != merged_data['current_stock_oracle']
            ]

            if len(discrepancies) > 0:
                return {
                    'validation_status': 'FAILED',
                    'message': f'Found {len(discrepancies)} products with inventory discrepancies',
                    'discrepancies': discrepancies.to_dict('records')
                }
            else:
                return {
                    'validation_status': 'PASSED',
                    'message': 'Inventory levels match across systems'
                }

        except Exception as e:
            return {
                'validation_status': 'ERROR',
                'message': f'Error during inventory validation: {str(e)}'
            }

def main():
    with BusinessValidator() as validator:
        # Run customer data validation
        print("\nValidating customer data...")
        customer_validation = validator.validate_customer_data()
        print(f"Status: {customer_validation['validation_status']}")
        print(f"Message: {customer_validation['message']}")
        
        # Run revenue data validation
        print("\nValidating revenue data...")
        revenue_validation = validator.validate_revenue_data()
        print(f"Status: {revenue_validation['validation_status']}")
        print(f"Message: {revenue_validation['message']}")

        # Run new inventory validation
        print("\nValidating inventory levels...")
        inventory_validation = validator.validate_inventory_levels()
        print(f"Status: {inventory_validation['validation_status']}")
        print(f"Message: {inventory_validation['message']}")

if __name__ == "__main__":
    main() 