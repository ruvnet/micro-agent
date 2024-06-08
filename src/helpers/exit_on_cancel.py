def exit_on_cancel(value):
    if isinstance(value, symbol):
        print('Goodbye!')
        exit(0)
    return value
