from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
	api_key=os.getenv('OPENAI_API_KEY')
)

def get_ai_completions(prompt: str) -> str:
	response = client.chat.completions.create(
		model='gpt-4o-mini',
		messages=[
			{
				'role': 'system',
				'content': '''
					You're a data entry professional who converts plain text into json format.
					Your response must contain only valid json data, without any text before or after it.
					Your response should start with an opening curly brace ({) and end with a closing curly brace (}).
				'''.strip().replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
			},
			{'role': 'user', 'content': prompt}
		],
	)

	return response.choices[0].message.content

if __name__ == '__main__':
	print(get_ai_completions('Convert this plain text into json format: name: John Doe, age: 30, location: New York, job: Software Engineer'))
