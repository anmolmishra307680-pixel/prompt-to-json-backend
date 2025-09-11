"""Schema models for different prompt types."""

from .design import DesignSpec, Dimensions, Metadata
from .email import EmailSpec

__all__ = ["DesignSpec", "Dimensions", "Metadata", "EmailSpec"]