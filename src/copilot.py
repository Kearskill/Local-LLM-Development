import ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Load our local KB
embeddings = OllamaEmbeddings(model="nomic-embed-text")
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)


def search_kb(query: str):
    """Searches the internal IT Knowledge Base for troubleshooting steps."""
    results = db.similarity_search(query, k=2)
    return "\n".join([r.page_content for r in results])


def create_ticket(summary: str, severity: str):
    """Creates a support ticket in the internal system."""
    # In a real app, this would be a POST request to Jira/ServiceNow
    return f"SUCCESS: Ticket created. [Summary: {summary}, Severity: {severity}]"


def chat():
    messages = [{"role": "system",
                 "content": "You are a helpful IT Desk Copilot. Use tools to find info. If you find a solution, draft a reply for the user. Never ask for passwords."}]

    while True:
        user_input = input("\nUser: ")
        messages.append({"role": "user", "content": user_input})

        # Call the model with tool definitions
        response = ollama.chat(
            model='llama3.1',
            messages=messages,
            tools=[search_kb, create_ticket],
        )

        # Check if the model wants to use a tool
        if response['message'].get('tool_calls'):
            for tool in response['message']['tool_calls']:
                print(f"--- Running Tool: {tool['function']['name']} ---")

                # Logic to execute the function
                if tool['function']['name'] == 'search_kb':
                    obs = search_kb(tool['function']['arguments']['query'])
                elif tool['function']['name'] == 'create_ticket':
                    args = tool['function']['arguments']
                    obs = create_ticket(args['summary'], args['severity'])

                # Feed the tool output back to the model
                messages.append(response['message'])
                messages.append({'role': 'tool', 'content': obs})

            # Get final response after tool execution
            final_response = ollama.chat(model='llama3.1', messages=messages)
            print(f"Copilot: {final_response['message']['content']}")
        else:
            print(f"Copilot: {response['message']['content']}")


if __name__ == "__main__":
    chat()