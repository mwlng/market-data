from risingwave import RisingWave, RisingWaveConnOptions, OutputFormat, MaterializedView
import pandas as pd
import threading

class RisingWaveClient:
    def __init__(self, host: str = "localhost", 
                 port: int = 4566,
                 user: str = 'root',
                 password: str = 'root',
                 database: str = 'dev'
                ):
        self._connOPtions = RisingWaveConnOptions.from_connection_info(
            host=host, port=port, user=user, password=password, database=database
        )
        self._rw = RisingWave(self._connOPtions)
    

    def create_schema(self, schema_name: str):
        sql=f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
        self._rw.execute(sql)

    #def create_table(self, table_name: str, schema: str = 'public'):
     
    def create_materialized_view(self, name:str, query: str, schema: str = 'public') -> MaterializedView:
        return self._rw.mv(
            name=name,
            stmt=query,
            schema_name=schema            
        )


    def insert_dataframe(self, table: str, df: pd.DataFrame, schema: str = 'public'):
        self._rw.insert(table_name=table, data=df)


    def query(self, sql: str) -> pd.DataFrame:
        result = self._rw.query(sql, output_format=OutputFormat.PANDAS)
        return result
    

    def subscribe_table_change(self, table: str, 
                               handler: callable,
                               schema: str = 'public') -> threading.Thread:
        def subscribe_table():
            self._rw.on_change(
                name=table, 
                handler=handler,
                output_format=OutputFormat.DATAFRAME,
                schema_name=schema,
            )

        return threading.Thread(target=subscribe_table)
    

    def subscribe_mv_change(self, mv: MaterializedView, 
                     handler: callable) -> threading.Thread:
        def subscribe_mv():
            mv.on_change(
                handler=handler,
                output_format=OutputFormat.DATAFRAME,
            )

        return threading.Thread(target=subscribe_mv)
