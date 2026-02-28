from enum import Enum

class UserRole(str,Enum):
    CANDIDATE = "candidate"
    RECRUITER = "recruiter"
    ADMIN = "admin"
    SUPER_ADIMM="super_admin"
    
