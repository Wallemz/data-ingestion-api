import azure.functions as func
from function_http_trigger import http_trigger_bp
from function_svbus_trigger import svbus_trigger_bp

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
app.register_functions(http_trigger_bp) 
app.register_functions(svbus_trigger_bp)