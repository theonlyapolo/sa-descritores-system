from enum import Enum

class UserRole(str, Enum):
    ADMIN = "Administrador"
    PCA = "PCA"

class DescriptorStatus(str, Enum):
    APPLIED = "Aplicado"
    NOT_APPLIED = "Não Aplicado"
