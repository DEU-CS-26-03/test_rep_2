class TryonStatus:
    QUEUED     = "queued"
    PROCESSING = "processing"
    COMPLETED  = "completed"
    FAILED     = "failed"

class ErrorCode:
    INVALID_FILE_TYPE  = "INVALID_FILE_TYPE"
    FILE_TOO_LARGE     = "FILE_TOO_LARGE"
    NOT_FOUND          = "NOT_FOUND"
    TRYON_BUSY         = "TRYON_BUSY"
    MODEL_NOT_READY    = "MODEL_NOT_READY"
    INFERENCE_FAILED   = "INFERENCE_FAILED"
    BAD_REQUEST        = "BAD_REQUEST"
