# Message List 
# [id of message, message size, frequnecy]

# LIST VERSION
def message_list_updater(messages, new_message):
    ''' 
    message list is list of lists [id of message, message size, frequency]
    new_message is a list [id of message, message size, frequency]
    Function checks id to see if new message matches an existing message. 
    If it matches, the frequency is incremented. 
    If it does not match any existing message, the new message is appended to the list. 
    Updated message_list is returned. 
    '''
    i = 0
    while i < len(messages):
        if new_message[0] == messages[i][0]:
            messages[i][2] += 1
            break
        i += 1
    else: 
        messages.append(new_message)
    return messages

# ARRAY VERSION
# def message_updater(message_array, new_message):
#     i = 0
#     while i < len(message_array):
#         if new_message[0] == message_array[i][0]:
#             message_array[i][2] += 1
#             break
#         i += 1
#     else: 
#         message_array = np.vstack((message_array,new_message))
#     return message_array


def message_global(params, substep, state_history, prev_state, policy_input):
    '''
    Maintain global list of messages and frequencies. Used for testing of policies. 
    '''
    key = 'message_list'
    # value = prev_state[key]
    value = message_list_updater(prev_state['message_list'], policy_input['new_message'])
    return (key, value)


