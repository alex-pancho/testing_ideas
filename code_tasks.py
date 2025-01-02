
input_string = "jklsdfjdkfadjkuiueuwewuh jschjkeuewuf/ UYEUWHJNBX"

def volwes_counter(incoming:str):
    count = 0
    count_dict = dict()
    count_str = incoming.lower().strip()
    volwes = "aeyuio"
    for char in count_str:
        if char in volwes and char not in count_dict:
            count_dict[char] = 1
        elif char in volwes and char  in count_dict:
            count_dict[char] += 1
        
    return count_dict if count_dict else count

print(volwes_counter("sdfghjk"))