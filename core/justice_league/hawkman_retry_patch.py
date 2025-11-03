"""
🔮 ORACLE'S HAWKMAN RETRY PATCH
Adds robust retry logic with exponential backoff for Figma PNG exports
"""

import time
import requests
from typing import Optional, Tuple


def download_with_retry(
    url: str,
    headers: dict,
    max_retries: int = 3,
    timeout: int = 60,
    backoff_factor: float = 2.0
) -> Tuple[bool, Optional[bytes], Optional[str]]:
    """
    Download content with exponential backoff retry logic

    Args:
        url: URL to download
        headers: Request headers (Figma token)
        max_retries: Maximum retry attempts (default: 3)
        timeout: Request timeout in seconds (default: 60)
        backoff_factor: Exponential backoff multiplier (default: 2.0)

    Returns:
        Tuple of (success: bool, content: bytes, error_message: str)
    """
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return (True, response.content, None)

        except requests.exceptions.Timeout as e:
            last_error = f"Timeout after {timeout}s"
            if attempt < max_retries:
                wait_time = backoff_factor ** (attempt - 1)
                print(f"⏳ Timeout on attempt {attempt}/{max_retries}, retrying in {wait_time:.0f}s...")
                time.sleep(wait_time)

        except requests.exceptions.RequestException as e:
            last_error = str(e)
            if attempt < max_retries:
                wait_time = backoff_factor ** (attempt - 1)
                print(f"⚠️ Error on attempt {attempt}/{max_retries}: {e}, retrying in {wait_time:.0f}s...")
                time.sleep(wait_time)

    return (False, None, last_error)


def export_frame_with_retry(
    file_key: str,
    node_id: str,
    node_name: str,
    output_path: str,
    figma_token: str,
    scale: float = 2.0,
    max_retries: int = 3
) -> Tuple[bool, Optional[str]]:
    """
    Export a single Figma frame as PNG with retry logic

    Args:
        file_key: Figma file key
        node_id: Node ID to export
        node_name: Node name for logging
        output_path: Full path where PNG should be saved
        figma_token: Figma API token
        scale: Export scale (1.0-4.0)
        max_retries: Maximum retry attempts

    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    headers = {"X-Figma-Token": figma_token}

    # Step 1: Get image URL from Figma API (with retry)
    api_url = f"https://api.figma.com/v1/images/{file_key}?ids={node_id}&format=png&scale={scale}"

    success, content, error = download_with_retry(api_url, headers, max_retries=max_retries, timeout=60)

    if not success:
        return (False, f"Failed to get image URL: {error}")

    try:
        import json
        data = json.loads(content)

        if 'images' not in data or node_id not in data['images']:
            return (False, "No image URL returned from Figma API")

        image_url = data['images'][node_id]

    except Exception as e:
        return (False, f"Failed to parse Figma API response: {e}")

    # Step 2: Download the actual PNG image (with retry and longer timeout)
    success, image_content, error = download_with_retry(
        image_url,
        headers={},
        max_retries=max_retries,
        timeout=120  # Longer timeout for large images from CDN
    )

    if not success:
        return (False, f"Failed to download PNG: {error}")

    # Step 3: Save to file
    try:
        with open(output_path, 'wb') as f:
            f.write(image_content)
        return (True, None)

    except Exception as e:
        return (False, f"Failed to save file: {e}")
