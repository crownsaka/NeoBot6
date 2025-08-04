export default async function handler(req, res) {
  const prompt = req.body.prompt;

  try {
    const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${process.env.OPENROUTER_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "mistralai/mistral-small-3.2-24b-instruct:free",
        messages: [
          { role: "user", content: prompt }
        ]
      })
    });

    const data = await response.json();
    res.status(200).json({ reply: data.choices?.[0]?.message?.content || "No response" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Something went wrong." });
  }
}
