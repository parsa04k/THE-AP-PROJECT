import secrets
import string
import difflib
import re
from models import *

def generate_temp_password(length): 
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password



def find_similar_names(name, name_list = ClinicTable().names(), cutoff=0.6):
    
    # Use difflib to find close matches
    close_matches = difflib.get_close_matches(name, name_list, n=5, cutoff=cutoff)

    # Use regex to find names that contain the search term
    regex_matches = [n for n in name_list if re.search(name, n, re.IGNORECASE)]

    # Combine and deduplicate the lists
    similar_names = list(set(close_matches + regex_matches))
    if similar_names==[]:
        return False
    for name in similar_names:
        ClinicTable().read(name)
        
    return True 