# 🤖 BotNist – Transforming Web Data into Intelligent Support

**BotNist** is a powerful end-to-end web intelligence system that automates the scraping, structuring, and serving of website data to a cloud-hosted chatbot. It extracts structured information from any public website, uploads it to a centralized database, and provides an API key that enables integration with a **LLAMA2-7B-powered RAG chatbot** — turning any site into an intelligent, conversational experience.

---

## 🧠 Core Idea

Turn a website into a smart knowledge assistant:
- **Crawl** and extract useful business info from a website.
- **Store** it in a secure cloud database.
- **Serve** it through a chatbot using Retrieval-Augmented Generation (RAG).

---

## 🚀 Key Features

- 🌐 **Dynamic Web Scraping** via Selenium & BeautifulSoup
- 🔍 **Smart Categorization**: about us, services, contacts, legal, team, and more
- 🧾 **Multi-format Output**: `.json`, `.txt`, and MongoDB
- 🛡️ **User-Scoped SHA256 Key** generation
- 🧠 **RAG-Powered Chatbot Integration** (LLAMA2-7B with ChromaDB)
- 🔑 **API Key Provisioning** to connect chatbot to your website
- ⚡ **Plug-and-Play API Endpoint** for instant embedding

---

## 🛠️ Technologies Used

- **Python 3**
- **Selenium**, **BeautifulSoup4** — for crawling and parsing
- **Regex** — for email/phone extraction
- **MongoDB** — cloud storage
- **SHA256** — unique ID for each crawl session
- **LLAMA2-7B** — cloud-hosted chatbot
- **ChromaDB** — vector store for RAG pipeline
- **FastAPI / Flask API** — for serving answers via key-based access

---

## 📂 Folder Structure

```
BotNist/
├── output_data/
│   ├── all_data.json
│   └── all_data.txt
├── extracted_data.txt
├── process_link.py             # 🔁 Core crawler logic
├── case_study.pdf              # 📘 PDF documentation
└── README.md
```

---

## 🔄 Workflow

1. **Run the Scraper**  
   ```bash
   python process_link.py your_email@example.com https://example.com
   ```

2. **BotNist will:**
   - Crawl and extract categorized data from the site
   - Save it as `all_data.json` and `all_data.txt`
   - Upload structured data to MongoDB
   - Generate a **unique SHA256-based API key**

3. **Data is sent to a cloud-hosted LLM pipeline:**
   - LLAMA2-7B ingests the data using a RAG architecture
   - Embeddings are stored in ChromaDB
   - Queries are answered with **website-specific knowledge**

4. **User receives:**
   - ✅ A secure API key (based on email + site link hash)
   - ✅ API endpoint for chatbot interaction

---

## 🧪 Example API Usage

```bash
POST https://api.botnist.ai/query
Headers:
  Authorization: Bearer <your-api-key>
Body:
  {
    "question": "What services does this company offer?"
  }
```

💬 Response:
```json
{
  "answer": "The company offers cloud consulting, DevOps automation, and ML-based solutions tailored for SMEs."
}
```

---

## 🔗 Integration Flowchart

```
        ┌────────────┐         ┌───────────────┐
        │  User URL  ├───────► │  BotNist Crawler│
        └────────────┘         └───────────────┘
                                     │
                                     ▼
                           ┌──────────────────┐
                           │ Categorized Data │
                           └──────────────────┘
                                     │
                           ┌─────────┴─────────┐
                           ▼                   ▼
                  Store in MongoDB     Embed in ChromaDB (via RAG)
                                     │
                                     ▼
                          Hosted LLAMA2-7B Chatbot
                                     │
                                     ▼
                         Serve Answers via API (Keyed Access)
```

---

## 📑 Case Study

📎 **`case_study.pdf`** — Includes:
- Project overview & architecture
- Real crawl + chatbot output examples
- Error handling & key security
- Cloud pipeline architecture (LLAMA2 + ChromaDB)

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/BotNist.git
   cd BotNist
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure:
   - MongoDB URI in `connect_to_mongodb()`
   - Cloud chatbot endpoint (in the deployment setup)

4. Run the crawler:
   ```bash
   python process_link.py your_email@example.com https://targetsite.com
   ```

---

## 🧠 Use Case

> “Companies embed the BotNist chatbot on their website. Customers ask questions like ‘What are your refund policies?’ or ‘Do you offer SaaS services?’ — and the bot answers accurately using the site’s own scraped data.”

---

## 💬 API Integration in Website

Use the provided API key in your website like this:

```html
<script src="https://cdn.botnist.ai/chatbot.js"></script>
<script>
  BotNist.init({
    apiKey: "your-api-key",
    theme: "dark",
    position: "bottom-right"
  });
</script>
```

---

## ✨ Future Improvements

- Website change detection for re-crawling
- Chatbot tone customization (formal/casual)
- Admin dashboard for API key and crawl logs

---

## 📜 License

MIT License © 2025 BotNist Developers

---
> 🧠 *Your website — now with answers.*
