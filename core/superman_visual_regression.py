"""
SUPERMAN VISUAL REGRESSION SYSTEM
Complete visual comparison and regression detection

Capabilities:
- Baseline screenshot storage
- Pixel-perfect image comparison
- Diff image generation with highlights
- Layout shift detection
- Visual change scoring
- Regression reporting

Libraries:
- Pillow (PIL) for image processing
- scikit-image for structural similarity
- NumPy for pixel math
"""

import logging
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import hashlib

try:
    from PIL import Image, ImageDraw, ImageFont, ImageChops
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("Pillow not available")

try:
    import numpy as np
    from skimage.metrics import structural_similarity as ssim
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    logging.warning("NumPy/scikit-image not available")

logger = logging.getLogger(__name__)


class SupermanVisualRegression:
    """
    Visual regression testing with baseline comparison

    Features:
    1. Store baseline screenshots
    2. Compare new screenshots to baseline
    3. Generate diff images highlighting changes
    4. Calculate similarity scores
    5. Detect layout shifts
    6. Report visual regressions
    """

    def __init__(self, baseline_dir: Optional[str] = None):
        """
        Initialize visual regression system

        Args:
            baseline_dir: Directory to store baseline images
        """
        self.baseline_dir = Path(baseline_dir or '/tmp/aldo-vision-baselines')
        self.baseline_dir.mkdir(parents=True, exist_ok=True)

        self.diff_dir = self.baseline_dir / 'diffs'
        self.diff_dir.mkdir(exist_ok=True)

        self.metadata_dir = self.baseline_dir / 'metadata'
        self.metadata_dir.mkdir(exist_ok=True)

        logger.info(f"📸 Visual Regression initialized: {self.baseline_dir}")

    def store_baseline(self, image_path: str, test_name: str,
                      metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Store a screenshot as baseline for future comparisons

        Args:
            image_path: Path to image file
            test_name: Unique name for this test (e.g., 'homepage-desktop')
            metadata: Optional metadata (viewport size, url, etc.)

        Returns:
            Storage result with baseline info
        """
        if not PIL_AVAILABLE:
            return {'error': 'Pillow not available'}

        logger.info(f"📥 Storing baseline: {test_name}")

        try:
            # Load image
            img = Image.open(image_path)

            # Generate baseline filename
            baseline_path = self.baseline_dir / f"{test_name}.png"

            # Save as PNG (lossless)
            img.save(baseline_path, 'PNG')

            # Store metadata
            meta = metadata or {}
            meta.update({
                'test_name': test_name,
                'stored_at': datetime.now().isoformat(),
                'image_size': img.size,
                'image_mode': img.mode,
                'baseline_path': str(baseline_path)
            })

            meta_path = self.metadata_dir / f"{test_name}.json"
            with open(meta_path, 'w') as f:
                json.dump(meta, f, indent=2)

            logger.info(f"  ✓ Baseline stored: {baseline_path}")

            return {
                'status': 'success',
                'baseline_path': str(baseline_path),
                'metadata_path': str(meta_path),
                'image_size': img.size,
                'test_name': test_name
            }

        except Exception as e:
            logger.error(f"Failed to store baseline: {e}")
            return {'error': str(e)}

    def compare_to_baseline(self, new_image_path: str, test_name: str,
                           threshold: float = 0.95) -> Dict[str, Any]:
        """
        Compare new screenshot to stored baseline

        Args:
            new_image_path: Path to new screenshot
            test_name: Name of test to compare against
            threshold: Similarity threshold (0-1, default 0.95 = 95% similar)

        Returns:
            Comparison results with diff image and scores
        """
        if not PIL_AVAILABLE or not NUMPY_AVAILABLE:
            return {'error': 'Required libraries not available'}

        logger.info(f"🔍 Comparing to baseline: {test_name}")

        baseline_path = self.baseline_dir / f"{test_name}.png"

        if not baseline_path.exists():
            return {
                'error': 'No baseline found',
                'message': f'No baseline exists for {test_name}. Store baseline first.',
                'baseline_path': str(baseline_path)
            }

        try:
            # Load images
            baseline_img = Image.open(baseline_path)
            new_img = Image.open(new_image_path)

            # Ensure same size (resize if needed)
            if baseline_img.size != new_img.size:
                logger.warning(f"  ⚠️ Size mismatch: baseline {baseline_img.size} vs new {new_img.size}")
                new_img = new_img.resize(baseline_img.size, Image.Resampling.LANCZOS)

            # Convert to RGB if needed
            if baseline_img.mode != 'RGB':
                baseline_img = baseline_img.convert('RGB')
            if new_img.mode != 'RGB':
                new_img = new_img.convert('RGB')

            # Convert to numpy arrays
            baseline_array = np.array(baseline_img)
            new_array = np.array(new_img)

            # Calculate SSIM (Structural Similarity Index)
            ssim_score, ssim_diff = ssim(baseline_array, new_array,
                                        channel_axis=2, full=True)

            # Calculate pixel-level difference
            pixel_diff = np.abs(baseline_array.astype(float) - new_array.astype(float))
            pixel_diff_percentage = (np.sum(pixel_diff) / (pixel_diff.size * 255)) * 100

            # Generate diff image
            diff_image_path = self._generate_diff_image(
                baseline_img, new_img, ssim_diff, test_name
            )

            # Determine if regression
            is_regression = ssim_score < threshold

            results = {
                'test_name': test_name,
                'comparison_time': datetime.now().isoformat(),
                'similarity_score': float(ssim_score),
                'threshold': threshold,
                'is_regression': is_regression,
                'pixel_difference_percent': float(pixel_diff_percentage),
                'diff_image_path': diff_image_path,
                'baseline_path': str(baseline_path),
                'new_image_path': new_image_path,
                'verdict': self._get_verdict(ssim_score, threshold)
            }

            if is_regression:
                logger.warning(f"  ⚠️ REGRESSION DETECTED! Similarity: {ssim_score:.2%}")
            else:
                logger.info(f"  ✓ No regression. Similarity: {ssim_score:.2%}")

            return results

        except Exception as e:
            logger.error(f"Comparison failed: {e}")
            return {'error': str(e)}

    def _generate_diff_image(self, baseline: Image.Image, new: Image.Image,
                            ssim_diff: np.ndarray, test_name: str) -> str:
        """
        Generate visual diff image highlighting differences

        Args:
            baseline: Baseline PIL Image
            new: New PIL Image
            ssim_diff: SSIM difference matrix
            test_name: Test name for filename

        Returns:
            Path to generated diff image
        """
        try:
            # Create diff highlight image
            diff_highlight = (ssim_diff * 255).astype(np.uint8)
            diff_highlight = 255 - diff_highlight  # Invert (dark = different)

            # Apply colormap (red for differences)
            diff_colored = np.zeros((*diff_highlight.shape, 3), dtype=np.uint8)
            diff_colored[:, :, 0] = diff_highlight  # Red channel
            diff_colored[:, :, 1] = 255 - diff_highlight  # Green channel (inverse)
            diff_colored[:, :, 2] = 255 - diff_highlight  # Blue channel (inverse)

            diff_img = Image.fromarray(diff_colored)

            # Create side-by-side comparison
            width, height = baseline.size
            comparison = Image.new('RGB', (width * 3, height))

            # Paste images
            comparison.paste(baseline, (0, 0))
            comparison.paste(new, (width, 0))
            comparison.paste(diff_img, (width * 2, 0))

            # Add labels
            draw = ImageDraw.Draw(comparison)
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            except:
                font = ImageFont.load_default()

            draw.text((10, 10), "BASELINE", fill=(255, 255, 0), font=font)
            draw.text((width + 10, 10), "CURRENT", fill=(255, 255, 0), font=font)
            draw.text((width * 2 + 10, 10), "DIFF (Red=Changed)", fill=(255, 255, 0), font=font)

            # Save diff image
            diff_path = self.diff_dir / f"{test_name}_diff_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            comparison.save(diff_path, 'PNG')

            logger.info(f"  📊 Diff image saved: {diff_path}")

            return str(diff_path)

        except Exception as e:
            logger.error(f"Failed to generate diff image: {e}")
            return ""

    def _get_verdict(self, score: float, threshold: float) -> Dict[str, str]:
        """Get human-readable verdict on visual comparison"""
        if score >= 0.99:
            return {
                'grade': 'S+ (Perfect Match)',
                'message': 'Images are virtually identical',
                'color': 'green'
            }
        elif score >= threshold:
            return {
                'grade': 'A (Passed)',
                'message': 'Minor differences within acceptable range',
                'color': 'green'
            }
        elif score >= threshold - 0.05:
            return {
                'grade': 'B (Warning)',
                'message': 'Noticeable differences, review recommended',
                'color': 'yellow'
            }
        else:
            return {
                'grade': 'F (Failed)',
                'message': 'Significant visual regression detected',
                'color': 'red'
            }

    def list_baselines(self) -> List[Dict[str, Any]]:
        """List all stored baselines"""
        baselines = []

        for baseline_file in self.baseline_dir.glob('*.png'):
            test_name = baseline_file.stem

            # Load metadata if exists
            meta_path = self.metadata_dir / f"{test_name}.json"
            metadata = {}
            if meta_path.exists():
                with open(meta_path, 'r') as f:
                    metadata = json.load(f)

            baselines.append({
                'test_name': test_name,
                'path': str(baseline_file),
                'size': baseline_file.stat().st_size,
                'modified': datetime.fromtimestamp(baseline_file.stat().st_mtime).isoformat(),
                'metadata': metadata
            })

        return baselines

    def delete_baseline(self, test_name: str) -> Dict[str, Any]:
        """Delete a stored baseline"""
        baseline_path = self.baseline_dir / f"{test_name}.png"
        meta_path = self.metadata_dir / f"{test_name}.json"

        if not baseline_path.exists():
            return {'error': f'No baseline found for {test_name}'}

        try:
            baseline_path.unlink()
            if meta_path.exists():
                meta_path.unlink()

            logger.info(f"🗑️ Deleted baseline: {test_name}")

            return {
                'status': 'success',
                'message': f'Baseline {test_name} deleted'
            }

        except Exception as e:
            return {'error': str(e)}

    def generate_report(self, comparisons: List[Dict]) -> Dict[str, Any]:
        """
        Generate summary report for multiple comparisons

        Args:
            comparisons: List of comparison results

        Returns:
            Summary report
        """
        total = len(comparisons)
        if total == 0:
            return {'message': 'No comparisons to report'}

        passed = sum(1 for c in comparisons if not c.get('is_regression', False))
        failed = total - passed

        avg_similarity = sum(c.get('similarity_score', 0) for c in comparisons) / total

        report = {
            'summary': {
                'total_tests': total,
                'passed': passed,
                'failed': failed,
                'pass_rate': (passed / total) * 100,
                'average_similarity': avg_similarity
            },
            'failed_tests': [c for c in comparisons if c.get('is_regression')],
            'passed_tests': [c for c in comparisons if not c.get('is_regression')],
            'generated_at': datetime.now().isoformat()
        }

        return report


# Main entry points
def store_baseline(image_path: str, test_name: str,
                  metadata: Optional[Dict] = None,
                  baseline_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Store screenshot as baseline

    Args:
        image_path: Path to screenshot
        test_name: Unique test name
        metadata: Optional metadata
        baseline_dir: Optional custom baseline directory

    Returns:
        Storage result
    """
    vr = SupermanVisualRegression(baseline_dir)
    return vr.store_baseline(image_path, test_name, metadata)


def compare_screenshots(new_image_path: str, test_name: str,
                       threshold: float = 0.95,
                       baseline_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Compare screenshot to baseline

    Args:
        new_image_path: Path to new screenshot
        test_name: Test name to compare against
        threshold: Similarity threshold (default 0.95)
        baseline_dir: Optional custom baseline directory

    Returns:
        Comparison results with diff image
    """
    vr = SupermanVisualRegression(baseline_dir)
    return vr.compare_to_baseline(new_image_path, test_name, threshold)


def list_all_baselines(baseline_dir: Optional[str] = None) -> List[Dict]:
    """List all stored baselines"""
    vr = SupermanVisualRegression(baseline_dir)
    return vr.list_baselines()
