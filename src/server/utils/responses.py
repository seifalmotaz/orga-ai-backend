from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


class APIResponse:
    """Standardized API response utilities."""
    
    @staticmethod
    def success(
        data: Any = None, 
        message: str = "Success", 
        status_code: int = status.HTTP_200_OK
    ) -> Dict[str, Any]:
        """Create a successful response."""
        response = {
            "success": True,
            "message": message,
        }
        if data is not None:
            response["data"] = data
        return response
    
    @staticmethod
    def error(
        message: str = "An error occurred",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None
    ) -> HTTPException:
        """Create an error response."""
        error_data = {
            "success": False,
            "message": message,
        }
        if details:
            error_data["details"] = details
        
        raise HTTPException(status_code=status_code, detail=error_data)


class TaskNotFoundError(HTTPException):
    """Custom exception for task not found."""
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "message": f"Task with ID {task_id} not found",
                "error_code": "TASK_NOT_FOUND"
            }
        )


class ValidationError(HTTPException):
    """Custom exception for validation errors."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        error_detail = {
            "success": False,
            "message": message,
            "error_code": "VALIDATION_ERROR"
        }
        if details:
            error_detail["details"] = details
            
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error_detail
        )


class UnauthorizedError(HTTPException):
    """Custom exception for unauthorized access."""
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "message": message,
                "error_code": "UNAUTHORIZED"
            }
        )


class ForbiddenError(HTTPException):
    """Custom exception for forbidden access."""
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "message": message,
                "error_code": "FORBIDDEN"
            }
        )
