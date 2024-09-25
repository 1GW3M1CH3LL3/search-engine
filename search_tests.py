from search import keyword_to_titles, title_to_info, search, article_length,key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):


    ##############
    # UNIT TESTS #
    ##############

    # def test_example_unit_test(self):
    #     dummy_keyword_dict = {
    #         'cat': ['title1', 'title2', 'title3'],
    #         'dog': ['title3', 'title4']
    #     }
    #     expected_search_results = ['title3', 'title4']
    #     self.assertEqual(search('dog', dummy_keyword_dict), expected_search_results)
        def test_keyword_to_titles(self):
                metadata = [["Wake Forest Demon Deacons men's soccer", 'Burna Boy', 1260577388, 26745, ['the']]]
                expected_output = {'the': ["Wake Forest Demon Deacons men's soccer"] }
                self.assertEqual(keyword_to_titles(metadata), expected_output)
                metadata = [["Wake Forest Demon Deacons men's soccer", 'Burna Boy', 1260577388, 26745, ['the', 'ThE']]]
                expected_output = {'the': ["Wake Forest Demon Deacons men's soccer"], 'ThE': ["Wake Forest Demon Deacons men's soccer"]}
                self.assertEqual(keyword_to_titles(metadata), expected_output)
                metadata = [["Wake Forest Demon Deacons men's soccer", 'Burna Boy', 1260577388, 26745, []]]
                expected_output = {}
                self.assertEqual(keyword_to_titles(metadata), expected_output)

        def test_title_to_info(self):
                metadata = [["Wake Forest Demon Deacons men's soccer", 'Burna Boy',
                1260577388, 26745, ['the', 'mls', 'usl', 'united', '2013']]]
                expected_output = {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745}}
                self.assertEqual(title_to_info(metadata), expected_output)  
                metadata = [["Wake Forest Demon Deacons men's soccer", 'Burna Boy',
                1260577388, 26745, ['the', 'mls', 'usl', 'united', '2013']], ['Harry Potter', 'ada',
                2309090909, 1609, ['ron', 'hermoine']]]
                expected_output = {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745},
                'Harry Potter': {'author': 'ada', 'timestamp': 2309090909, 'length': 1609 }}
                self.assertEqual(title_to_info(metadata), expected_output) 
                metadata = []
                expected_output = {}
                self.assertEqual(title_to_info(metadata), expected_output) 

        def test_search(self):
                keyword = 'the' 
                keyword_to_titles = {'the': ["Wake Forest Demon Deacons men's soccer"] }  
                expected_output = ["Wake Forest Demon Deacons men's soccer"]   
                self.assertEqual(search(keyword, keyword_to_titles), expected_output)  
                keyword = 'october' 
                keyword_to_titles = {'the': ["Wake Forest Demon Deacons men's soccer"] }  
                expected_output = []   
                self.assertEqual(search(keyword, keyword_to_titles), expected_output)  
                keyword = '' 
                keyword_to_titles = {'the': ["Wake Forest Demon Deacons men's soccer"] }  
                expected_output = []   
                self.assertEqual(search(keyword, keyword_to_titles), expected_output)

        def test_article_length(self):
                max_length = 1200
                title_to_info =  {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745}}
                article_titles = ["Wake Forest Demon Deacons men's soccer"]
                expected_output = []
                self.assertEqual(article_length(max_length, article_titles, title_to_info), expected_output) 
                max_length = 1260577390
                title_to_info = {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745}}
                article_titles = ["Wake Forest Demon Deacons men's soccer"]
                expected_output = article_titles 
                self.assertEqual(article_length(max_length, article_titles, title_to_info), expected_output)
                max_length = 0
                title_to_info = {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745}}
                article_titles = ["Wake Forest Demon Deacons men's soccer"]
                expected_output = [] 
                self.assertEqual(article_length(max_length, article_titles, title_to_info), expected_output) 

        def test_key_by_author(self):
                article_titles = ['Harry Potter']
                title_to_info = {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745},
                'Harry Potter': {'author': 'ada', 'timestamp': 2309090909, 'length': 1609 }}
                expected_output = {'ada': ['Harry Potter']}
                self.assertEqual(key_by_author(article_titles, title_to_info), expected_output)
                article_titles = ['Harry Potter','Socerers Stone']
                title_to_info = {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745},
                'Harry Potter': {'author': 'ada', 'timestamp': 2309090909, 'length': 1609 }, 'Socerers Stone': {'author': 'Ada', 'timestamp': 2309090909, 'length': 1609 }}
                expected_output = {'ada': ['Harry Potter'], 'Ada': ['Socerers Stone']}
                self.assertEqual(key_by_author(article_titles, title_to_info), expected_output)
                article_titles = []
                title_to_info = {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745},
                'Harry Potter': {'author': 'ada', 'timestamp': 2309090909, 'length': 1609 }, 'Socerers Stone': {'author': 'Ada', 'timestamp': 2309090909, 'length': 1609 }}
                expected_output = {}
                self.assertEqual(key_by_author(article_titles, title_to_info), expected_output)

        def test_filter_to_author(self):
                author = 'ada'    
                article_titles = ['Harry Potter','Socerers Stone', "Wake Forest Demon Deacons men's soccer"]
                title_to_info = {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745},
                'Harry Potter': {'author': 'ada', 'timestamp': 2309090909, 'length': 1609 }, 'Socerers Stone': {'author': 'Ada', 'timestamp': 2309090909, 'length': 1609 }}
                expected_output = ['Harry Potter']
                self.assertEqual(filter_to_author(author, article_titles, title_to_info), expected_output)
                author = 'women'    
                article_titles = ['Harry Potter','Socerers Stone', "Wake Forest Demon Deacons men's soccer"]
                title_to_info = {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745},
                'Harry Potter': {'author': 'ada', 'timestamp': 2309090909, 'length': 1609 }, 'Socerers Stone': {'author': 'Ada', 'timestamp': 2309090909, 'length': 1609 }}
                expected_output = []
                self.assertEqual(filter_to_author(author, article_titles, title_to_info), expected_output)
                author = ''    
                article_titles = ['Harry Potter','Socerers Stone', "Wake Forest Demon Deacons men's soccer"]
                title_to_info = {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745},
                'Harry Potter': {'author': 'ada', 'timestamp': 2309090909, 'length': 1609 }, 'Socerers Stone': {'author': 'Ada', 'timestamp': 2309090909, 'length': 1609 }}
                expected_output = []
                self.assertEqual(filter_to_author(author, article_titles, title_to_info), expected_output)

        def test_filter_out(self):
                keyword = 'the'
                article_titles =  ['Harry Potter','Socerers Stone', "Wake Forest Demon Deacons men's soccer"]
                keyword_to_titles = {'the': ["Wake Forest Demon Deacons men's soccer"], 'ThE': ["Wake Forest Demon Deacons men's soccer"]}
                expected_output = ['Harry Potter', 'Socerers Stone']
                self.assertEqual(filter_out(keyword, article_titles, keyword_to_titles), expected_output)
                keyword = 'the'
                article_titles =  ['Harry Potter','Socerers Stone', "Wake Forest Demon Deacons men's soccer"]
                keyword_to_titles = {'the': ["there"], 'ThE': ["Wake Forest Demon Deacons men's soccer"]}
                expected_output = ['Harry Potter', 'Socerers Stone', "Wake Forest Demon Deacons men's soccer"]
                self.assertEqual(filter_out(keyword, article_titles, keyword_to_titles), expected_output)  
                keyword = ''
                article_titles =  ['Harry Potter','Socerers Stone', "Wake Forest Demon Deacons men's soccer"]
                keyword_to_titles = {'the': ["there"], 'ThE': ["Wake Forest Demon Deacons men's soccer"]}
                expected_output = ['Harry Potter', 'Socerers Stone', "Wake Forest Demon Deacons men's soccer"]
                self.assertEqual(filter_out(keyword, article_titles, keyword_to_titles), expected_output)  

        def test_articles_from_year(self):
                year = 2009
                article_titles = ["Wake Forest Demon Deacons men's soccer"]
                title_to_info = {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745},
                'Harry Potter': {'author': 'ada', 'timestamp': 2309090909, 'length': 1609 }, 'Socerers Stone': {'author': 'Ada', 'timestamp': 2309090909, 'length': 1609 }}
                expected_output = ["Wake Forest Demon Deacons men's soccer"]
                self.assertEqual(articles_from_year(year, article_titles, title_to_info), expected_output)   
                year = 2023
                article_titles = ["Wake Forest Demon Deacons men's soccer"]
                title_to_info = {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745},
                'Harry Potter': {'author': 'ada', 'timestamp': 2309090909, 'length': 1609 }, 'Socerers Stone': {'author': 'Ada', 'timestamp': 2309090909, 'length': 1609 }}
                expected_output = []
                self.assertEqual(articles_from_year(year, article_titles, title_to_info), expected_output)     
                year = 1200
                article_titles = ["Wake Forest Demon Deacons men's soccer"]
                title_to_info = {"Wake Forest Demon Deacons men's soccer": {'author': 'Burna Boy', 'timestamp': 1260577388, 'length': 26745},
                'Harry Potter': {'author': 'ada', 'timestamp': 2309090909, 'length': 1609 }, 'Socerers Stone': {'author': 'Ada', 'timestamp': 2309090909, 'length': 1609 }}
                expected_output = []
                self.assertEqual(articles_from_year(year, article_titles, title_to_info), expected_output)        
    #####################
    #####################
    # INTEGRATION TESTS #
    #####################

        @patch('builtins.input')
        def test_example_integration_test(self, input_mock):
                keyword = 'soccer'
                advanced_option = 5
                advanced_response = 2009

                output = get_print(input_mock, [keyword, advanced_option, advanced_response])
                expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

                self.assertEqual(output, expected)
        @patch('builtins.input')
        def test_run_article_length(self, input_mock):
                keyword = 'soccer'
                advanced_option = 1
                advanced_response = 20000

                output = get_print(input_mock, [keyword, advanced_option, advanced_response])
                expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)']\n"

                self.assertEqual(output, expected)

        @patch('builtins.input')
        def test_run_key_by_author(self, input_mock):
                keyword = 'soccer'
                advanced_option = 2
              

                output = get_print(input_mock, [keyword, advanced_option])
                expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: {'jack johnson': ['Spain national beach soccer team'], 'Burna Boy': ['Will Johnson (soccer)'], 'Mack Johnson': ['Steven Cohen (soccer)']}\n"

                self.assertEqual(output, expected)        

        @patch('builtins.input')
        def test_run_filter_out_keyword(self, input_mock):
                keyword = 'soccer'
                advanced_option = 4
                advanced_response = 'beach'
              

                output = get_print(input_mock, [keyword, advanced_option, advanced_response])
                expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) +  str(advanced_response) + "\n\nHere are your articles: ['Will Johnson (soccer)', 'Steven Cohen (soccer)']\n"

                self.assertEqual(output, expected)        

        @patch('builtins.input')
        def test_run_none(self, input_mock):
                keyword = 'fisk'
                advanced_option = 6
                
              

                output = get_print(input_mock, [keyword, advanced_option])
                expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: ['Fisk University']\n"
                self.assertEqual(output, expected)
        

# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()
