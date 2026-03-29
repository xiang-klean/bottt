import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import re
import math
import random
import sys
from collections import Counter

# ============================================================
#  FLASK WEB SERVER  (NEW)
# ============================================================
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder=".")
CORS(app)

# ============================================================
#  FIREBASE CONFIG
# ============================================================
cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

COL_INTENTS   = "intents"
COL_PATTERNS  = "training_data"
COL_RESPONSES = "responses"
COL_HISTORY   = "chat_history"


# ============================================================
#  1. DATABASE LAYER (Firebase Firestore)
# ============================================================

def init_db():
    print("[DB] Firebase Firestore ready.")


def seed_data():
    existing = db.collection(COL_INTENTS).limit(1).get()
    if len(existing) > 0:
        return

    print("[DB] Seeding programming training data...")

    INTENTS = [
        {
            "tag": "greeting",
            "description": "Welcome",
            "patterns": [
                "hello", "hi", "hey", "hi there", "hello there",
                "good morning", "good afternoon", "good evening",
                "howdy", "greetings", "what's up", "sup",
                "hi bot", "hello bot", "hey chatbot", "hey bot",
                "start", "begin", "wake up",
            ],
            "responses": [
                "👨‍💻 Hello! I'm your Programming AI Tutor!\n\nI can teach you:\n🐍 Python Basics        🔷 OOP & Design Patterns\n📦 Data Structures      🔍 Algorithms\n🧠 Problem Solving      💡 Best Practices\n\nWhat would you like to learn today?",
                "🚀 Welcome to your Programming Tutor!\n\nAsk me about:\n• Python   • OOP   • Data Structures   • Algorithms\n\nType 'help' to see all topics!",
            ]
        },
        {
            "tag": "goodbye",
            "description": "Farewell",
            "patterns": [
                "bye", "goodbye", "see you", "see you later",
                "farewell", "take care", "good night", "gotta go",
                "i'm done", "done", "stop", "end", "finish", "exit", "quit",
            ],
            "responses": [
                "👋 Goodbye! Keep coding every day!\nPractice makes perfect — you've got this! 🚀",
                "✌️ See you! Remember: the best way to learn programming is to BUILD things!\nHappy coding! 💻",
            ]
        },
        {
            "tag": "python_basics",
            "description": "Python fundamentals",
            "patterns": [
                "python", "python basics", "python fundamentals",
                "learn python", "python beginner", "start python",
                "python intro", "python introduction",
                "variable", "variables", "data type", "data types",
                "string", "integer", "float", "boolean",
                "int", "str", "bool", "type",
                "assign variable", "declare variable",
                "print", "input", "output", "print function",
                "how to print", "user input",
                "operator", "operators", "arithmetic", "arithmetic operator",
                "comparison operator", "logical operator",
                "addition", "subtraction", "multiplication", "division",
                "modulo", "floor division", "exponent",
                "if", "if else", "elif", "condition", "conditional",
                "nested if", "ternary",
                "loop", "loops", "for loop", "while loop",
                "iteration", "iterate", "range", "break", "continue",
                "nested loop",
                "function", "functions", "def", "return",
                "parameter", "argument", "default parameter",
                "lambda", "anonymous function",
                "string method", "string methods", "string slicing",
                "f-string", "format string", "string concatenation",
                "split", "join", "strip", "upper", "lower",
                "list", "lists", "append", "remove", "sort", "reverse",
                "tuple", "tuples", "list comprehension",
                "slice", "index",
                "dictionary", "dict", "key value", "keys", "values",
                "set", "sets", "set operations",
                "file", "files", "open file", "read file", "write file",
                "with open", "file handling",
                "error", "exception", "try except", "try catch",
                "raise", "finally", "error handling",
                "module", "modules", "import", "library",
                "pip", "install package", "math module", "random module",
            ],
            "responses": [
                "🐍 **Python Basics — The Foundation!**\n\n📌 **Variables & Data Types**\n```python\nname    = 'Alice'      # str\nage     = 21           # int\ngpa     = 3.85         # float\npassed  = True         # bool\n```\n\n📌 **Control Flow**\n```python\nif age >= 18:\n    print('Adult')\nelif age >= 13:\n    print('Teenager')\nelse:\n    print('Child')\n```\n\n📌 **Loops**\n```python\nfor i in range(5):         # 0,1,2,3,4\n    print(i)\n\nwhile count < 10:\n    count += 1\n```\n\n📌 **Functions**\n```python\ndef add(a, b=0):            # default param\n    return a + b\n\nresult = add(3, 4)          # → 7\ndouble = lambda x: x * 2   # lambda\n```\n\n📌 **Lists & Dicts**\n```python\nfruits = ['apple', 'banana']\nfruits.append('cherry')\nevens  = [x for x in range(10) if x%2==0]\n\nstudent = {'name': 'Alice', 'age': 21}\nprint(student['name'])      # → Alice\n```\n\n📌 **Error Handling**\n```python\ntry:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero!')\nfinally:\n    print('Done.')\n```\n\n💡 Ask about a SPECIFIC topic for deeper explanation!\ne.g. 'list comprehension', 'lambda', 'file handling'",
            ]
        },
        {
            "tag": "oop",
            "description": "Object-Oriented Programming & Design Patterns",
            "patterns": [
                "oop", "object oriented", "object-oriented",
                "class", "classes", "object", "objects",
                "instance", "instantiate", "constructor", "__init__",
                "self", "attribute", "attributes", "method", "methods",
                "property", "getter", "setter", "@property",
                "encapsulation", "abstraction", "inheritance", "polymorphism",
                "four pillars", "pillars of oop",
                "inherit", "subclass", "superclass", "parent class", "child class",
                "extend", "override", "super()", "multiple inheritance",
                "mro", "method resolution order",
                "overriding", "duck typing", "interface",
                "abstract", "abstract class", "abc", "abstract method",
                "magic method", "dunder", "__str__", "__repr__",
                "__len__", "__eq__", "__add__", "operator overloading",
                "design pattern", "design patterns", "pattern",
                "creational pattern", "structural pattern", "behavioral pattern",
                "singleton", "factory", "factory method", "abstract factory",
                "builder pattern", "prototype pattern",
                "decorator pattern", "adapter pattern", "facade pattern",
                "proxy pattern", "composite pattern",
                "observer pattern", "strategy pattern", "command pattern",
                "iterator pattern", "template method",
                "solid", "solid principles",
                "single responsibility", "srp",
                "open closed", "ocp",
                "liskov", "lsp",
                "interface segregation", "isp",
                "dependency inversion", "dip",
            ],
            "responses": [
                "🔷 **OOP & Design Patterns — Write Professional Code!**\n\n📌 **Class & Object Basics**\n```python\nclass Animal:\n    def __init__(self, name, sound):\n        self.name  = name\n        self.sound = sound\n\n    def speak(self):\n        return f'{self.name} says {self.sound}!'\n\n    def __str__(self):\n        return f'Animal({self.name})'\n\ndog = Animal('Rex', 'Woof')\nprint(dog.speak())  # → Rex says Woof!\n```\n\n📌 **4 Pillars of OOP**\n🔒 **Encapsulation**  → hide internal data with _private\n🎭 **Abstraction**    → expose only what's necessary\n👪 **Inheritance**    → child class reuses parent code\n🎨 **Polymorphism**   → same method, different behaviour\n\n📌 **Inheritance**\n```python\nclass Dog(Animal):\n    def fetch(self, item):\n        return f'{self.name} fetches {item}!'\n\n    def speak(self):  # override\n        return 'Woof! Woof!'\n```\n\n📌 **Design Patterns**\n🏭 **Singleton** → only ONE instance exists\n🏗️ **Factory**  → create objects without specifying class\n👁️ **Observer** → notify many objects on state change\n🎯 **Strategy** → swap algorithms at runtime\n\n📌 **SOLID Principles**\nS — Single Responsibility: 1 class = 1 job\nO — Open/Closed: open for extension, closed for modification\nL — Liskov: subclass must be substitutable for parent\nI — Interface Segregation: don't force unused methods\nD — Dependency Inversion: depend on abstractions\n\n💡 Ask about a specific pattern: 'singleton', 'factory', 'observer'",
            ]
        },
        {
            "tag": "data_structures",
            "description": "Data Structures",
            "patterns": [
                "data structure", "data structures", "ds",
                "what is data structure", "data structure basics",
                "array", "arrays", "linked list",
                "singly linked list", "doubly linked list",
                "stack", "stacks", "push", "pop", "peek",
                "queue", "queues", "enqueue", "dequeue", "fifo", "lifo",
                "deque", "double ended queue",
                "tree", "trees", "binary tree", "bst",
                "binary search tree", "avl tree", "red black tree",
                "heap", "min heap", "max heap", "priority queue",
                "graph", "graphs", "node", "edge", "vertex",
                "directed graph", "undirected graph", "weighted graph",
                "hash", "hash table", "hash map", "hashing",
                "collision", "chaining", "open addressing",
                "trie", "segment tree", "fenwick tree",
                "which data structure", "when to use",
                "best data structure", "choose data structure",
            ],
            "responses": [
                "📦 **Data Structures — Organise Your Data!**\n\n📌 **Array / List** — O(1) access, O(n) insert\n```python\narr = [10, 20, 30, 40]\narr[0]           # → 10  (O(1))\narr.append(50)   # O(1) amortised\narr.insert(2,99) # O(n) shift\n```\n\n📌 **Stack** — LIFO | push/pop O(1)\n```python\nstack = []\nstack.append(1)  # push\nstack.pop()      # → last in, first out\n# Use for: undo, brackets check, DFS\n```\n\n📌 **Queue** — FIFO | enqueue/dequeue O(1)\n```python\nfrom collections import deque\nq = deque()\nq.append(1)      # enqueue\nq.popleft()      # → first in, first out\n# Use for: BFS, task scheduling\n```\n\n📌 **Hash Table / Dict** — O(1) avg lookup\n```python\ntable = {}\ntable['alice'] = 90  # O(1) insert\ntable['alice']       # O(1) lookup\n```\n\n📌 **BST Rule**: left < root < right\nSearch / Insert / Delete: O(log n) balanced\n\n📊 **Quick Comparison**\n| Structure   | Access | Search | Insert |\n|-------------|--------|--------|--------|\n| Array       | O(1)   | O(n)   | O(n)   |\n| Linked List | O(n)   | O(n)   | O(1)   |\n| Hash Table  | O(1)   | O(1)   | O(1)   |\n| BST (bal.)  | O(logn)| O(logn)| O(logn)|\n\n💡 Ask: 'stack', 'queue', 'linked list', 'binary tree', 'graph'",
            ]
        },
        {
            "tag": "algorithms",
            "description": "Algorithms & Problem Solving",
            "patterns": [
                "algorithm", "algorithms", "algo",
                "problem solving", "problem-solving",
                "complexity", "time complexity", "space complexity",
                "big o", "big-o", "o notation", "asymptotic",
                "sort", "sorting", "sorting algorithm",
                "bubble sort", "selection sort", "insertion sort",
                "merge sort", "quick sort", "heap sort",
                "counting sort", "radix sort", "bucket sort",
                "fastest sort", "best sorting algorithm",
                "search", "searching", "search algorithm",
                "linear search", "binary search",
                "how to search", "find element",
                "recursion", "recursive", "base case",
                "fibonacci", "factorial", "tower of hanoi",
                "call stack", "stack overflow",
                "bfs", "breadth first search", "breadth-first",
                "dfs", "depth first search", "depth-first",
                "dijkstra", "shortest path", "minimum spanning tree",
                "bellman ford", "floyd warshall",
                "topological sort", "cycle detection",
                "dynamic programming", "dp",
                "memoization", "tabulation", "bottom up", "top down",
                "knapsack", "longest common subsequence", "lcs",
                "coin change", "fibonacci dp",
                "greedy", "greedy algorithm",
                "divide and conquer", "divide conquer",
                "two pointer", "two pointers", "sliding window",
                "backtracking", "n queens", "sudoku solver",
                "permutation", "combination",
            ],
            "responses": [
                "🔍 **Algorithms & Problem Solving!**\n\n📌 **Big-O Complexity** (Best → Worst)\n```\nO(1)       → Constant    (hash lookup)\nO(log n)   → Logarithmic (binary search)\nO(n)       → Linear      (linear search)\nO(n log n) → Linearithmic (merge sort)\nO(n²)      → Quadratic   (bubble sort)\nO(2ⁿ)      → Exponential (naive fibonacci)\n```\n\n📌 **Bubble Sort** — O(n²)\n```python\ndef bubble_sort(arr):\n    for i in range(len(arr)):\n        for j in range(len(arr)-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n```\n\n📌 **Binary Search** — O(log n)\n```python\ndef binary_search(arr, target):\n    lo, hi = 0, len(arr) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: lo = mid + 1\n        else:                   hi = mid - 1\n    return -1\n```\n\n📌 **Recursion** — Base Case + Recursive Case\n```python\ndef factorial(n):\n    if n == 0: return 1       # base case\n    return n * factorial(n-1) # recursive\n\ndef fibonacci(n, memo={}):\n    if n <= 1: return n\n    if n in memo: return memo[n]\n    memo[n] = fibonacci(n-1,memo) + fibonacci(n-2,memo)\n    return memo[n]\n```\n\n📌 **BFS** — level by level, uses Queue\n```python\nfrom collections import deque\ndef bfs(graph, start):\n    visited, queue = set(), deque([start])\n    while queue:\n        node = queue.popleft()\n        if node not in visited:\n            visited.add(node)\n            queue.extend(graph[node])\n```\n\n💡 Ask: 'bubble sort', 'binary search', 'bfs', 'dynamic programming'",
            ]
        },
        {
            "tag": "tips",
            "description": "Programming tips and best practices",
            "patterns": [
                "tip", "tips", "best practice", "best practices",
                "clean code", "good code", "code quality",
                "how to become better programmer", "improve coding",
                "coding advice", "programming advice",
                "debug", "debugging", "how to debug",
                "read error", "understand error", "fix bug",
                "naming convention", "variable naming",
                "comment", "comments", "documentation", "docstring",
                "refactor", "refactoring", "dry", "don't repeat yourself",
                "kiss", "yagni", "code smell",
                "version control", "git", "github",
                "practice", "leetcode", "hackerrank", "project",
                "portfolio", "build project",
            ],
            "responses": [
                "💡 **Programming Tips & Best Practices!**\n\n📌 **Clean Code Principles**\n✅ DRY   — Don't Repeat Yourself\n✅ KISS  — Keep It Simple, Stupid\n✅ YAGNI — You Aren't Gonna Need It\n\n```python\n# BAD\nx = 3.14159  # magic number\ndef f(a, b): return a + b  # vague name\n\n# GOOD\nPI = 3.14159\ndef add_numbers(first, second): return first + second\n```\n\n📌 **Naming Conventions (PEP8)**\n```\nvariables  → snake_case      (my_variable)\nfunctions  → snake_case      (calculate_total)\nclasses    → PascalCase      (StudentRecord)\nconstants  → UPPER_CASE      (MAX_SIZE)\nprivate    → _underscore     (_internal)\n```\n\n📌 **Debugging Strategy**\n1. READ the error message carefully\n2. IDENTIFY the line number\n3. ADD print() / use debugger\n4. Google the exact error message\n5. Rubber duck debug (explain to yourself)\n\n**Common Python Errors:**\n```\nSyntaxError    → typo / missing colon\nNameError      → variable not defined\nTypeError      → wrong type operation\nIndexError     → list index out of range\nKeyError       → dict key doesn't exist\n```\n\n📌 **How to Get Better FAST**\n1. 🏗️ BUILD projects (not just tutorials)\n2. 🧩 Solve 1 LeetCode problem/day\n3. 📖 Read code on GitHub\n4. 🔁 Refactor your old code\n5. 🤝 Pair programming / teach others\n\n**Roadmap:** Python Basics → DSA → OOP → Projects → Open Source",
            ]
        },
        {
            "tag": "thanks",
            "description": "Appreciation",
            "patterns": [
                "thank you", "thanks", "thank", "thx", "ty",
                "thank you so much", "thanks a lot", "many thanks",
                "appreciate", "helpful", "very helpful",
                "good", "great", "awesome", "nice", "excellent",
                "perfect", "well done", "good bot", "good job",
                "that helps", "that helped", "got it", "understand",
            ],
            "responses": [
                "🎉 You're welcome! Happy coding!\n\nWhat next?\n🐍 Python  |  🔷 OOP  |  📦 Data Structures  |  🔍 Algorithms  |  💡 Tips",
                "😊 Glad I could help! Keep building things!\n\n→ Ask anything else about Python, OOP, DSA, or Algorithms!",
            ]
        },
        {
            "tag": "help",
            "description": "Help menu",
            "patterns": [
                "help", "menu", "options", "what can you do",
                "what do you know", "topics", "topic list",
                "commands", "guide", "instructions", "start",
            ],
            "responses": [
                "📚 **Programming Tutor — Available Topics:**\n\n🐍 **Python Basics**\n→ 'python', 'variables', 'loops', 'functions', 'list', 'dictionary', 'error handling'\n\n🔷 **OOP & Design Patterns**\n→ 'class', 'inheritance', 'polymorphism', 'singleton', 'factory', 'observer', 'solid'\n\n📦 **Data Structures**\n→ 'array', 'linked list', 'stack', 'queue', 'hash table', 'binary tree', 'graph'\n\n🔍 **Algorithms**\n→ 'sorting', 'binary search', 'bfs', 'dfs', 'recursion', 'dynamic programming', 'big o'\n\n💡 **Tips & Best Practices**\n→ 'clean code', 'debug', 'naming', 'practice'",
            ]
        },
        {
            "tag": "unknown",
            "description": "Fallback",
            "patterns": [],
            "responses": [
                "🤔 I didn't quite understand that.\n\nTry asking about:\n• 'Python basics'    • 'OOP / classes'\n• 'Data structures'  • 'Sorting algorithms'\n• 'Binary search'    • 'Dynamic programming'\n• 'Big O notation'   • 'Debug tips'\n\nOr type 'help' to see all available topics!",
                "❓ Not sure about that one.\n\nI specialise in:\n🐍 Python  |  🔷 OOP  |  📦 DSA  |  🔍 Algorithms\n\nType 'help' for the full topic list!",
            ]
        },
    ]

    for intent_data in INTENTS:
        intent_ref = db.collection(COL_INTENTS).document(intent_data["tag"])
        intent_ref.set({
            "tag":         intent_data["tag"],
            "description": intent_data["description"]
        })
        for pattern in intent_data["patterns"]:
            db.collection(COL_PATTERNS).add({
                "intent_tag": intent_data["tag"],
                "pattern":    pattern.lower()
            })
        for response in intent_data["responses"]:
            db.collection(COL_RESPONSES).add({
                "intent_tag": intent_data["tag"],
                "response":   response
            })

    print("[DB] Programming training data seeded successfully.")


