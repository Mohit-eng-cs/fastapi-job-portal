def Jobs_code(jobname:str,id:int):
    new_code = f"{jobname[:3].upper()}-{id+1:04}"
    return new_code

print(Jobs_code("Software eng",27))

