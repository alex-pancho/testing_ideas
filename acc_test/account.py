import sys


def acc(filename=None):
    ''' description '''

    if filename is None:
        try:
            filename=sys.argv[1]
        except IndexError:
            filename='transactions.txt'

    try:
        openfile = open(filename, "r")
    except FileNotFoundError as e:
        print(e)
        return
    saldo=0
    opercount=0
    first_negaviv = []
    with openfile as f:
        lines = f.readlines()
        
        if len(lines) == 0:
            print('no data')
            return
        for l in lines:
            l = l.replace("  ", " ").replace("\t", " ").replace("\n", "").replace("$", "").split(" ")
            try:
                l[2] = float(l[2])
            except ValueError:
                try:
                    print(l[0],l[1], f':{l[2]} is wrong ammount')
                except IndexError:
                    print('wrong number of parametrs')
                return
            except IndexError:
                print ('no ammount data in string')
                return
            try:
                l[1]=l[1].lower()
            except (ValueError,IndexError):
                print ('wrong or missed operation data')
                return
                
            if l[1]!= 'deposit' and  l[1]!= 'withdraw':
                print ( l[0], f': {l[1]} : is wrong operation data')
                return
            if l[1]== 'deposit':
                saldo = saldo+l[2]
                opercount=opercount+1
            else:
                saldo = saldo-l[2]
                opercount=opercount+1
                if saldo < 0 and len(first_negaviv) == 0:
                    first_negaviv=[l[0],l[1],l[2]]
                
        print('The number of total transactions:', opercount)
        print('The account balance including all transactions:', round(saldo, 2))
        if len(first_negaviv) >0:
            long_text= 'The date and balance for the first transaction that results in a negative account balance'
            print(long_text, first_negaviv)
    return True

if __name__ == '__main__':
    acc()