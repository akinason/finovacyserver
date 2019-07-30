
def format_api_response(success, result=None, errors=None, status_code=None, error_message=None):
    if errors and error_message:
        errors['message'] = error_message
    elif error_message and not errors:
        errors = {}
        errors['message'] = error_message

    return {
        "success": success, "results": result if result else {}, "errors": errors if errors else {}
    }
