

def message_collect(only_list: bool = False):
    """
    Message collector for collect jsonify the response message.
    
    :param: only_list: by default returns a string if one message is present,
    else returns a list of message, if multiple message are present. For returning
    only list set this parameter to True
    """
    messages = []
    def wrapper(mes: str = None):
        nonlocal messages
        if mes:
            messages.append(mes)
            return
        if len(messages) == 1 and not only_list:
            return messages[0]
        return messages
    return wrapper