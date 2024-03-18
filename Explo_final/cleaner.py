import re

def is_valid_datetime(datetime_string):
    # Define a regex pattern for the specified datetime format
    pattern = r'^[A-Z][a-z]{2}\s\d{1,2},\s\d{4}\s\d{1,2}:\d{2}\s(?:AM|PM)$'

    # Check if the string matches the pattern
    if re.match(pattern, datetime_string):
        return True
    else:
        return False


def process_text(text, words_to_delete_pattern=None):
    # Split the text into a list of strings using full stops and question marks as delimiters
    text_list = [part.strip() for part in re.split(r'(?<!\d)\.|\?(?!\d)', text)]

#     # Check if text is a valid datetime
    if is_valid_datetime(text):
        return ''
    # print(text_list)
    # print("\n\n")
    # If words_to_delete_pattern is provided, use it to remove undesired words
    if words_to_delete_pattern:
        text_list = [part for part in text_list if not any(words_to_delete_pattern.findall(part))]

    # Join the remaining strings in the list to form the text in order
    processed_text = ' '.join(text_list)

    return processed_text


def cleaning_function(best_node):

    content = []

    #No article tag taken
    tag_types = ['p', 'div', 'span']
    # Define undesired word patterns for each category
    advertisement_pattern = r'\bads?\b|Advertisement|advertisements'
    technical_issues_pattern = r'sorry|try again|audio is unavailable|AI-generated|Content is loading'
    subscription_pattern = r'subscribe|purchase'
    feedback_pattern = r'feedback'
    footer_pattern = r'read\s*more'

    # Add more patterns for other categories if needed

    # Combine all patterns into a single regular expression
    undesired_words_pattern = re.compile(
        f'{advertisement_pattern}|{technical_issues_pattern}|{subscription_pattern}|{feedback_pattern}|{footer_pattern}',
        re.IGNORECASE
    )



    for node in best_node.find_all(tag_types[0]) + best_node.find_all(tag_types[2]):
        try:
           if len(node.find_all()) == 0 or any(child.name in ['a', 'em', 'span'] for child in node.children):


                text = node.get_text(strip=True)
                text = process_text(text,undesired_words_pattern)
                if len(text) >= 10:
                    content.append(text)
        except:
            continue


    fin = []
    if len(content) > 0:
        for x in content:
            if(x not in fin):
              fin.append(x)
        for x in fin:
          print(x)

    else:
      for node in best_node.find_all(tag_types[1]):
        try:
            if len(node.find_all()) == 0 :
                text = node.get_text(strip=True)
                text = process_text(text)
                if len(text) >= 10:
                    content.append(text)
        except:
            continue

      fin = []
      if len(content) > 0:
        for x in content:
            if(x not in fin):
              fin.append(x)
        for x in fin:
          print(x)
      else:
        print("No data found on Website")