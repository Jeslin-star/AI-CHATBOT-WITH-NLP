import nltk
from nltk.stem import WordNetLemmatizer
from difflib import get_close_matches

# === Download wordnet only once ===
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# === Intent Categories ===
intents = {
    "greeting": ["hello", "hi", "good morning", "good evening", "hey"],
    "goodbye": ["bye", "goodbye", "exit", "see you", "farewell"],
    "thanks": ["thank you", "thanks", "thx"],
    "education": [
        "what is ai", "what is machine learning", "define python",
        "what is chatbot", "explain programming", "define algorithm"
    ],
    "science": [
        "what is gravity", "what is atom", "explain photosynthesis",
        "define force", "what is energy", "what is cell"
    ],
    "tech": [
        "what is internet", "what is cloud computing", "what is cyber security",
        "explain database", "what is operating system", "define software"
    ],
    "gk": [
        "who is prime minister of india", "capital of france", 
        "largest ocean", "tallest mountain", "who invented telephone"
    ],
    "history": [
        "who is mahatma gandhi", "when india got independence",
        "what is world war 2", "who was hitler", "who was nelson mandela"
    ],
    "geography": [
        "capital of japan", "largest desert", "longest river",
        "smallest country", "highest waterfall"
    ]
}

# === Response Knowledge Base ===
responses = {
    "greeting": "Hello. I am your assistant. How may I help you today?",
    "goodbye": "Thank you for the conversation. Wishing you a wonderful day ahead.",
    "thanks": "You're welcome. I'm always here to assist you.",
    
    "education": {
        "what is ai": "Artificial Intelligence is the ability of machines to simulate human intelligence.",
        "what is machine learning": "Machine Learning is a field of AI that helps machines learn from data.",
        "define python": "Python is a powerful, high-level programming language used in many areas including AI and web development.",
        "what is chatbot": "A chatbot is an AI program that can simulate a human conversation.",
        "explain programming": "Programming is the process of writing instructions that a computer can understand and execute.",
        "define algorithm": "An algorithm is a step-by-step procedure for solving a problem or performing a task."
    },

    "science": {
        "what is gravity": "Gravity is the force by which a planet or other body draws objects toward its center.",
        "what is atom": "An atom is the smallest unit of ordinary matter that forms a chemical element.",
        "explain photosynthesis": "Photosynthesis is the process by which green plants make their food using sunlight, carbon dioxide, and water.",
        "define force": "Force is a push or pull on an object resulting from the object's interaction with another object.",
        "what is energy": "Energy is the ability to do work. It exists in various forms such as kinetic, potential, thermal, etc.",
        "what is cell": "A cell is the basic structural, functional, and biological unit of all known living organisms."
    },

    "tech": {
        "what is internet": "The Internet is a global network of computers that communicate using standardized protocols.",
        "what is cloud computing": "Cloud computing is the delivery of computing services over the internet on-demand.",
        "what is cyber security": "Cyber security is the practice of protecting systems, networks, and data from digital attacks.",
        "explain database": "A database is an organized collection of data that can be accessed, managed, and updated.",
        "what is operating system": "An operating system is system software that manages computer hardware and software resources.",
        "define software": "Software is a set of instructions or programs used to operate computers and execute specific tasks."
    },

    "gk": {
        "who is prime minister of india": "As of 2025, the Prime Minister of India is Narendra Modi.",
        "capital of france": "The capital of France is Paris.",
        "largest ocean": "The largest ocean on Earth is the Pacific Ocean.",
        "tallest mountain": "Mount Everest is the tallest mountain in the world.",
        "who invented telephone": "Alexander Graham Bell is credited with inventing the first practical telephone."
    },

    "history": {
        "who is mahatma gandhi": "Mahatma Gandhi was a leader of India’s non-violent independence movement against British rule.",
        "when india got independence": "India gained independence from British rule on August 15, 1947.",
        "what is world war 2": "World War II was a global war from 1939 to 1945 involving most of the world’s nations.",
        "who was hitler": "Adolf Hitler was a German dictator and leader of the Nazi Party responsible for WWII and the Holocaust.",
        "who was nelson mandela": "Nelson Mandela was a South African leader who fought against apartheid and became the country's first black president."
    },

    "geography": {
        "capital of japan": "The capital of Japan is Tokyo.",
        "largest desert": "The largest desert in the world is the Antarctic Desert.",
        "longest river": "The longest river in the world is the Nile River.",
        "smallest country": "The smallest country in the world is Vatican City.",
        "highest waterfall": "The highest waterfall in the world is Angel Falls in Venezuela."
    }
}

# === Intent Detection (exact + fuzzy match) ===
def classify_intent(user_input):
    user_input = user_input.lower().strip()
    tokens = [lemmatizer.lemmatize(w) for w in user_input.split()]

    for intent, keywords in intents.items():
        for phrase in keywords:
            if user_input == phrase:
                return intent, phrase

        # Fuzzy match for close spelling
        match = get_close_matches(user_input, keywords, n=1, cutoff=0.85)
        if match:
            return intent, match[0]

    return "unknown", ""

# === Generate Response (with final changes) ===
def generate_response(user_input):
    user_input = user_input.lower().strip()

    # Handle "all science", etc.
    if user_input.startswith("all "):
        category = user_input.replace("all ", "").strip()
        if category in responses and isinstance(responses[category], dict):
            full_response = ""
            for q, a in responses[category].items():
                full_response += f"{q.title()}\n{a}\n\n"
            return full_response.strip()

    intent, keyword = classify_intent(user_input)

    if intent in ["greeting", "goodbye", "thanks"]:
        return responses[intent]
    elif intent in responses and keyword in responses[intent]:
        return responses[intent][keyword]
    elif len(user_input.split()) <= 2:  # Very short or meaningless
        return "Oops! Something went wrong in your prompt."
    else:
        return "I'm still learning. Could you please rephrase your question?"

# === Chat Starts Here ===
print("Serious Knowledge Chatbot is active.\n(Type 'exit' or 'bye' to end the chat)\n")

while True:
    try:
        user_input = input("You: ")
        if user_input.lower().strip() in ["exit", "bye", "quit"]:
            print("Bot:", responses["goodbye"])
            break
        response = generate_response(user_input)
        print("Bot:", response)
    except Exception as e:
        print("Bot: Oops! Something went wrong:", e)