def load_training_data():
    docs = db.collection(COL_PATTERNS).get()
    data = {}
    for doc in docs:
        d = doc.to_dict()
        tag = d["intent_tag"]
        data.setdefault(tag, []).append(d["pattern"])
    return data


def get_responses(intent_tag):
    docs = db.collection(COL_RESPONSES)\
             .where("intent_tag", "==", intent_tag).get()
    return [doc.to_dict()["response"] for doc in docs]


def save_chat_history(user_input, bot_response, intent_tag, confidence):
    db.collection(COL_HISTORY).add({
        "user_input":   user_input,
        "bot_response": bot_response,
        "intent_tag":   intent_tag,
        "confidence":   float(confidence),
        "timestamp":    firestore.SERVER_TIMESTAMP
    })


def view_chat_history(limit=10):
    docs = db.collection(COL_HISTORY)\
             .order_by("timestamp", direction=firestore.Query.DESCENDING)\
             .limit(limit).get()
    results = []
    for doc in docs:
        d = doc.to_dict()
        results.append((
            doc.id,
            d.get("user_input", ""),
            d.get("bot_response", ""),
            d.get("intent_tag", ""),
            d.get("confidence", 0),
            str(d.get("timestamp", ""))
        ))
    return results


def get_db_stats():
    return {
        "intents":      len(db.collection(COL_INTENTS).get()),
        "patterns":     len(db.collection(COL_PATTERNS).get()),
        "responses":    len(db.collection(COL_RESPONSES).get()),
        "chat_history": len(db.collection(COL_HISTORY).get()),
    }


