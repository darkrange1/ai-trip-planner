from utils.expense_calculator import Calculator
from typing import List
from langchain.tools import tool

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""
        @tool
        def estimate_total_hotel_cost(price_per_night: str | float | int, total_days: float | int) -> float:
            """Calculate total hotel cost"""
            try:
                # Clean string if necessary (remove currency symbols like $)
                if isinstance(price_per_night, str):
                    clean_price = ''.join(c for c in price_per_night if c.isdigit() or c == '.')
                    price_val = float(clean_price) if clean_price else 0.0
                else:
                    price_val = float(price_per_night)
                
                days_val = float(total_days)
                return self.calculator.multiply(price_val, days_val)
            except Exception:
                return 0.0
        
        @tool
        def calculate_total_expense(costs: List[float]) -> float:
            """Calculate total expense of the trip"""
            return self.calculator.calculate_total(*costs)
        
        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate daily expense"""
            return self.calculator.calculate_daily_budget(total_cost, days)
        
        return [estimate_total_hotel_cost, calculate_total_expense, calculate_daily_expense_budget]