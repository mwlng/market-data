from pydantic import BaseModel

class StockDataModel(BaseModel):
    id: int
    name: str
    email: str

def create_stock_data_model(data: dict) -> StockDataModel:
    """
    Create a StockDataModel instance from a dictionary.

    Args:
        data (dict): A dictionary containing stock data.
    """
    try:
        stock_data_model = StockDataModel(**data)
    except Exception as e:
        print(f"Error creating StockDataModel: {e}")
        raise
        
    return stock_data_model