# ============================================================
#  2. NLP LAYER
# ============================================================

STOPWORDS = {
    "a","an","the","is","are","was","were","be","been","to","of","in",
    "for","on","with","at","by","from","i","me","my","we","you","he",
    "she","it","they","do","does","did","have","has","had","will",
    "would","can","could","should","may","might","and","or","but",
    "not","no","so","if","this","that","these","those","about",
    "after","before","some","any","all","more","also","just","very"
}

def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.split()

def remove_stopwords(tokens):
    return [t for t in tokens if t not in STOPWORDS]

def stem(word):
    for suffix in ["ing", "tion", "ness", "ment", "er", "ed", "es"]:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[:-len(suffix)]
    return word

def preprocess(text):
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = [stem(t) for t in tokens]
    return tokens


# ============================================================
#  3. ML LAYER — TF-IDF + Cosine + Keyword Boost
# ============================================================

KEYWORD_MAP = {
    "python":          "python_basics",
    "variable":        "python_basics",
    "loop":            "python_basics",
    "function":        "python_basics",
    "list":            "python_basics",
    "dictionary":      "python_basics",
    "dict":            "python_basics",
    "string":          "python_basics",
    "exception":       "python_basics",
    "lambda":          "python_basics",
    "comprehension":   "python_basics",
    "decorator":       "python_basics",
    "oop":             "oop",
    "class":           "oop",
    "object":          "oop",
    "inheritance":     "oop",
    "polymorphism":    "oop",
    "encapsulation":   "oop",
    "abstraction":     "oop",
    "singleton":       "oop",
    "factory":         "oop",
    "observer":        "oop",
    "strategy":        "oop",
    "solid":           "oop",
    "pattern":         "oop",
    "stack":           "data_structures",
    "queue":           "data_structures",
    "linked":          "data_structures",
    "tree":            "data_structures",
    "graph":           "data_structures",
    "heap":            "data_structures",
    "hash":            "data_structures",
    "trie":            "data_structures",
    "array":           "data_structures",
    "algorithm":       "algorithms",
    "sort":            "algorithms",
    "search":          "algorithms",
    "recursion":       "algorithms",
    "bfs":             "algorithms",
    "dfs":             "algorithms",
    "dijkstra":        "algorithms",
    "dynamic":         "algorithms",
    "memoization":     "algorithms",
    "complexity":      "algorithms",
    "binary":          "algorithms",
    "debug":           "tips",
    "clean":           "tips",
    "best":            "tips",
    "refactor":        "tips",
    "git":             "tips",
    "leetcode":        "tips",
    "hello":           "greeting",
    "hi":              "greeting",
    "bye":             "goodbye",
    "thank":           "thanks",
    "help":            "help",
    "menu":            "help",
}


