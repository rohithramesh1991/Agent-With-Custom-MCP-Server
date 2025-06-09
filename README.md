# Agent-With-Custom-MCP-Server
This project demonstrates building a custom MCP (Model Context Protocol) server from scratch and integrating it seamlessly with a Gradio-based chat application. It extends the previous work of connecting existing MCP servers by providing full control over server behavior and enabling deeper customization for AI agent workflows.

This project demonstrates a powerful multi-tool chat assistant built using the Model Context Protocol (MCP). It integrates:

Custom MCP servers for real-time API tools like weather information and IP reputation checks.

- A prebuilt SQLite MCP server to perform live database queries.

- A user-friendly Gradio chat interface for seamless conversational interaction.

- By combining these components, the assistant can handle diverse queries—from database management and API calls to fetching real-time data—all within a single chat session.

### Important: API Keys and Environment Variables
To run this project, you must add your API keys to a `.env` file in the root directory:

- `GROQ_API_KEY` — for the Groq language model access from [Groq](https://groq.com/)

- `ABUSEIPDB_API_KEY` — for checking IP reputation from [abuseipdb](https://www.abuseipdb.com/)

- `WEATHERMAP_API_KEY` — for weather data from [OpenWeatherMap](https://home.openweathermap.org/users/sign_in)

👉 You can read more about this on my [Medium](https://medium.com/@rohithramesh1991/how-to-build-and-integrate-mcp-servers-for-a-versatile-chat-agent-cb0ea07b2b89) page.
