<!-- Text content inside the page. -->
/*
<!-- Text content inside the page. -->
Sample Node.js Express server for Safaricom Daraja STK Push.

<!-- Text content inside the page. -->
1. Install dependencies:
   <!-- Text content inside the page. -->
   npm install express axios dotenv

<!-- Text content inside the page. -->
2. Create a .env file in the same folder with:
   <!-- Text content inside the page. -->
   CONSUMER_KEY=your_consumer_key
   <!-- Text content inside the page. -->
   CONSUMER_SECRET=your_consumer_secret
   <!-- Text content inside the page. -->
   SHORTCODE=174379            # or your live shortcode
   <!-- Text content inside the page. -->
   PASSKEY=your_passkey
   <!-- Text content inside the page. -->
   CALLBACK_URL=https://yourdomain.com/mpesa-callback
   <!-- Text content inside the page. -->
   DARJA_ENDPOINT=https://sandbox.safaricom.co.ke

<!-- Text content inside the page. -->
3. Run:
   <!-- Text content inside the page. -->
   node mpesa-stk-server.js

<!-- Text content inside the page. -->
4. From your checkout page, POST phone and amount to /stk-push
<!-- Text content inside the page. -->
*/

<!-- Text content inside the page. -->
// Load configuration variables from a .env file into process.env
<!-- Text content inside the page. -->
require('dotenv').config();
<!-- Text content inside the page. -->
const express = require('express');
<!-- Text content inside the page. -->
const axios = require('axios');
<!-- Text content inside the page. -->
const app = express();
<!-- Text content inside the page. -->
const port = process.env.PORT || 3000;

<!-- Text content inside the page. -->
const {
  <!-- Text content inside the page. -->
  CONSUMER_KEY,
  <!-- Text content inside the page. -->
  CONSUMER_SECRET,
  <!-- Text content inside the page. -->
  SHORTCODE,
  <!-- Text content inside the page. -->
  PASSKEY,
  <!-- Text content inside the page. -->
  CALLBACK_URL,
  <!-- Text content inside the page. -->
  DARJA_ENDPOINT = 'https://sandbox.safaricom.co.ke'
<!-- Text content inside the page. -->
} = process.env;

<!-- Text content inside the page. -->
if (!CONSUMER_KEY || !CONSUMER_SECRET || !SHORTCODE || !PASSKEY || !CALLBACK_URL) {
  <!-- Text content inside the page. -->
  console.error('Missing required environment variables. Please set CONSUMER_KEY, CONSUMER_SECRET, SHORTCODE, PASSKEY, CALLBACK_URL.');
  <!-- Text content inside the page. -->
  process.exit(1);
<!-- Text content inside the page. -->
}

<!-- Text content inside the page. -->
app.use(express.json());

<!-- Text content inside the page. -->
// Get an access token from the M-Pesa API using app credentials.
<!-- Text content inside the page. -->
// This token is needed for every request to the Daraja API.
<!-- Text content inside the page. -->
async function getAccessToken() {
  <!-- Text content inside the page. -->
  const url = `${DARJA_ENDPOINT}/oauth/v1/generate?grant_type=client_credentials`;
  <!-- Text content inside the page. -->
  const auth = Buffer.from(`${CONSUMER_KEY}:${CONSUMER_SECRET}`).toString('base64');

  <!-- Text content inside the page. -->
  const response = await axios.get(url, {
    <!-- Text content inside the page. -->
    headers: {
      <!-- Text content inside the page. -->
      Authorization: `Basic ${auth}`
    <!-- Text content inside the page. -->
    }
  <!-- Text content inside the page. -->
  });

  <!-- Text content inside the page. -->
  return response.data.access_token;
<!-- Text content inside the page. -->
}

<!-- Text content inside the page. -->
// Build the timestamp in the format required by M-Pesa Daraja.
<!-- Text content inside the page. -->
function getTimestamp() {
  <!-- Text content inside the page. -->
  const date = new Date();
  <!-- Text content inside the page. -->
  const year = date.getFullYear();
  <!-- Text content inside the page. -->
  const month = String(date.getMonth() + 1).padStart(2, '0');
  <!-- Text content inside the page. -->
  const day = String(date.getDate()).padStart(2, '0');
  <!-- Text content inside the page. -->
  const hours = String(date.getHours()).padStart(2, '0');
  <!-- Text content inside the page. -->
  const minutes = String(date.getMinutes()).padStart(2, '0');
  <!-- Text content inside the page. -->
  const seconds = String(date.getSeconds()).padStart(2, '0');
  <!-- Text content inside the page. -->
  return `${year}${month}${day}${hours}${minutes}${seconds}`;
<!-- Text content inside the page. -->
}

