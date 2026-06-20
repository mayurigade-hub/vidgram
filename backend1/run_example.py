import json
from api import score_influencer_payload

# Load the low-risk influencer sample data
with open('sample_data/influencer_low_risk.json', 'r') as f:
    payload = json.load(f)

# Run the fraud detection engine
result = score_influencer_payload(payload)

# Print the final scoring result beautifully
print(json.dumps(result, indent=2))
