
import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from LLM_Helper import llm




def process_post(raw_file_path, processed_file_path = "data\processed_posts.json" ):
    extracted_post = []
    with open(raw_file_path, encoding='utf-8' ) as f:
        posts = json.load(f)
        
        for post in posts:
            meta_data = extract_metadata( post['text'])

            # we will join the meta_data and text in one json
            post_with_metadata = post | meta_data # pype operator we will store in seperate list

            extracted_post.append(post_with_metadata) # adding post text and meta data together

        with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
            json.dump(extracted_post, outfile, indent=4)

    

def extract_metadata(post): # this function extracts some additional data from each linedin post it will be done by a llm as pre process steps
    pt = PromptTemplate(template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language and tags. 
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)
    
    Here is the actual post on which you need to perform this task:  
    {post}
    ''', input_variables=[{post}])

    
    chain = pt | llm
    response = chain.invoke(input={"post": post})
    
    try:

        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Content too big. Unable to parse jobs")

    return res






if __name__ == "__main__":
    process_post(r"data\raw_post.json", r"data\processed_posts.json")