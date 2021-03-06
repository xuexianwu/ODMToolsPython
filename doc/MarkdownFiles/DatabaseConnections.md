#Connecting to an ODM Database#

Before using the ODM Tools Python application, a connection must be established to an ODM database. The application is compatible with databases running in Microsoft SQL Server and MySQL. Note that the user must already have credentials to use ODM Tools Python to access a database. 

In the 'Database Configuration' window, select 'SQL Server' or 'MySQL' from the Connection Type dropdown. Enter the server name, the database name, and the user credentials. Connections can be made to local or remote database servers. If you are unsure of the server path or database name, consult with your database administrator. Use the 'Test Connection' button to verify configuration, and click the 'Save Connection' button to use the specified configuration.

![DatabaseConnection](images/DatabaseConnection.png)

Note that the application only supports connections to one database at a time, and the configuration can be changed via the 'File' menu on the ribbon. The database configuration that you specify will be saved to a .config file so that the the connection will persist when the program is re-opened. Note that the user credentials are saved to this file, and may be visible elsewhere when using the program, so users should avoid using sensitive passwords.