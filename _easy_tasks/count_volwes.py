input_string = "jklsdfjdkfadjkuiueuwewuh jschjkeuewuf/ UYEUWHJNBX oooooooooo"

def volwes_counter(incoming:str):
    count = 0
    count_dict = dict()
    count_str = incoming.lower().strip()
    volwes = "aeyuio"
    for char in count_str:
        if char in volwes:
            count_dict[char] = count_dict[char] + 1 if count_dict.get(char, False) else 1      
  
    return count_dict if count_dict else count

print(volwes_counter(input_string))