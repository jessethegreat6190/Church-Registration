exports.handler = async (event) => {
  const GOOGLE_SCRIPT_URL = process.env.GOOGLE_SCRIPT_URL;

  if (!GOOGLE_SCRIPT_URL) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "GOOGLE_SCRIPT_URL environment variable is not set in Netlify." })
    };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const response = await fetch(GOOGLE_SCRIPT_URL, {
      method: 'POST',
      body: event.body,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      redirect: 'follow'
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Google Script Error:", errorText);
      return {
        statusCode: response.status,
        body: JSON.stringify({ error: `Google Script error: ${errorText}` })
      };
    }

    const resText = await response.text();
    return {
      statusCode: 200,
      body: JSON.stringify({ message: "Success", details: resText })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
