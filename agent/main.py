import os
import json
from flask import Flask, request, jsonify
from pyhelm3 import Client
import outlines
import outlines.models.openai as llm
from pydantic import BaseModel

# Configuration
LLM_API_URL = os.getenv("LLM_API_URL", "http://ollama:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5-coder:7b")
DEPLOYMENTS_DIR = "/deployments"
METADATA_FILE = os.path.join(DEPLOYMENTS_DIR, "meta.json")

# Define schema for LLM output
class Asset(BaseModel):
    name: str
    code: str

# Initialize OpenAI model
model = llm.OpenAI(
    base_url=LLM_API_URL,
    model=LLM_MODEL,
)

def generate_asset(prompt: str) -> Asset:
    """Generate asset using structured output from LLM"""
    guide = outlines.generate.json(Asset)
    program = outlines.Program(model)
    
    system_prompt = """You are a code generation assistant. Generate Python code based on the user's prompt.
    Return a JSON object with a descriptive name for the asset and the generated code."""
    
    result = program.text(f"{system_prompt}\n\nUser prompt: {prompt}")
    return guide(result)

app = Flask(__name__)

DEPLOYMENTS_DIR = "/deployments"
METADATA_FILE = os.path.join(DEPLOYMENTS_DIR, "meta.json")

# Ensure deployments directory exists
os.makedirs(DEPLOYMENTS_DIR, exist_ok=True)

def get_existing_deployments():
    """Read all deployments from the filesystem"""
    deployments = []
    # Read metadata index if exists
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {}

    for filename in os.listdir(DEPLOYMENTS_DIR):
        if filename.endswith('.py'):
            name = filename[:-3]  # Remove .py extension
            with open(os.path.join(DEPLOYMENTS_DIR, filename), 'r') as f:
                code = f.read()
                deployments.append({
                    "name": name,
                    "code": code,
                    "prompt": metadata.get(name, {}).get('prompt', '')
                })
    return deployments

def store_deployment(asset, prompt):
    """Store deployment as Python file and update metadata"""
    # Save Python file
    filename = f"{asset.name}.py"
    filepath = os.path.join(DEPLOYMENTS_DIR, filename)
    with open(filepath, 'w') as f:
        f.write(asset.code)
    
    # Update metadata
    metadata = {}
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            metadata = json.load(f)
    
    metadata[asset.name] = {
        "prompt": prompt
    }
    
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f)

def update_helm_chart():
    """Update Helm chart with all deployments from filesystem"""
    helm_client = Client()
    try:
        deployments = [{
            "name": d["name"],
            "image": "dagster/dagster-k8s:latest",
            "dagsterApiGrpcArgs": ["-m", "dagster_pipeline"], 
            "port": 4000
        } for d in get_existing_deployments()]

        helm_client.upgrade_release(
            release_name="dagster",
            chart="dagster/dagster",
            values={
                "dagster-user-deployments": {
                    "deployments": deployments
                }
            }
        )
        print("Helm chart updated successfully")
    except Exception as e:
        print(f"Failed to update Helm chart: {e}")
        raise

@app.route('/asset', methods=['POST'])
def create_asset():
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        # Generate structured output from LLM
        asset = generate_asset(prompt)

        # Store deployment
        store_deployment(asset, prompt)
        update_helm_chart()

        return jsonify({
            "success": True,
            "message": "Asset created and deployment updated.",
            "asset": asset
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
