# Admin Guide: Configuring Model Armor with Sensitive Data Protection (SDP) on GCP

This guide details how to secure your AI agents by integrating **Model Armor** with **Sensitive Data Protection (SDP)** on Google Cloud Platform.

## Overview
Model Armor acts as a security layer for your LLMs, filtering incoming prompts and outgoing responses. It leverages SDP to detect and redact sensitive information (PII, financial data, etc.) before it reaches the model or the user.

## Prerequisites
1.  **Google Cloud Project**: You must have a GCP project with billing enabled.
2.  **Permissions**: Ensure your user account has the following IAM roles:
    *   `roles/modelarmor.admin`
    *   `roles/dlp.admin` (for configuring SDP)
    *   `roles/serviceusage.serviceUsageAdmin` (to enable APIs)

## Step 1: Enable Required APIs

1.  Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Enable the following APIs:
    *   **Model Armor API**
    *   **Sensitive Data Protection (DLP) API**

## Step 2: Configure Sensitive Data Protection (SDP)

Model Armor uses SDP "Templates" to define what to look for and how to handle it.

### 2.1 Create an Inspection Template (Detection)
This defines *what* data specifically counts as "sensitive" (e.g., Credit Card numbers, Email addresses).

1.  Go to **Sensitive Data Protection** > **Configuration** > **Templates** in the GCP Console.
2.  Click **+ CREATE TEMPLATE**.
3.  Choose **Inspect** template type.
4.  **InfoTypes**: Select the built-in infoTypes you want to detect (e.g., `CREDIT_CARD_NUMBER`, `EMAIL_ADDRESS`, `US_SOCIAL_SECURITY_NUMBER`).
5.  (Optional) Add custom infoTypes if you have specific internal data formats (like Account IDs).
6.  Save the template. Note the **Template Resource Name** (e.g., `projects/YOUR_PROJECT/locations/us-central1/inspectTemplates/TEMPLATE_ID`).

### 2.2 Create a De-identification Template (Redaction)
This defines *what to do* when sensitive data is found (e.g., replace with `[REDACTED]`).

1.  In the **Templates** section, click **+ CREATE TEMPLATE** again.
2.  Choose **De-identify** template type.
3.  **Transformation**: Choose "Replace with infoType name" (e.g., `my name is John` -> `my name is [PERSON_NAME]`) or "Mask with character" (e.g., `XXX-XX-XXXX`).
4.  Save the template. Note the **Template Resource Name**.

## Step 3: Configure Model Armor

Now you create a Model Armor policy that uses your SDP templates.

1.  Go to **Model Armor** in the GCP Console.
2.  Click **CREATE TEMPLATE**.
3.  **Details**:
    *   **Name**: `agent-security-policy` (or similar).
    *   **Region**: Select the region where your agent is deployed (e.g., `us-central1`).
4.  **Detections**:
    *   Enable **Sensitive Data Protection**.
    *   Select **Advanced** configuration.
    *   **Inspection Template**: Paste the resource path of the template you created in Step 2.1.
    *   **De-identification Template**: Paste the resource path of the template you created in Step 2.2.
5.  **Other Filters** (Optional):
    *   Enable "Prompt Injection & Jailbreak" detection.
    *   Enable "Malicious URL" detection.
6.  **Responsible AI**: Set confidence thresholds for Hate Speech, Harassment, etc.
7.  Click **CREATE**.

## Step 4: Integration with Your Agent

Once configured, Model Armor exposes two key API methods: `sanitizeUserPrompt` and `sanitizeModelResponse`.

When integrating with `google.adk.agents` or Vertex AI:

*   **Vertex AI Proxy**: If using Vertex AI's managed endpoints, you can often attach Model Armor policies directly to the endpoint configuration.
*   **Manual Integration**: In your application code (`agent.py` or middleware), you would wrap your LLM calls:

    ```python
    # Pseudo-code for flow
    prompt = user_input
    
    # 1. Sanitize Prompt
    safe_prompt = model_armor_client.sanitize_user_prompt(
        name="projects/YOUR_PROJECT/locations/REGION/templates/YOUR_TEMPLATE_ID",
        user_prompt=prompt
    )
    
    # 2. Call LLM
    llm_response = call_gemini(safe_prompt.sanitized_content)
    
    # 3. Sanitize Response
    safe_response = model_armor_client.sanitize_model_response(
        name="projects/YOUR_PROJECT/locations/REGION/templates/YOUR_TEMPLATE_ID",
        model_response=llm_response
    )
    
    return safe_response.sanitized_content
    ```

## Step 5: Verify

1.  Go to the Model Armor dashboard.
2.  Use the "Try it out" feature (if available) or send a test request with a dummy credit card number via your agent.
3.  Verify that the credit card number is redacted or the request is blocked, depending on your policy.
