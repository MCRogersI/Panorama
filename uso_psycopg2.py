import psycopg2
# Connect to an existing database

conn = psycopg2.connect("dbname=panorama user=postgres host=localhost password=hxq54ght3 port=5432")


# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
#cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
cur.execute("INSERT INTO empleados VALUES (%s, %s, %s,%s, %s, %s, %s)",(3, 'pajero',1, 'f','f','f','f',))

# Query the database and obtain data as Python objects
#cur.execute("SELECT * FROM test;")

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()