class Dax:
    def __init__(catalog, datasource):
        self.catalog = catalog
        self.datasource = datasource

    def handle_oledb_field(f):
        mytype=str(type(f))
        if mytype == "<class 'System.DBNull'>": 
            return None
        if mytype == "<class 'int'>": 
            return int(f)        
        if mytype == "<class 'System.Decimal'>": 
            return float(f.ToString())
        if mytype == "<class 'str'>": 
            return str(f)
        raise "Unknown Type " + mytype   
        
    def tidy_col_name(c):
        newname = c.replace('[', '_').replace(']', '_').replace(' ', '_')
        return newname.strip('_')
        
    def dax_to_dataframe(self, daxcmd):
        if "connection" not in dax_to_dataframe.__dict__: dax_to_dataframe.connection = None
        connStr = f"Provider=MSOLAP;Persist Security Info=True;Initial Catalog={self.catalog};Data Source={self.datasource}"

        if self.connection is None:
            self.connection = ADONET.OleDbConnection(connStr)
            self.connection.Open()

        command = self.connection.CreateCommand()
        command.CommandText = daxcmd
        reader = command.ExecuteReader()
        schema_table = reader.GetSchemaTable()

        #schema_table rows are query result columns
        columns = []
        for r in schema_table.Rows:
            columns.append(r['ColumnName'])

        rows = [None] * reader.get_RecordsAffected()
        for x in tqdm(range(0, reader.get_RecordsAffected())):
            reader.Read()
            #https://docs.microsoft.com/en-us/dotnet/api/system.typecode?view=netframework-4.7.2
            #but ints dont have them
            #rows[x] = list( [ reader[c] if reader[c].GetTypeCode() != 2 else None for c in columns] )
            rows[x] = list ( [ handle_oledb_field(reader[c]) for c in columns ] )
            
        #connection.Close()
        df = pd.DataFrame.from_records(columns=[tidy_col_name(c) for c in columns], data=rows, coerce_float=True)
        del rows
        del reader
        return df