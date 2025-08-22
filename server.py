import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from providers import get_recipe_provider, get_preprocess_provider, get_score_provider
from meals import meals_list, prompt_template

app = FastAPI()

class GenerateRequest(BaseModel):
    provider: str
    model: str
    dataset: str

def save_generated_data(
    data: str,
    provider: str,
    model: str,
    dataset: str,
    status: str = "raw",
    output_dir: str = "data/generated"
):
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
    results = {}
    for meal in meals_list:
        prompt = prompt_template.format(meal=meal)
        try:
            generated = provider.generate(request.model, prompt)
            results[meal] = generated
            save_generated_data(
                generated,
                provider=request.provider,
                model=request.model,
                dataset=request.dataset,
                status="raw"
            )
        except Exception as e:
            results[meal] = f"Error: {e}"
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