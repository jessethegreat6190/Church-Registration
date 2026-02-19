exports.handler = async (event) => {
  const GOOGLE_SCRIPT_URL = process.env.GOOGLE_SCRIPT_URL;

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    await fetch(GOOGLE_SCRIPT_URL, {
      method: 'POST',
      body: event.body,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ message: "Success" })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
