# Admin Guide: Deploying and Registering Your Agent

This guide covers how to deploy your ADK agent to **Vertex AI Agent Engine** and make it available in **Gemini Enterprise**.

## 1. Deploy to Agent Engine

The primary way to "register" your agent for use is to deploy it to the managed **Agent Engine** service. This creates a callable endpoint and an identity for your agent.

### Command
Run the following command from your project root:

```bash
adk deploy agent_engine \
  --project YOUR_PROJECT_ID \
  --region us-central1 \
  --display_name "My First Agent"
```

### Important Flags
*   `--trace_to_cloud`: Enables Cloud Trace (highly recommended for debugging).
*   `--otel_to_cloud`: Enables OpenTelemetry logging.
*   `--env_file .env`: Loads your environment variables.

### Example with Logging Enabled

```bash
adk deploy agent_engine \
  --project my-gcp-project \
  --region us-central1 \
  --display_name "Production Agent" \
  --trace_to_cloud \
  --otel_to_cloud
```

## 2. Registering with Gemini Enterprise

Once deployed to Agent Engine, you can integrate your agent with Gemini Enterprise to make it discoverable in Google Workspace.

### Method A: Google Cloud Console (Recommended)
1.  Go to the **Vertex AI Agent Builder** console.
2.  Navigate to **Agent Engine** (or **Reasoning Engine**).
3.  Find your deployed agent in the list.
4.  Copy the **Resource ID** (e.g., `projects/123/locations/us-central1/reasoningEngines/456`).
5.  Navigate to **Gemini Enterprise** (or **Google Workspace Admin** > **Gemini**).
6.  Select **Add Agent** or **Connect Resource**.
7.  Paste the Agent Engine Resource ID.

### Method B: ADK CLI (If Supported)
If your version of ADK supports direct registration (check `adk --help` for `api_server` or similar), you might be able to create an app entry directly, but the Console method is the standard path for Enterprise integration.

## 3. Deployment Checklist

Before deploying, ensure:
*   [ ] You have run `adk web` locally to verify functionality.
*   [ ] You have set **Model Armor** policies (see `model_armor_setup.md`).
*   [ ] You have configured logging env vars (see `view_logs_guide.md`).
*   [ ] Your `requirements.txt` is up to date.
