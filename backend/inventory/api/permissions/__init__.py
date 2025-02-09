"""
Permissions module for the API.
This module contains all the custom permissions used in the API.
"""

from .base import IsStaffOrReadOnly, IsOwnerOrStaff

__all__ = ['IsStaffOrReadOnly', 'IsOwnerOrStaff']
