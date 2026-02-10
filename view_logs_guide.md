# How to View Logs and Traces for Vertex AI Agent Engine

Since your agent is deployed to **Vertex AI Agent Engine**, its logs and traces are automatically sent to **Google Cloud Logging** and **Google Cloud Trace**, respectively.

## Part 1: Viewing Logs

You can access logs in two ways: via the **Google Cloud Console** (GUI) or the **gcloud CLI**.

### Method 1: Google Cloud Console (Recommended)

1.  Navigate to the **[Logs Explorer](https://console.cloud.google.com/logs/query)** in the Google Cloud Console.
2.  In the **Query** field, paste the following filter to see logs specifically for your Agent Engine:

    ```text
    resource.type="aiplatform.googleapis.com/ReasoningEngine"
    ```

3.  Click **Run query**.
4.  You will see `stdout` (print statements) and `stderr` (errors) from your agent.

#### Refining the Query
To see logs for a specific agent or time range:

```text
resource.type="aiplatform.googleapis.com/ReasoningEngine"
severity>=DEFAULT
timestamp>"2023-10-27T00:00:00Z"
```

### Method 2: Command Line (gcloud)

You can stream logs directly to your terminal using the `gcloud` command.

#### Read Recent Logs
To fetch the last 20 log entries:

```bash
gcloud logging read 'resource.type="aiplatform.googleapis.com/ReasoningEngine"' \
  --limit=20 \
  --format="table(timestamp, severity, textPayload)"
```

#### Stream Live Logs
To watch logs in real-time (like `tail -f`):

```bash
gcloud beta logging tail 'resource.type="aiplatform.googleapis.com/ReasoningEngine"'
```

*(Note: `gcloud beta logging tail` requires the `roles/logging.viewer` IAM role and may require installing the `gcloud-logging-tail` component via `gcloud components install alpha` if it's not already available.)*

### Enabling Additional Logs

While standard output (`stdout`/`stderr`) is captured by default, you can enable more detailed logging for your agent's interactions.

To capture the actual content of prompts and responses (system, user, and model messages), you must set the following environment variable when deploying your agent:

```bash
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
```

You can set this in your `agent.py` or pass it as an environment variable during deployment.

## Part 2: Viewing Traces

Vertex AI Agent Engine integrates with **Google Cloud Trace** to help you visualize the execution flow of your agent (e.g., tool calls, LLM steps).

### How to Access Traces

1.  Navigate to the **Vertex AI Agent Builder** section in the Google Cloud Console.
2.  Go to **Agent Engine** (or **Reasoning Engine**).
3.  Click on your specific **Agent Engine ID**.
4.  Select the **Traces** tab.

Here you can see a "Span view" of your agent's execution, which details:
*   Reasoning steps
*   Tool execution times
*   Input/Output for each step

### Differentiating Tools and Memory

In the **Traces** view, you can distinguish between standard tool calls and memory operations by looking at the **Span Name** or **Tool Name** attribute:

*   **Tool Calls**: Will display the name of the function you defined (e.g., `morning_greet`, `google_search`).
*   **Memory Access**: Will typically appear as specific memory-related tool names such as:
    *   `PreloadMemoryTool`: Automatic retrieval of memories at the start of a turn.
    *   `LoadMemory`: Explicit action by the agent to recall information.
    *   `SaveMemory`: Action to store new information.

You can click on any span to see the specific input arguments (what the agent sent to the tool) and the output (what the tool returned).

### Enabling Traces

To ensure traces are captured, make sure you deploy your agent with tracing enabled.

If using the ADK CLI:
```bash
adk deploy agent_engine --trace_to_cloud
```

If using code (`agent.py`):
Ensure you set `enable_tracing=True` when initializing your agent or set the following environment variables if deploying custom containers:
*   `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=True`

---

## Part 3: Differentiating in Cloud Logs (Text)

While **Traces** are the best way to see the distinction, you might look at text logs in Logs Explorer.

*   **Tool Calls**: Vertex AI Agent Engine does **not** automatically generate distinct text log entries for every tool call by default. You rely on Traces for this. However, if you enabled `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`, you may see the *results* of tool calls embedded in the inputs/outputs of the model interaction logs.
*   **Memory**: There are **no automatic text logs** for Memory Bank operations (like "loading memory").
    *   To see memory operations in text logs, you must add your own `logging.info(...)` calls inside your agent's code or tool definitions.

**Summary**: Use **Traces** (Part 2) to visualize Tool vs. Memory distinct steps. Use **Logs** (Part 1) to inspect the raw text input/output of the LLM.

---

## Troubleshooting
*   **No logs/traces?** Ensure your agent has actually received traffic.
*   **Permissions**: Make sure your user account has `roles/logging.viewer` and `roles/cloudtrace.user`.
*   **Delays**: There might be a slight delay (a few seconds) between an event and it appearing in Cloud Console.
