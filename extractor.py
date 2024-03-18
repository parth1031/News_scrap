from bs4 import BeautifulSoup
from dateutil.parser import parse as date_parser



from bs4 import BeautifulSoup
from dateutil.parser import parse as date_parser
from stopwords import stop_word_lis

import re



class CustomExtractor:
    def __init__(self):
        self.stopwords = stop_word_lis()
        # self.parser = HTMLParser

    def calculate_gravity_score(self, tag):
        # Your custom logic to calculate the gravity score
        # This example uses the length of text content as a score
        text_content = tag.get_text(strip=True)
        return len(text_content)

    def previousSiblings(self,node):
      try:
        return [n for n in node.itersiblings(preceding=True)]
      except:
        return []
    def nieghbourhood_aggregation(self, node):
        # Iterate over siblings
        return self.previousSiblings(node)

    def linkage(self, node):

        # For simplicity, this example checks if the node contains more than 5 links
        links = node.find_all('a')
        return len(links) > 25



    def boost_req(self, node):
        para = "p"
        steps_away = 0
        minimum_stopword_count = 2
        max_stepsaway_from_node = 3

        text_containers = self.nieghbourhood_aggregation(node)
        # print(len(text_containers))
        for current_node in text_containers:
            current_node_tag = current_node.name
            if current_node_tag == para:
                if steps_away >= max_stepsaway_from_node:
                    return False
                paragraph_text = current_node.get_text(strip=True)
                word_stats = self.stop_words_chck(paragraph_text)
                # print(word_stats)
                if word_stats > minimum_stopword_count:
                    return True
                steps_away += 1
        return False

    def stop_words_chck(self, text):
        text = re.sub(r'[^\w\s]', '', text)
        words = [word.lower() for word in text.split()]

        sm = 0
        for word in words:
          if(word in self.stopwords):
            sm+=1
        return sm


    def count_paragraph_tags_on_same_level_with_depth(self,element, depth=0):
        paragraph_tags = element.find_all('p', recursive=False)
        if paragraph_tags:
            return len(paragraph_tags), depth
        for child in element.children:
            try:
                num_paragraphs, child_depth = self.count_paragraph_tags_on_same_level_with_depth(child, depth=depth+1)
            except:
                continue
            if num_paragraphs:
                return num_paragraphs, child_depth
        return 0, 0


    def count_br_tags_on_same_level_with_depth(self,element, depth=0):
        paragraph_tags = element.find_all('br', recursive=False)
        if paragraph_tags:
            return len(paragraph_tags), depth
        for child in element.children:
            try:
                num_paragraphs, child_depth = self.count_br_tags_on_same_level_with_depth(child, depth=depth+1)
            except:
                continue
            if num_paragraphs:
                return num_paragraphs, child_depth
        return 0, 0



    def most_imp_node(self, soup):
        top_node = None
        top_node_score = 0
        worthy_text_containers = self.worthy_text_containers(soup)
        # print(worthy_text_containers)
        starting_boost = 1.0
        cnt = 0
        i = 0
        parent_text_containers = []
        text_containers_with_text = []


        for node in worthy_text_containers:
            text_node = node.get_text()
            word_stats = self.stop_words_chck(text_node)
#             print(node.get_text(strip=True))
            # print(word_stats)
            high_link_density = self.linkage(node)
            if word_stats >= 2 and not high_link_density:
                text_containers_with_text.append(node)

        text_containers_number = len(text_containers_with_text)
        negative_scoring = 0
        bottom_negativescore_text_containers = text_containers_number * 0.25

#         print(text_containers_with_text)
        for node in text_containers_with_text:

#             print(type(node))
            boost_score = 0
            depth = 0

            boost_score3 = 0
            depth3 = 0

            try:
                boost_score, depth = self.count_paragraph_tags_on_same_level_with_depth(node)
    #                print(node['class'], " ", boost_score)
            except:
                boost_score = 0

            try:
              boost_score3, depth3 = self.count_br_tags_on_same_level_with_depth(node)
            except:
              depth3 += 0

            text_node = node.get_text(strip=True)
            word_stats = self.stop_words_chck(text_node)/2
            temp = 0

            try:
                temp = len(node.content)
            except:
                pass

            boost_score2 = 0
            if(self.boost_req(node)):
              print("Hello ")
              boost_score2 = 5

            try:
              if 'article' in node['class'][0].split():
                word_stats += 10
            except:
                word_stats += 0
            try:
              if 'content' in node['class'][0].split():
                word_stats += 10
            except:
                word_stats += 0

            boost_score = boost_score*(0.95**(depth+1))
            upscore = word_stats + boost_score + boost_score2 + boost_score3*(0.95**(depth3+1))


            # class_pattern = re.compile(r'\b(?:article|content)\b', re.IGNORECASE)