class TFIDFClassifier:

    def __init__(self):
        self.idf = {}
        self.class_vectors = {}
        self.classes = []

    def _tf(self, tokens):
        count = Counter(tokens)
        total = len(tokens) if tokens else 1
        return {w: f / total for w, f in count.items()}

    def _build_idf(self, all_docs):
        N = len(all_docs)
        df = Counter()
        for doc in all_docs:
            for w in set(doc):
                df[w] += 1
        return {w: math.log((N + 1) / (f + 1)) + 1 for w, f in df.items()}

    def _tfidf_vector(self, tokens):
        tf = self._tf(tokens)
        return {w: tf[w] * self.idf.get(w, 0) for w in tf}

    def _cosine(self, v1, v2):
        common = set(v1) & set(v2)
        dot = sum(v1[w] * v2[w] for w in common)
        n1  = math.sqrt(sum(x ** 2 for x in v1.values()))
        n2  = math.sqrt(sum(x ** 2 for x in v2.values()))
        return dot / (n1 * n2) if n1 and n2 else 0.0

    def train(self, training_data):
        self.classes = list(training_data.keys())
        processed = {}
        all_docs   = []
        for tag, patterns in training_data.items():
            p = [preprocess(x) for x in patterns]
            processed[tag] = p
            all_docs.extend(p)
        self.idf = self._build_idf(all_docs)
        for tag, patterns in processed.items():
            if not patterns:
                self.class_vectors[tag] = {}
                continue
            vecs = [self._tfidf_vector(p) for p in patterns]
            avg  = {}
            for v in vecs:
                for w, val in v.items():
                    avg[w] = avg.get(w, 0) + val
            n = len(vecs)
            self.class_vectors[tag] = {w: v / n for w, v in avg.items()}
        total_patterns = sum(len(p) for p in processed.values())
        print(f"[ML] Trained: {len(self.classes)} intents, {total_patterns} patterns.")

    def predict(self, text):
        tokens_raw = tokenize(text)
        for token in tokens_raw:
            stemmed = stem(token)
            if token in KEYWORD_MAP:
                return KEYWORD_MAP[token], 0.99
            if stemmed in KEYWORD_MAP:
                return KEYWORD_MAP[stemmed], 0.95
        tokens = remove_stopwords(tokens_raw)
        tokens = [stem(t) for t in tokens]
        if not tokens:
            return "unknown", 0.0
        query_vec = self._tfidf_vector(tokens)
        if not query_vec:
            return "unknown", 0.0
        scores = {
            tag: self._cosine(query_vec, vec)
            for tag, vec in self.class_vectors.items()
            if tag != "unknown"
        }
        if not scores:
            return "unknown", 0.0
        best_tag   = max(scores, key=scores.get)
        best_score = scores[best_tag]
        if best_score < 0.05:
            return "unknown", best_score
        return best_tag, round(best_score, 4)


