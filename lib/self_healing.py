"""
🛡️ Justice League Self-Healing Module
Automatic retry logic with exponential backoff for transient failures

Usage:
    from lib.self_healing import execute_with_retry, retry_decorator

    # Option 1: Function wrapper
    result = execute_with_retry(risky_operation, max_retries=3)

    # Option 2: Decorator
    @retry_decorator(max_retries=3)
    def my_api_call():
        return requests.get(url)
"""

import time
import logging
from functools import wraps
from typing import Callable, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransientError(Exception):
    """Temporary error that should be retried"""
    pass


class PermanentError(Exception):
    """Permanent error that should not be retried"""
    pass


def is_transient_error(exception: Exception) -> bool:
    """
    Determine if an error is transient (should retry) or permanent.

    Transient errors:
    - HTTP 500, 502, 503, 504 (server errors)
    - HTTP 429 (rate limit)
    - Connection errors
    - Timeout errors

    Permanent errors:
    - HTTP 400, 401, 403, 404 (client errors)
    - Invalid data
    - Authentication failures
    """
    # Check if it's an HTTP error (requests library)
    if hasattr(exception, 'response') and hasattr(exception.response, 'status_code'):
        status_code = exception.response.status_code

        # Transient errors
        if status_code in [500, 502, 503, 504, 429]:
            return True

        # Permanent errors
        if status_code in [400, 401, 403, 404]:
            return False

    # Check exception type
    exception_name = type(exception).__name__

    # Transient
    transient_errors = [
        'ConnectionError', 'Timeout', 'TimeoutError',
        'ConnectionResetError', 'BrokenPipeError'
    ]
    if exception_name in transient_errors:
        return True

    # Permanent by default (conservative approach)
    return False


def calculate_backoff(attempt: int, base_delay: float = 1.0, max_delay: float = 32.0) -> float:
    """
    Calculate exponential backoff delay.

    Formula: min(base_delay * 2^attempt, max_delay)

    Args:
        attempt: Current retry attempt (0-indexed)
        base_delay: Base delay in seconds (default: 1.0)
        max_delay: Maximum delay in seconds (default: 32.0)

    Returns:
        Delay in seconds

    Examples:
        attempt 0: 1s
        attempt 1: 2s
        attempt 2: 4s
        attempt 3: 8s
        attempt 4: 16s
        attempt 5: 32s (capped)
    """
    delay = base_delay * (2 ** attempt)
    return min(delay, max_delay)


def execute_with_retry(
    operation: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 32.0,
    on_retry: Optional[Callable[[Exception, int], None]] = None
) -> Any:
    """
    Execute an operation with automatic retry on transient failures.

    Args:
        operation: Callable to execute
        max_retries: Maximum number of retry attempts (default: 3)
        base_delay: Base delay for exponential backoff (default: 1.0)
        max_delay: Maximum delay between retries (default: 32.0)
        on_retry: Optional callback function(exception, attempt) called on each retry

    Returns:
        Result of the operation

    Raises:
        PermanentError: If error is permanent
        Exception: If all retries exhausted

    Example:
        def fetch_data():
            return requests.get('https://api.example.com/data')

        result = execute_with_retry(fetch_data, max_retries=3)
    """
    last_exception = None

    for attempt in range(max_retries + 1):  # +1 for initial attempt
        try:
            result = operation()

            # Success! Log if we had previous failures
            if attempt > 0:
                logger.info(f"✅ Operation succeeded after {attempt} retries")

            return result

        except Exception as e:
            last_exception = e

            # Check if error is transient
            if not is_transient_error(e):
                logger.error(f"❌ Permanent error: {type(e).__name__}: {str(e)}")
                raise PermanentError(f"Permanent error: {str(e)}") from e

            # Check if we have retries left
            if attempt >= max_retries:
                logger.error(f"❌ All {max_retries} retries exhausted")
                break

            # Calculate backoff delay
            delay = calculate_backoff(attempt, base_delay, max_delay)

            # Log retry attempt
            logger.warning(
                f"⚠️ Transient error on attempt {attempt + 1}/{max_retries + 1}: "
                f"{type(e).__name__}: {str(e)}"
            )
            logger.info(f"⏳ Retrying in {delay:.1f}s... (attempt {attempt + 2}/{max_retries + 1})")

            # Call retry callback if provided
            if on_retry:
                on_retry(e, attempt)

            # Wait before retry
            time.sleep(delay)

    # All retries exhausted
    logger.error(f"❌ Operation failed after {max_retries + 1} attempts")
    raise last_exception


def retry_decorator(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 32.0,
    on_retry: Optional[Callable[[Exception, int], None]] = None
):
    """
    Decorator for automatic retry with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        base_delay: Base delay for exponential backoff (default: 1.0)
        max_delay: Maximum delay between retries (default: 32.0)
        on_retry: Optional callback function(exception, attempt) called on each retry

    Example:
        @retry_decorator(max_retries=3)
        def fetch_figma_file(file_key):
            response = requests.get(f'https://api.figma.com/v1/files/{file_key}')
            response.raise_for_status()
            return response.json()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            operation = lambda: func(*args, **kwargs)
            return execute_with_retry(
                operation,
                max_retries=max_retries,
                base_delay=base_delay,
                max_delay=max_delay,
                on_retry=on_retry
            )
        return wrapper
    return decorator


# Specialized retry for Figma API
def retry_figma_api(max_retries: int = 3):
    """
    Specialized retry decorator for Figma API calls.
    Includes Figma-specific rate limiting handling.

    Example:
        @retry_figma_api(max_retries=3)
        def get_figma_file(file_key):
            response = requests.get(
                f'https://api.figma.com/v1/files/{file_key}',
                headers={'X-Figma-Token': FIGMA_TOKEN}
            )
            response.raise_for_status()
            return response.json()
    """
    def on_retry_callback(exception, attempt):
        # Figma rate limit: 50 requests/min
        if hasattr(exception, 'response') and exception.response.status_code == 429:
            logger.warning("⏳ Figma rate limit hit - waiting longer before retry")

    return retry_decorator(
        max_retries=max_retries,
        base_delay=2.0,  # Longer initial delay for Figma
        max_delay=60.0,  # Up to 1 minute for rate limits
        on_retry=on_retry_callback
    )


# Example usage and testing
if __name__ == '__main__':
    import requests

    print("🛡️ Testing Self-Healing Module\n")

    # Test 1: Successful operation (no retry needed)
    print("Test 1: Successful operation")
    @retry_decorator(max_retries=3)
    def successful_operation():
        print("  Operation executed successfully")
        return "success"

    result = successful_operation()
    print(f"  Result: {result}\n")

    # Test 2: Transient failure with recovery
    print("Test 2: Transient failure with recovery")
    attempt_count = {'count': 0}

    @retry_decorator(max_retries=3)
    def failing_then_succeeding():
        attempt_count['count'] += 1
        if attempt_count['count'] < 3:
            print(f"  Attempt {attempt_count['count']}: Simulating transient failure")
            raise ConnectionError("Simulated connection error")
        print(f"  Attempt {attempt_count['count']}: Success!")
        return "recovered"

    result = failing_then_succeeding()
    print(f"  Result: {result}\n")

    # Test 3: Exponential backoff demonstration
    print("Test 3: Exponential backoff calculation")
    for i in range(6):
        delay = calculate_backoff(i)
        print(f"  Attempt {i}: Backoff delay = {delay:.1f}s")

    print("\n✅ Self-Healing Module Tests Complete!")
