def fillListUntillsafeword(safeword: str='stop') -> list:
    list = []
    user_input = ''
    user_input_name = input('Enter a name: ')
    user_input_id = input('Enter an id: ')
    while user_input_name and user_input_id != safeword:
        list.append(user_input)
        user_input = input(f'Enter a name or write {safeword} to stop: ')
        user_input_id = input(f'Enter an id or write {safeword} to stop: ')
    return list

list1=fillListUntillsafeword()
for i in list1:
    print(i)