<!-- Text content inside the page. -->
// Generate the encoded password required by the M-Pesa STK Push protocol.
<!-- Text content inside the page. -->
function generatePassword() {
  <!-- Text content inside the page. -->
  const timestamp = getTimestamp();
  <!-- Text content inside the page. -->
  const data = `${SHORTCODE}${PASSKEY}${timestamp}`;
  <!-- Text content inside the page. -->
  return Buffer.from(data).toString('base64');
<!-- Text content inside the page. -->
}

<!-- Text content inside the page. -->
app.get('/', (req, res) => {
  <!-- Text content inside the page. -->
  res.send('M-Pesa STK Push sample server is running. POST /stk-push');
<!-- Text content inside the page. -->
});

<!-- Text content inside the page. -->
app.post('/stk-push', async (req, res) => {
  <!-- Text content inside the page. -->
  // This endpoint receives a phone number and amount from the checkout page.
  <!-- Text content inside the page. -->
  // It then sends a request to the M-Pesa API to trigger the STK Push on the customer's phone.
  <!-- Text content inside the page. -->
  const { phone, amount, accountReference, transactionDesc } = req.body;

  <!-- Text content inside the page. -->
  if (!phone || !amount) {
    <!-- Text content inside the page. -->
    return res.status(400).json({ error: 'phone and amount are required' });
  <!-- Text content inside the page. -->
  }

  <!-- Text content inside the page. -->
  try {
    <!-- Text content inside the page. -->
    const accessToken = await getAccessToken();
    <!-- Text content inside the page. -->
    const url = `${DARJA_ENDPOINT}/mpesa/stkpush/v1/processrequest`;
    <!-- Text content inside the page. -->
    const payload = {
      <!-- Text content inside the page. -->
      BusinessShortCode: SHORTCODE,
      <!-- Text content inside the page. -->
      Password: generatePassword(),
      <!-- Text content inside the page. -->
      Timestamp: getTimestamp(),
      <!-- Text content inside the page. -->
      TransactionType: 'CustomerPayBillOnline',
      <!-- Text content inside the page. -->
      Amount: amount,
      <!-- Text content inside the page. -->
      PartyA: phone,
      <!-- Text content inside the page. -->
      PartyB: SHORTCODE,
      <!-- Text content inside the page. -->
      PhoneNumber: phone,
      <!-- Text content inside the page. -->
      CallBackURL: CALLBACK_URL,
      <!-- Text content inside the page. -->
      AccountReference: accountReference || 'BoutiqueOrder',
      <!-- Text content inside the page. -->
      TransactionDesc: transactionDesc || 'Boutique payment'
    <!-- Text content inside the page. -->
    };

    <!-- Text content inside the page. -->
    // Send the STK Push request to the M-Pesa Daraja API.
    <!-- Text content inside the page. -->
    const response = await axios.post(url, payload, {
      <!-- Text content inside the page. -->
      headers: {
        <!-- Text content inside the page. -->
        Authorization: `Bearer ${accessToken}`,
        <!-- Text content inside the page. -->
        'Content-Type': 'application/json'
      <!-- Text content inside the page. -->
      }
    <!-- Text content inside the page. -->
    });

    <!-- Text content inside the page. -->
    return res.json(response.data);
  <!-- Text content inside the page. -->
  } catch (error) {
    <!-- Text content inside the page. -->
    console.error(error.response ? error.response.data : error.message);
    <!-- Text content inside the page. -->
    return res.status(500).json({ error: 'STK push request failed', details: error.response ? error.response.data : error.message });
  <!-- Text content inside the page. -->
  }
<!-- Text content inside the page. -->
});

<!-- Text content inside the page. -->
app.listen(port, () => {
  <!-- Text content inside the page. -->
  console.log(`M-Pesa STK Push server listening at http://localhost:${port}`);
<!-- Text content inside the page. -->
});