#             print(upscore," ",word_stats," ",boost_score," ",word_stats+boost_score)



            parent_node = node.parent

            self.update_score(node,upscore)


            if(node['score'] > top_node_score):
              top_node = node
              top_node_score = node['score']

            # print(node.name," ",word_stats," ",boost_score," ",boost_score3," ",node['score']," ",upscore)

            parent_text_containers.append(node)
            # print(node.name," ",len(parent_text_containers))
            # try:
            #   print(node['class'])
            # except:
            #   boost_score += 0

            x = node
            if(node.name == 'p'):
                for i in range(5):
                    x = x.parent
                    self.update_score(x,upscore*((0.8)**i))

            if parent_node not in parent_text_containers:
                parent_text_containers.append(parent_node)

            parent_parent_node = parent_node.parent
            if parent_parent_node is not None:
                self.update_node_count(parent_parent_node, 1)

                if parent_parent_node not in parent_text_containers:
                    parent_text_containers.append(parent_parent_node)
            cnt += 1
            i += 1


        # print(len(parent_text_containers))
        for e in parent_text_containers:
            # print(node.name," ",node['score'])
            score = self.get_score(e)

            if score > top_node_score:
#                 print(node.name," ",node['score'])
                top_node = e
                top_node_score = score

            if top_node is None:
                top_node = e

        return top_node

    def worthy_text_containers(self, soup):
        worthy_text_containers = []
        for tag in ['div','p', 'pre', 'td']:
            items = soup.find_all(tag)
            worthy_text_containers += items
