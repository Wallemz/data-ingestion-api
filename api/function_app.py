import azure.functions as func
from additional_function_app import bp1
from function_http_trigger import http_trigger_bp

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
app.register_functions(bp1)
app.register_functions(http_trigger_bp) 