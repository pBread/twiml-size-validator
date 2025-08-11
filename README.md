# TwiML Payload Size Validator

Twilio enforces a 64 KB limit on the entire TwiML XML your webhook returns. After Twilio receives that XML, it is compressed internally, and some TwiML elements apply additional (undocumented) limits based on the post‑compression size. Because real‑world compression varies with the data, two payloads of the same raw size can behave differently.

This repo gives you a controlled way to explore those boundaries: generate payloads with different compressibility profiles, embed them as `<Parameter>` values, and observe how close you can get to the limits under realistic conditions.

The example implementation uses the `<Parameter>` element nested under `<ConversationRelay>`, but the approach works for any TwiML elements with arbitrarily defined values.

## Getting Started

### Configure Twilio Number

Open the Twilio Console → Phone Numbers → Manage → Active numbers → click the number you want to use.

For A CALL COMES IN, set:

- URL: https://your-ngrok-domain.ngrok-free.app/incoming-call
- Method: HTTP POST

For STATUS CALLBACK URL, set:

- URL: https://your-ngrok-domain.ngrok-free.app/call-status
- Method: HTTP POST

### Local Setup

#### Run Ngrok

```bash
ngrok http 3333

# or

ngrok http 3333 --url your-ngrok-domain.ngrok-free.app
```

#### Set Ngrok Domain as HOSTNAME

Create an `.env`

```bash
cp .env.example .env
```

and set your `HOSTNAME` as the Ngrok domain.

```bash
HOSTNAME="your-ngrok-domain.ngrok-free.app"  # must match your public tunnel host
```

#### Install & Run Server

Open a second terminal and start the server.

```bash
uv sync
uv run python src/main.py
```

## Using the App

### How to Run a Test

Place a call to the Twilio phone number you have configured.

- If the call connects successfully, then your payload is fine.
- If the call fails, then your payload is greater than 64kb.
- If the call results in a `no-answer`, your payload is smaller than the 64kb limit but is tripping some internal limitation.

### Generator

The repo includes a generator that produces strings with different compressibility profiles so you can explore best-case, worst-case, and realistic behavior without hand-crafting data.

Simply update the following two configuration parameters for initial testing.

- **TWIML_SIZE**: The total TwiML size in bytes.
- **COMPRESSIBILITY**: Determines the type of data generated, which have different compressibility profiles.
  - `random` – Uniformly random characters → low compression. Treat this as worst-case.
  - `maximally` – Highly repetitive content → very high compression. Best-case sanity check.
  - `lipsum` – Realistic, human-ish text (names, places, sentences) → moderate compression.

```python
TWIML_SIZE = 34 * 1024  # kbs
COMPRESSIBILITY = "lipsum"  # . Options: random | maximally | lipsum
```

### Testing Your Own Payload

Update the file [src/custom.txt](src/custom.txt) with your own payload. Then, uncomment the code in the `/incoming-call` webhook.

```python
    # uncomment to use the custom.txt file as the payload
    with open("src/custom.txt", "r", encoding="utf-8") as f:
        target = f.read().strip()
        target = escape_xml(target)
        logger.info("Loaded content from custom.txt")
```