# ============================================================
#  4. RESPONSE GENERATOR
# ============================================================

def generate_response(intent_tag):
    responses = get_responses(intent_tag)
    if not responses:
        responses = get_responses("unknown")
    return random.choice(responses) if responses else "Sorry, I have no response for that."


# ============================================================
#  5. CONSOLE INTERFACE  (original — unchanged)
# ============================================================

def print_banner():
    print("\n" + "=" * 62)
    print("   💻 PROGRAMMING AI TUTOR                              ")
    print("   🐍 Python  |  🔷 OOP  |  📦 DSA  |  🔍 Algorithms   ")
    print("=" * 62)
    print("   Type 'help' to see all topics")
    print("   Commands: history | stats | quit")
    print("=" * 62 + "\n")


def print_db_stats():
    stats = get_db_stats()
    print("\n📊 Firebase Firestore Stats:")
    print(f"   Intents  : {stats['intents']}")
    print(f"   Patterns : {stats['patterns']}")
    print(f"   Responses: {stats['responses']}")
    print(f"   History  : {stats['chat_history']} messages\n")


def print_history():
    rows = view_chat_history(limit=5)
    print("\n📜 Last 5 Conversations:")
    print("-" * 55)
    if not rows:
        print("  (No history yet)")
    for row in rows:
        _, user_in, bot_resp, tag, conf, ts = row
        print(f"  [{ts}]  Intent: {tag}  Conf: {conf:.0%}")
        print(f"  You: {user_in}")
        print(f"  Bot: {bot_resp[:70].strip()}…")
        print()
    print("-" * 55 + "\n")


