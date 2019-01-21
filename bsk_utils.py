from time import gmtime, strftime
from typing import List

def create_keyword_card(input_list: list,
                        name: str,
                        card_id: int,
                        duration: float,
                        time_codes: List[List[dict]] = None) -> dict:

    """
    Return a dict formatted in the style that Box expects for its skills.

    Takes a list of Watson Natural Language Understanding enrichments, such as keywords or concepts, to use as the elements of a card in a box skill and
    formats it correctly to appear as a collection of bubbles in the metadata
    portion of a file shown on Box. 

    Args:
        input_list: A list of the things to appear as bubbles on this card.
        name: The title of the card to create.
        card_id: An identified for the Box skills card.
        duration: The length in seconds of the card.
        time_codes: A list of the time codes for a particular bubble. The format
            should be a list where each element corrosponds to an element of the
            input list. The second level down should be a list of all of the
            time codes to append to the bubble. The next level down should be
            a dict representing the individual times, with a start and end
            end key whose value is a time in secods.

    Returns:
        A dict representing the correct format for a card on a Box skill.
    """

    card = {
        'created_at': get_formatted_time(),
        'type': 'skill_card',
        'skill_card_type': 'keyword',
        'skill': {
            'type': 'service',
            'id': 'box-skill-exploration-ex'
        },
        'invocation': {
            'type': 'skill_invocation',
            'id': card_id
        },
        'skill_card_title': {'message': name},
        'duration': duration,
        'entries': []
    }

    for index, element in enumerate(input_list):
        try:
            if time_codes:
                element_time_codes = time_codes[index]
                chunk = {'type': 'text', 'text': element, 'appears': []}

                for time_code in element_time_codes:
                    time_code_formatted = {'start': time_code['start'],
                                           'end': time_code['end']}
                    chunk['appears'].append(time_code_formatted)

            else:
                chunk = {'type': 'text', 'text': element}
            card['entries'].append(chunk)
            
        except IndexError as error:
            print(len(input_list))
            print(index)
            print(str(error))

    return card

def create_transcript_card(stt_output: dict,
                           name: str,
                           card_id: int,
                           duration: float) -> dict:

    """
    Return a dict formatted in the style that Box expects for its skills.

    Takes the output of Watson Speech to Text and returns a dict that is formatted
    correctly. The input is the direct output of Watson Speech to Text.

    Args:
        stt_output: The direct output of Watson Speech to Text.
        name: The title of the card to create.
        card_id: An identified for the Box skills card.
        duration: The length in seconds of the card.

    Returns:
        A dict representing the correct format for a card on a Box skill.
    """

    card = {
        'created_at': get_formatted_time(),
        'type': 'skill_card',
        'skill_card_type': 'transcript',
        'skill': {
            'type': 'service',
            'id': 'box-skill-exploration-ex'
        },
        'invocation': {
            'type': 'skill_invocation',
            'id': card_id
        },
        'skill_card_title': {'message': name},
        'duration': duration,
        'entries': []
    }

    for entry in stt_output['results']:
        text = entry['alternatives'][0]['transcript']
        text = text[:-1] + '.'
        text = text.capitalize()
        chunk = {'text':text}
        chunk['appears'] = [{'start': entry['alternatives'][0]['timestamps'][0][1],
                             'end': entry['alternatives'][0]['timestamps'][-1][2]}]
        card['entries'].append(chunk)

    return card

def create_timeline_card(input_list: list,
                         name: str,
                         card_id: int,
                         duration: float,
                         time_codes: List[List[dict]]) -> dict:

    """
    Return a dict formatted in the style that Box expects for its skills.

    Takes a list of things to use as the elements of a card in a Box skill and
    formats it correctly to appear as a list, with a colored bar under it that
    will bring you to the correct place in a video or audio file when clicked.

    Args:
        input_list: A list of the things to appear as bubbles on this card.
        name: The title of the card to create.
        card_id: An identified for the Box skills card.
        duration: The length in seconds of the card.
        time_codes: A list of the time codes for a particular bubble. The format
            should be a list where each element corrosponds to an element of the
            input list. The second level down should be a list of all of the
            time codes to append to the bubble. The next level down should be
            a dict representing the individual times, with a start and
            end key whose value is a time in secods.

    Returns:
        A dict representing the correct format for a card on a Box skill.
    """

    card = {
        'created_at': get_formatted_time(),
        'type': 'skill_card',
        'skill_card_type': 'timeline',
        'skill': {
            'type': 'service',
            'id': 'box-skill-exploration-ex'
        },
        'invocation': {
            'type': 'skill_invocation',
            'id': card_id
        },
        'skill_card_title': {'message': name},
        'duration': duration,
        'entries': []
    }

    for index, element in enumerate(input_list):
        if time_codes:
            element_time_codes = time_codes[index]
            chunk = {'text': element, 'appears': []}

            for time_code in element_time_codes:
                time_code_formatted = {'start': time_code['start'],
                                       'end': time_code['end']}
                chunk['appears'].append(time_code_formatted)

        card['entries'].append(chunk)

    print(card)
    return card

def get_formatted_time() -> str:
    '''Return time formatted in an appropriatly specific format'''

    #YYYY-MM-DD'T'HH:MM:SS'Z' format e.g. "2018-02-05T18:49:57.714Z"
    time = strftime("%Y-%m-%dT%H:%M:%S.000Z", gmtime())
    return time
