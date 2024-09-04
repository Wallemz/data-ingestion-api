import azure.functions as func
from additional_function_app import bp1
from aditional_function_app import bp2

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
app.register_functions(bp1)
app.register_functions(bp2) 