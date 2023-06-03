def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False




