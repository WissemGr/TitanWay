import os
import json
import httpx

# Define the API URL
api_url = ""


# Define the Swagger JSON URL
swagger_url = api_url + "/swagger/v1/swagger.json"

# Function to generate the FastAPI route code from Swagger JSON
def generate_route_code(swagger_json, service_name):
    route_file_content = f"""from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import httpx

router = APIRouter()
tag = "{service_name}"

"""

    for path, path_data in swagger_json["paths"].items():
        for http_method, http_data in path_data.items():
            operation_id = http_data.get("operationId", http_method)
            route_function = f"""
@router.{http_method}("{path}", tags=[tag])
async def {operation_id}(*, depends: Depends = Depends()):
    url = f"{api_url}{path}"
    async with httpx.AsyncClient() as client:
        response = await client.{http_method}(url)
    return JSONResponse(content=response.json(), status_code=response.status_code)
"""
            route_file_content += route_function

    return route_file_content

# Fetch Swagger JSON from the URL
async def fetch_swagger_json(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

# Main script
async def main():
    # Fetch Swagger JSON from the URL
    swagger_json_str = await fetch_swagger_json(swagger_url)
    swagger_json = json.loads(swagger_json_str)

    # Extract service name from the Swagger JSON (customize this based on your Swagger structure)
    service_name = swagger_json["info"]["title"].split('.')[0]

    # Generate route code
    route_code = generate_route_code(swagger_json, service_name)

    # Write the code to a Python file (e.g., service_name.py)
    filename = f"{service_name.lower()}.py"
    with open(filename, "w") as route_file:
        route_file.write(route_code)

    print(f"{filename} generated successfully!")

if __name__ == "__main__":
    import uvicorn
    import asyncio

    # Run the main script asynchronously
    asyncio.run(main())

    # If you want to run the FastAPI application, you can add the code here
    # uvicorn.run(app, host="0.0.0.0", port=8000)