#         print(worthy_text_containers)
        return worthy_text_containers


    def update_score(self, node, score):
        if 'score' not in node:
            node['score'] = len(node.get_text(strip=True))**(0.5)
        node['score'] += score

    def update_node_count(self, node, count):
        if 'count' not in node:
            node['count'] = 0

        node['count'] += count

    def get_score(self, node):
        return node.get('score', 0)

    def get_authors(self, doc):
        def contains_digits(d):
            for char in d:
                if char.isdigit():
                    return True
            return False

        def unique_list(lst):
            count = {}
            list = []
            for item in lst:
                if item.lower() in count:
                    continue
                count[item.lower()] = 1
                list.append(item.title())
            return list

        def parse(str):

            str = ''.join(char for char in str if char != '<' and char != '>')

            str = str.replace('By:', '').replace('From:', '').strip()

            names = [s.strip() for s in re.split(r"[^\w\'\-\.]", str) if s]


            authors = []
            current = []
            delimiters = ['and', ',', '']

            for name in names:
                if name in delimiters:
                    if len(current) > 0:
                        authors.append(' '.join(current))
                        current = []
                elif not contains_digits(name):
                    current.append(name)

            valid_name = (len(current) >= 2)
            if valid_name:
                authors.append(' '.join(current))

            return authors
        patterns=[re.compile(r'(?:author.*?name|name.*?author)', re.IGNORECASE)]
        attributes = ['name', 'rel', 'itemprop', 'class', 'id']
        variables = ['author', 'byline', 'dc.creator', 'byl','group-info']
        matches = []
        authors = []

        for attr in attributes:
            for val in variables+patterns:
                found = doc.find_all(attrs={attr: val})
                matches.extend(found)


        for match in matches:
            content = ''
            if match.tag == 'meta':
                content_value = match.get('content')
                if len(content_value) > 0:
                    content = content_value[0]
            else:
                content = match.get_text() or ''
            if len(content) > 0:
                authors.extend(parse(content))

        return unique_list(authors)

    def publishing_date(self, url, doc):
        def parse_date(str):
            if str:
                try:
                    return date_parser(str)
                except (ValueError, OverflowError, AttributeError, TypeError):
                    return None


        STRICT_DATE_REGEX = re.compile(r'\/(\d{4})\/(\d{2})\/(\d{2})\/')
        date_pattern = re.compile(r'(\d{2} [a-zA-Z]{3} \d{4}) (\d{2}:\d{2}[APMapm]{2})')
        date_match = STRICT_DATE_REGEX.search(url)
        if date_match:
            str = date_match.group(0)
            datetime = parse_date(str)
            if datetime:
                return datetime


        date_tags = [
            {'attribute': ('property', 'rnews:datePublished'), 'content': 'content'},
            {'attribute': ('property', 'article:published_time'), 'content': 'content'},
            {'attribute': ('name', 'OriginalPublicationDate'), 'content': 'content'},
            {'attribute': ('itemprop', 'datePublished'), 'content': 'datetime'},
            {'attribute': ('property', 'og:published_time'), 'content': 'content'},
            {'attribute': ('name', 'article_date_original'), 'content': 'content'},
            {'attribute': ('name', 'publication_date'), 'content': 'content'},
            {'attribute': ('name', 'sailthru.date'), 'content': 'content'},
            {'attribute': ('name', 'PublishDate'), 'content': 'content'},
            {'attribute': ('pubdate', 'pubdate'), 'content': 'datetime'},
            {'attribute': ('name', 'publish_date'), 'content': 'content'},
        ]



        patterns = re.compile(r'(?:article.*publish|publish.*article|\bdate\b|\btime\b)')

        for tags in date_tags:
            meta_tags = doc.find_all(attrs={tags['attribute'][0]: tags['attribute'][1]})
            if meta_tags:
                str = meta_tags[0].get(tags['content'])
                datetime = parse_date(str)
                if datetime:
                    return datetime

        additional_date_tag = doc.find('div', class_=lambda c: c and patterns.search(c))
        if additional_date_tag:
            str = additional_date_tag.get_text(strip=True)
            match = date_pattern.search(str)
            if match:
                date_str, time_str = match.groups()

                # Combine date and time, then parse using dateutil.parser
                datetime_str = f"{date_str} {time_str}"
                datetime_obj = date_parser(datetime_str)
            return datetime_obj



        # If none of the strategies work, return None
        return None
    def split_title(self,title, splitter, hint=None):
        """Split the title to best part possible"""
        large_text_length = 0
        large_text_index = 0
        title_pieces = title.split(splitter)
        if hint and hint!='':
            filter_regex = re.compile(r'[^a-zA-Z0-9\ ]')
            hint = filter_regex.sub('', hint).lower()

        # find the largest title piece
        for i, title_piece in enumerate(title_pieces):
            current = title_piece.strip()
            #Immediately break if any part matches
            if hint and hint in filter_regex.sub('', current).lower():
                large_text_index = i
                break
            if len(current) > large_text_length:
                large_text_length = len(current)
                large_text_index = i

    #     Even if no part matches with hint(h1) if prints simply the longest part as the parts
    #     are usually of independent meaning
        title = title_pieces[large_text_index]
        return title
    def get_title(self,soup):
        """Explicit rules:
        1. title == h1, no need to split
        2. h1 similar to og:title, use h1
        3. title contains h1, title contains og:title, len(h1) > len(og:title), use h1
        4. title starts with og:title, use og:title
        5. use title, after splitting
        """
        title = ''
        title_element = soup.title

        # no title found
        if title_element is None or len(title_element) == 0:
            print("Error")
            return title

        # title elem found
        title_text = title_element.text
        used_delimeter = False

    #     title from h1
            # - extract the longest text from all h1 elements
        # - too short texts (fewer than 2 words) are discarded
        # - clean double spaces
    #     h1_element = soup.find_all('h1')[0]
    #     title_text_h1 = h1_element.text
        title_text_h1=''
        title_element_h1_list = soup.find_all('h1')
        title_text_h1_list = [tag.get_text(strip=True) for tag in title_element_h1_list]
        if title_text_h1_list:
            title_text_h1_list.sort(key=len, reverse=True)
            #longest title
            title_text_h1 = title_text_h1_list[0]
            # clean double spaces
            title_text_h1 = ' '.join([x for x in title_text_h1.split() if x])
        #title from meta tag(not user-visible)
        meta_tag_content = soup.find({'meta': {'property': 'og:title'}})
        if not meta_tag_content:
            meta_tag_content = soup.find({'meta': {'name': 'og:title'}})
        title_text_meta = meta_tag_content.get('content', '')  # Empty string if no meta tag found
        # Further filtering of unwanted characters
        # Alphanumeric characters, punctuation and alphanumeric
        filter_regex = re.compile(r'[^a-zA-Z0-9\ ]')
        filter_title_text = filter_regex.sub('', title_text).lower()
        filter_title_text_h1 = filter_regex.sub('', title_text_h1).lower()
        filter_title_text_meta = filter_regex.sub('', title_text_meta).lower()

        # Case1: If both matches don't do anything
        if title_text_h1 == title_text:
            used_delimeter = True
        # Case2: h1 and meta tag matches(either of h1 or meta)
        elif filter_title_text_h1 and filter_title_text_h1 == filter_title_text_meta:
            title_text = title_text_h1
            used_delimeter = True
        # Case3: If both h1 and meta are a substring of title_text(use h1)
        elif filter_title_text_h1 and filter_title_text_h1 in filter_title_text and filter_title_text_meta in filter_title_text  and len(title_text_h1) > len(title_text_meta):
            title_text = title_text_h1
            used_delimeter = True
        # Case4: If title_text startswith meta text(replace with meta)
        elif filter_title_text_meta and filter_title_text_meta != filter_title_text and filter_title_text.startswith(filter_title_text_meta):
            title_text = title_text_meta
            used_delimeter = True

        # If none of the above condition is matched, means a delimiter must be present between them
        # Now individually parts separated by delimiter has to be checked and now we check with h1 tag only(no meta tag)-Observation based
        if not used_delimeter and '|' in title_text:
            title_text = self.split_title(title_text, '|', title_text_h1)
            used_delimeter = True

        # self.split title with -
        if not used_delimeter and '-' in title_text:
            title_text = self.split_title(title_text, '-', title_text_h1)
            used_delimeter = True

        # self.split title with _
        if not used_delimeter and '_' in title_text:
            title_text = self.split_title(title_text, '_', title_text_h1)
            used_delimeter = True

        # self.split title with /
        if not used_delimeter and '/' in title_text:
            title_text = self.split_title(title_text, '/', title_text_h1)
            used_delimeter = True

        # self.split title with »
        if not used_delimeter and ' » ' in title_text:
            title_text = self.split_title(title_text, ' » ', title_text_h1)
            used_delimeter = True
        return title_text
