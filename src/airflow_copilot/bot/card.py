delete_card = {
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.4",
  "backgroundImage": {
    "url": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='1' height='1'><rect width='100%' height='100%' fill='%23F7F9FC'/></svg>"
  },
  "body": [
    {
      "type": "Container",
      "style": "accent",
      "bleed": True,
      "items": [
        {
          "type": "ColumnSet",
          "spacing": "Small",
          "columns": [
            {
              "type": "Column",
              "width": "auto",
              "items": [
                {
                  "type": "Image",
                  "url": "https://img.icons8.com/color/48/broom.png",
                  "size": "Medium",
                  "style": "Person",
                  "altText": "AI Assistant"
                }
              ]
            },
            {
              "type": "Column",
              "width": "stretch",
              "items": [
                {
                  "type": "TextBlock",
                  "text": "Clear chat history?",
                  "weight": "Bolder",
                  "size": "Large",
                  "wrap": True
                },
                {
                  "type": "TextBlock",
                  "text": "This will clear the AI Assistant’s conversation with you.\nDon’t worry—there’s no data loss. The assistant will begin storing messages again from your next interaction.",
                  "wrap": True,
                  "spacing": "Small",
                  "isSubtle": True
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "TextBlock",
      "text": "Help keep the system clean and green 🌿 — ready to refresh backend chat?",
      "weight": "Bolder",
      "spacing": "Medium",
      "wrap": True
    }
  ],
  "actions": [
    {
      "type": "Action.Submit",
      "title": "🧹Refresh & Save Space",
      "style": "positive",
      "data": {
        "type": "delete_history"
      }
    },
    {
      "type": "Action.Submit",
      "title": "😒 Later, maybe",
      "data": {
        "type": "cancel"
      }
    }
  ],
  "msteams": {
    "width": "Full"
  }
}

airflow_credential = {
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "type": "AdaptiveCard",
  "version": "1.4",
  "body": [
    {
      "type": "TextBlock",
      "text": "🔐 Enter Airflow Credentials",
      "weight": "Bolder",
      "size": "Large",
      "wrap": True
    },
    {
      "type": "TextBlock",
      "text": "Please enter your Airflow username and password to continue.",
      "wrap": True,
      "spacing": "Small",
      "isSubtle": True
    },
    {
      "type": "Input.Text",
      "id": "airflow_user",
      "placeholder": "Enter username",
      "label": "👤 Username"
    },
    {
      "type": "Input.Text",
      "id": "airflow_pass",
      "placeholder": "Enter password",
      "style": "Password",
      "label": "🔑 Password"
    }
  ],
  "actions": [
    {
      "type": "Action.Submit",
      "title": "🚀 Connect to Airflow",
      "data": {
        "type": "submit_airflow_credentials"
      },
      "style": "positive"
    }
  ],
  "msteams": {
    "width": "Full"
  }
}
