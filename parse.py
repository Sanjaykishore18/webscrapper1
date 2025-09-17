import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Set your Gemini / Google Generative AI API key
# It’s better to store in env var rather than hard-code
os.environ["GOOGLE_API_KEY"] = "AIzaSyAB7VWGfRZr4gLc7lzy5pNgzVUwqhyEBmg"

# Define the common template
template = """
You are tasked with extracting specific information from the following DOM text content:

{dom_content}

Please follow these rules carefully:
1. **Extract Information Only** – Only include information that directly matches the description provided below.
2. **No Extra Content** – Do not add explanations, commentary, or unrelated details.
3. **Empty Response** – If no matching information is found, return an empty string ("").
4. **Direct Data Only** – Output should contain only the raw data requested, without formatting or additional text.

Information to extract:
{parse_description}
"""

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",   # pick desired Gemini model, e.g. "gemini-pro" etc.
    temperature=0.1,
    # optionally you can pass google_api_key here instead of using env var:
    # google_api_key="AIzaSyAB7VWGfRZr4gLc7lzy5pNgzVUwqhyEBmg"
)

def parse_with_gemini(dom_chunks, parse_description):
    # Create prompt template
    prompt = ChatPromptTemplate.from_template(template)
    # Compose chain: prompt -> llm
    chain = prompt | llm

    parsed_result = []
    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({
            "dom_content": chunk,
            "parse_description": parse_description
        })
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        # Depending on the API, response may be in `.content` or similar
        # In langchain-google-genai, .invoke returns an object with .content
        # But when using chain, often response is the raw string in `.content`
        try:
            parsed_text = response.content
        except AttributeError:
            # maybe it’s a raw string already
            parsed_text = response
        parsed_result.append(parsed_text)

    return "\n".join(parsed_result)

# Example usage
if __name__ == "__main__":
    dom_chunks = [
        "<div>Name: Alice<br>Age: 30</div>",
        "<div>No relevant info here</div>",
    ]
    parse_description = "Name and Age"
    result = parse_with_gemini(dom_chunks, parse_description)
    print("Final result:")
    print(result)
