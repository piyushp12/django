import mysql.connector

# Connect to the source database
source_connection = mysql.connector.connect(
    host='3.234.60.184',
    user='breakout_user',
    password='Mobilo/tte56',
    database='breakoutDB_live'
)

# Connect to the destination database
destination_connection = mysql.connector.connect(
    host='mysql-164782-0.cloudclusters.net',
    user='admin',
    password='TRVVNwrt',
    database='mySQL'
)

# Create cursor objects for both connections
source_cursor = source_connection.cursor()
destination_cursor = destination_connection.cursor()

try:
    # Fetch data from the source database
    source_cursor.execute("SELECT * FROM your_table_name")
    rows = source_cursor.fetchall()

    # Insert data into the destination database
    for row in rows:
        destination_cursor.execute("INSERT INTO App_cryptopair (exchange, pair) VALUES (%s, %s)", row)

    # Commit the transaction
    destination_connection.commit()
    print("Data transfer successful.")

except mysql.connector.Error as error:
    print("Error transferring data:", error)

finally:
    # Close cursor and connections
    source_cursor.close()
    destination_cursor.close()
    source_connection.close()
    destination_connection.close()
