# Admin Guide: Setting up Google Workspace Connectors

Gemini Enterprise allows you to ground your agents with data from Google Workspace (Drive, Gmail, Docs, Slides, Sheets, Sites, Keynote, etc.) using **Google Workspace Connectors**.

This guide details how to configure these connectors to make your organization's data searchable and usable by your agents.

## Prerequisites

Before configuring any connector, ensure the following:

1.  **Gemini Enterprise Edition**: You must have a Gemini Enterprise license.
2.  **Google Workspace Administrator Access**: You need admin privileges to configure data access and visibility.
3.  **Google Cloud Project**: A Google Cloud project with **Vertex AI Search and Conversation** enabled.
4.  **Identity Provider (IdP)**: You **must** configure an Identity Provider (like Google Cloud Identity) to map Google Workspace identities to Google Cloud identities. This ensures users only see data they are allowed to access.
    *   *See [Configure Identity Provider](https://cloud.google.com/generative-ai-app-builder/docs/configure-identity-provider) for details.*
5.  **Smart Features**: Ensure "Smart features and personalization" is enabled in Gmail/Google Workspace.

## Supported Data Sources

*   **Google Drive** (Docs, Sheets, Slides, PDFs, etc.)
*   **Gmail**
*   **Google Sites** (Requires allowlist)
*   **Google Groups** (Requires allowlist)
*   **People / Directory**

## Step 1: Enable the Connector

1.  Native to **Google Cloud Console** > **Agent Builder** > **Data Stores**.
2.  Click **Create Data Store**.
3.  Select the **Google Workspace** source you want to connect (e.g., **Google Drive**).

### Configuration for Google Drive

1.  **Source**: Select **Google Drive**.
2.  **Optimization**: Choose "Chat" (for agents) or "Search".
3.  **Data Selection**:
    *   **Entire Domain**: Indexes all non-private shared locations.
    *   **Specific Units**: Select specific Shared Drives or Folders.
4.  **Create**: Click create. The initial indexing can take up to 24-48 hours depending on data volume.

### Configuration for Gmail

1.  **Source**: Select **Gmail**.
2.  **Authorization**: You may need to provide a Service Account with Domain-Wide Delegation to access user emails (for discovery/audit) or configure OAuth for individual user access.
3.  **Create**: Click create.

## Step 2: Link Data Store to Agent

Once the Data Store is created and indexing:

1.  Go to your **Agent** (or Search App) in the Console.
2.  Go to **Data Stores**.
3.  Click **Add Data Store**.
4.  Select your newly created Google Workspace Data Store.
5.  Click **Add**.

## Step 3: Verification

To verify the connection:

1.  Go to the **Preview** pane of your Agent.
2.  Ask a question relevant to a document in your connected Drive.
    *   *Example: "Summarize the 'Project Alpha' design doc."*
3.  The agent should return an answer cited from the Google Doc.

## Troubleshooting

*   **"I don't see results"**: Indexing takes time. Wait at least 4 hours for small datasets, 24+ for large ones.
*   **"Access Denied"**: Check your Identity Provider configuration. If your testing email doesn't match the Google Workspace identity, you won't see results.
*   **"Connector not found"**: Some sources (Sites, Groups) may be in Preview and require allowlisting. Contact your Google account representative.
