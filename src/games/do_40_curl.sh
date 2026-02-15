
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3-vl:2b",
  "messages": [
    {
      "role": "user",
      "content": "Why is the sky blue?"
    }
  ],
  "stream": false
}'
