import os
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from providers import get_recipe_provider, get_preprocess_provider, get_score_provider
from meals import meals_list, get_recipe_prompt

app = FastAPI()

class GenerateRequest(BaseModel):
    provider: str
    model: str
    dataset: str

    @validator('provider')
    def validate_provider(cls, v):
        allowed = {'gpt5', 'grok', 'gemini', 'deepseek', 'perplexity', 'dummy', 'openai'}
        if v.lower() not in allowed:
            raise ValueError(f'Provider must be one of {allowed}')
        return v.lower()

def save_generated_data(
    data: str,
    provider: str,
    model: str,
    dataset: str,
    status: str = "raw",
    output_dir: str = "data/generated"
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    dataset_slug = dataset.lower().replace(" ", "-")
    filename = f"{dataset_slug}_{provider}_{model}_{status}_.csv"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data)
    return filepath

@app.post("/generate")
async def generate_recipes(request: GenerateRequest):
    provider = get_recipe_provider(request.provider)
    if not provider:
        raise HTTPException(status_code=400, detail="Unknown recipe provider")
    
    results: Dict[str, Any] = {}
    for meal in meals_list:
        try:
            prompt = get_recipe_prompt(meal)
            generated = provider.generate(request.model, prompt)
            filepath = save_generated_data(
                generated,
                provider=request.provider,
                model=request.model,
                dataset=request.dataset,
                status="raw"
            )
            results[meal] = {
                "status": "success",
                "filepath": filepath,
                "recipes_count": len(generated.split('\n')) - 1  # Exclude header
            }
        except Exception as e:
            results[meal] = {
                "status": "error",
                "error": str(e)
            }
    return results

class PreprocessRequest(BaseModel):
    input_path: str
    output_path: Optional[str] = None

@app.post("/preprocess")
async def preprocess_endpoint(request: PreprocessRequest):
    provider = get_preprocess_provider()
    cleaned_path = provider.preprocess(request.input_path, request.output_path)
    return {"cleaned_file": cleaned_path}

class ScoreRequest(BaseModel):
    input_path: str
    output_path: Optional[str] = None

@app.post("/score")
async def score_endpoint(request: ScoreRequest):
    provider = get_score_provider()
    return provider.score(request.input_path, request.output_path)