import os
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, validator
from providers.generation import get_recipe_provider
from providers.preprocessing import get_preprocess_provider
from providers.scoring import get_score_provider
from providers.validation import get_validation_provider
from providers.image import get_image_provider
from providers.logging import get_logging_provider
from meals import meals_list, get_recipe_prompt

app = FastAPI(title="Recipe Generation API")

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

# Add middleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logging_provider = get_logging_provider()
        try:
            response = await call_next(request)
            logging_provider.log_request(
                path=request.url.path,
                method=request.method,
                status_code=response.status_code
            )
            return response
        except Exception as e:
            logging_provider.log_error(str(e))
            raise

app.add_middleware(LoggingMiddleware)

# Add new endpoints
class ValidationRequest(BaseModel):
    input_path: str
    output_path: Optional[str] = None

class ImageGenerationRequest(BaseModel):
    recipe_data: Dict[str, Any]
    output_dir: Optional[str] = "data/images"

@app.post("/validate")
async def validate_endpoint(request: ValidationRequest):
    provider = get_validation_provider()
    validation_result = provider.validate(request.input_path)
    return {"validation_result": validation_result}

@app.post("/generate-images")
async def generate_images(request: ImageGenerationRequest):
    provider = get_image_provider()
    image_paths = provider.generate_images(request.recipe_data)
    return {"image_paths": image_paths}