"""
This is a program meant to track satelite movements and properly display them on a map
"""
from datetime import datetime

now = datetime.utcnow()  #Palydovai naudoja UTC laika, padaryti i class veliau, kad palydovo clase paveldetu
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted)