import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from lxmlparser1 import HTMLParser

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
    cleaned_text = re.sub(r'\{.*?\}', '', process_text)
    # cleaned_text = re.sub(r'<[^>]*>', '', process_text)


    return cleaned_text


def cleaning_function(best_node,parser):

    content = []

    #No article tag taken
    tag_types = ['p', 'div', 'span']
    # Define undesired word patterns for each category
    advertisement_pattern = r'\bads?\b|Advertisement|advertisements|view comments|I agree to theterms|I agree to the terms'
    technical_issues_pattern = r'sorry|try again|audio is unavailable|AI-generated|Content is loading'
    subscription_pattern = r'subscribe|purchase|subscription'
    feedback_pattern = r'feedback|facebooktwiiterwhatsapp'
    footer_pattern = r'read\s*more|read next|editors pick'

    # Add more patterns for other categories if needed

    # Combine all patterns into a single regular expression
    undesired_words_pattern = re.compile(
        f'{advertisement_pattern}|{technical_issues_pattern}|{subscription_pattern}|{feedback_pattern}|{footer_pattern}',
        re.IGNORECASE
    )




    # for node in best_node.find_all(tag_types[0]) + best_node.find_all(tag_types[2]):
    for node in parser.find_all_lxml(node=best_node):
        if(node.tag != tag_types[0] and node.tag != tag_types[2]):
            continue 
        # print(node.tag," ",node.text_content().strip())
        
        parent_list = []
        parent = node.getparent()
        # parent = node.parent
        cnt = 0
        while(cnt < 5):
           parent_list.append(parent)
           parent = parent.getparent()
        #    parent = parent.parent
           cnt = cnt+1
        
        flag = 0
        for z in parent_list:
           if(z.tag == "form"):
            #  if(node.name == "form"):
              flag = 1
              break
        
        if(flag == 1):
           continue
        
        content.append(parser.remove_scripts(node).strip())
        
    if len(content) > 5:
    
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(content)
        cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Identify duplicate or highly similar sentences using cosine similarity
        duplicate_indices = set()
        for i in range(len(content)):
            for j in range(i+1, len(content)):
                if cosine_similarities[i][j] > 0.9:  # Adjust threshold as needed
                    duplicate_indices.add(j)

        # Filter out duplicate sentences
        unique_content = [content[i] for i in range(len(content)) if i not in duplicate_indices]

        # Print unique content
        for sentence in unique_content:
            print(sentence.replace('\n', ' '))


    else:
      for node in parser.find_all_lxml(node=best_node):
        try:
           if(node.tag != tag_types[1]):
               continue
           print(node.text_content().strip())
           text = node.text_content().strip()
           text = process_text(text,undesired_words_pattern)
           if len(text) >= 10:
               content.append(parser.remove_scripts(node).strip())
        except:
            continue
      
      if len(content) > 0:
        
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(content)
        cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Identify duplicate or highly similar sentences using cosine similarity
        duplicate_indices = set()
        for i in range(len(content)):
            for j in range(i+1, len(content)):
                if cosine_similarities[i][j] > 0.9:  # Adjust threshold as needed
                    duplicate_indices.add(j)

        # Filter out duplicate sentences
        unique_content = [content[i] for i in range(len(content)) if i not in duplicate_indices]

        # Print unique content
        for sentence in unique_content:
            # print(sentence)
            print(sentence.replace('\n', ' '))
            # pass
      else:
        # print(best_node.get_text(strip=True))
          content = parser.remove_scripts(best_node)
          print(content.strip().replace('\n', ' '))