def run_chatbot():
    print("[DB] Connecting to Firebase Firestore...")
    init_db()
    seed_data()

    training_data = load_training_data()
    classifier_console = TFIDFClassifier()
    classifier_console.train(training_data)

    print_banner()
    print_db_stats()
    print("Bot: 👋 Hello! I'm your Programming AI Tutor!")
    print("     Ask me about Python, OOP, Data Structures, or Algorithms.")
    print("     Type 'help' to see all topics.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: 👋 Goodbye! Keep coding! 🚀")
            break

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit", "q", "bye", "goodbye"]:
            print("Bot: 👋 Goodbye! Keep building things! 🚀")
            break
        if user_input.lower() == "history":
            print_history()
            continue
        if user_input.lower() == "stats":
            print_db_stats()
            continue

        intent_tag, confidence = classifier_console.predict(user_input)
        response = generate_response(intent_tag)

        print(f"\nBot: {response}")
        print(f"     [Intent: {intent_tag} | Confidence: {confidence:.1%}]\n")

        save_chat_history(user_input, response, intent_tag, confidence)


# ============================================================
#  6. FLASK API ROUTES  (NEW)
# ============================================================

# Global classifier (trained once at startup)
classifier = None

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    intent_tag, confidence = classifier.predict(user_input)
    response = generate_response(intent_tag)
    save_chat_history(user_input, response, intent_tag, confidence)

    return jsonify({
        "response":   response,
        "intent":     intent_tag,
        "confidence": round(float(confidence), 2)
    })

@app.route("/history", methods=["GET"])
def history():
    rows = view_chat_history(limit=10)
    result = []
    for row in rows:
        _, user_in, bot_resp, tag, conf, ts = row
        result.append({
            "user":       user_in,
            "bot":        bot_resp,
            "intent":     tag,
            "confidence": conf,
            "timestamp":  ts
        })
    return jsonify(result)

@app.route("/stats", methods=["GET"])
def stats():
    return jsonify(get_db_stats())


# ============================================================
#  7. STARTUP
# ============================================================

if __name__ == "__main__":
    print("[DB] Connecting to Firebase Firestore...")
    init_db()
    seed_data()

    training_data = load_training_data()
    classifier    = TFIDFClassifier()
    classifier.train(training_data)

    # Run mode: pass "--console" to use the original terminal chatbot
    # Default (no args) starts the Flask web server
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        run_chatbot()
    else:
        print("\n[Server] Starting Flask web server on http://localhost:5000")
        print("[Server] Visit http://localhost:5000 to open the chat UI")
        print("[Server] Or run:  python chatbot.py --console  for terminal mode\n")
       # app.run(port=5000, debug=False)
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))