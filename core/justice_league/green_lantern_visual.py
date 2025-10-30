"""
💚 GREEN LANTERN - THE VISUAL GUARDIAN
Justice League Member: Visual Regression Specialist

Wielding the power of the Green Lantern Ring, this hero protects visual integrity!

Powers:
- Baseline screenshot storage
- Pixel-perfect image comparison (SSIM algorithm)
- Diff image generation with highlights
- Layout shift detection
- Visual change scoring
- Regression reporting
- Baseline management

"In brightest day, in blackest night, no visual bug shall escape my sight!"

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
    logging.warning("Pillow not available - Green Lantern's ring needs power!")

try:
    import numpy as np
    from skimage.metrics import structural_similarity as ssim
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    logging.warning("NumPy/scikit-image not available - Green Lantern's constructs weakened!")

# Narrator system import
try:
    from .mission_control_narrator import get_narrator
    NARRATOR_AVAILABLE = True
except ImportError:
    NARRATOR_AVAILABLE = False

logger = logging.getLogger(__name__)


class GreenLanternVisual:
    """
    💚 Visual regression testing with baseline comparison

    Green Lantern's Powers:
    1. Store baseline screenshots (create constructs)
    2. Compare new screenshots to baseline (detect changes)
    3. Generate diff images highlighting changes (visual constructs)
    4. Calculate similarity scores (measure visual integrity)
    5. Detect layout shifts (catch visual regressions)
    6. Report visual regressions (alert the Justice League)
    """

    def __init__(self, baseline_dir: Optional[str] = None, narrator: Optional[Any] = None):
        """
        Initialize Green Lantern's visual regression system

        Args:
            baseline_dir: Directory to store baseline images (Green Lantern's vault)
            narrator: Mission Control Narrator for coordinated communication
        """
        self.baseline_dir = Path(baseline_dir or '/tmp/aldo-vision-baselines')
        self.baseline_dir.mkdir(parents=True, exist_ok=True)

        self.diff_dir = self.baseline_dir / 'diffs'
        self.diff_dir.mkdir(exist_ok=True)

        self.metadata_dir = self.baseline_dir / 'metadata'
        self.metadata_dir.mkdir(exist_ok=True)

        # Initialize narrator for enhanced UX
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

        logger.info(f"💚 Green Lantern Visual Guard initialized: {self.baseline_dir}")

    def store_baseline(self, image_path: str, test_name: str,
                      metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        💚 Store a screenshot as baseline for future comparisons
        (Create a Green Lantern construct for protection)

        Args:
            image_path: Path to image file
            test_name: Unique name for this test (e.g., 'homepage-desktop')
            metadata: Optional metadata (viewport size, url, etc.)

        Returns:
            Storage result with baseline info
        """
        if not PIL_AVAILABLE:
            return {'error': 'Pillow not available - Green Lantern needs his ring!'}

        logger.info(f"💚 Creating visual baseline construct: {test_name}")

        try:
            # Load image
            img = Image.open(image_path)

            # Generate baseline filename
            baseline_path = self.baseline_dir / f"{test_name}.png"

            # Save as PNG (lossless - perfect construct)
            img.save(baseline_path, 'PNG')

            # Store metadata
            meta = metadata or {}
            meta.update({
                'test_name': test_name,
                'stored_at': datetime.now().isoformat(),
                'image_size': img.size,
                'image_mode': img.mode,
                'baseline_path': str(baseline_path),
                'guardian': '💚 Green Lantern'
            })

            meta_path = self.metadata_dir / f"{test_name}.json"
            with open(meta_path, 'w') as f:
                json.dump(meta, f, indent=2)

            logger.info(f"  ✓ Baseline construct stored: {baseline_path}")

            return {
                'status': 'success',
                'baseline_path': str(baseline_path),
                'metadata_path': str(meta_path),
                'image_size': img.size,
                'test_name': test_name,
                'guardian': '💚 Green Lantern'
            }

        except Exception as e:
            logger.error(f"Failed to store baseline: {e}")
            return {'error': str(e)}

    def compare_to_baseline(self, new_image_path: str, test_name: str,
                           threshold: float = 0.95) -> Dict[str, Any]:
        """
        💚 Compare new screenshot to stored baseline
        (Green Lantern scans for visual threats)

        Args:
            new_image_path: Path to new screenshot
            test_name: Name of test to compare against
            threshold: Similarity threshold (0-1, default 0.95 = 95% similar)

        Returns:
            Comparison results with diff image and scores
        """
        if not PIL_AVAILABLE or not NUMPY_AVAILABLE:
            return {'error': 'Required libraries not available - Ring powerless!'}

        logger.info(f"💚 Green Lantern scanning for visual changes: {test_name}")

        baseline_path = self.baseline_dir / f"{test_name}.png"

        if not baseline_path.exists():
            return {
                'error': 'No baseline found',
                'message': f'No baseline construct exists for {test_name}. Create one first!',
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

            # Convert to numpy arrays (Green Lantern's analytical power)
            baseline_array = np.array(baseline_img)
            new_array = np.array(new_img)

            # Calculate SSIM (Structural Similarity Index) - Ring's scanner
            ssim_score, ssim_diff = ssim(baseline_array, new_array,
                                        channel_axis=2, full=True)

            # Calculate pixel-level difference
            pixel_diff = np.abs(baseline_array.astype(float) - new_array.astype(float))
            pixel_diff_percentage = (np.sum(pixel_diff) / (pixel_diff.size * 255)) * 100

            # Generate diff image (Visual construct of changes)
            diff_image_path = self._generate_diff_image(
                baseline_img, new_img, ssim_diff, test_name
            )

            # Determine if regression (Visual threat detected)
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
                'verdict': self._get_verdict(ssim_score, threshold),
                'guardian': '💚 Green Lantern'
            }

            if is_regression:
                logger.warning(f"  ⚠️ VISUAL REGRESSION DETECTED! Green Lantern alerts the League! Similarity: {ssim_score:.2%}")
            else:
                logger.info(f"  ✓ No visual threats detected. Similarity: {ssim_score:.2%}")

            return results

        except Exception as e:
            logger.error(f"Comparison failed: {e}")
            return {'error': str(e)}

    def _generate_diff_image(self, baseline: Image.Image, new: Image.Image,
                            ssim_diff: np.ndarray, test_name: str) -> str:
        """
        💚 Generate visual diff image highlighting differences
        (Create Green Lantern construct showing changes)

        Args:
            baseline: Baseline PIL Image
            new: New PIL Image
            ssim_diff: SSIM difference matrix
            test_name: Test name for filename

        Returns:
            Path to generated diff image
        """
        try:
            # Create diff highlight image (Green energy constructs)
            diff_highlight = (ssim_diff * 255).astype(np.uint8)
            diff_highlight = 255 - diff_highlight  # Invert (dark = different)

            # Apply colormap (green for differences - Green Lantern style!)
            diff_colored = np.zeros((*diff_highlight.shape, 3), dtype=np.uint8)
            diff_colored[:, :, 0] = 255 - diff_highlight  # Red channel (inverse)
            diff_colored[:, :, 1] = diff_highlight  # Green channel (GL power!)
            diff_colored[:, :, 2] = 255 - diff_highlight  # Blue channel (inverse)

            diff_img = Image.fromarray(diff_colored)

            # Create side-by-side comparison (GL construct triptych)
            width, height = baseline.size
            comparison = Image.new('RGB', (width * 3, height))

            # Paste images
            comparison.paste(baseline, (0, 0))
            comparison.paste(new, (width, 0))
            comparison.paste(diff_img, (width * 2, 0))

            # Add labels with Green Lantern flair
            draw = ImageDraw.Draw(comparison)
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            except:
                font = ImageFont.load_default()

            draw.text((10, 10), "BASELINE (Protected)", fill=(0, 255, 0), font=font)
            draw.text((width + 10, 10), "CURRENT (Scanned)", fill=(0, 255, 0), font=font)
            draw.text((width * 2 + 10, 10), "DIFF (Green=Changed)", fill=(0, 255, 0), font=font)

            # Save diff image
            diff_path = self.diff_dir / f"{test_name}_diff_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            comparison.save(diff_path, 'PNG')

            logger.info(f"  💚 Green Lantern construct saved: {diff_path}")

            return str(diff_path)

        except Exception as e:
            logger.error(f"Failed to generate diff image: {e}")
            return ""

    def _get_verdict(self, score: float, threshold: float) -> Dict[str, str]:
        """💚 Get Green Lantern's verdict on visual comparison"""
        if score >= 0.99:
            return {
                'grade': 'S+ (Perfect Visual Integrity)',
                'message': 'Images are virtually identical - No threats detected!',
                'color': 'green',
                'lantern_status': 'Ring at 100% power'
            }
        elif score >= threshold:
            return {
                'grade': 'A (Protected)',
                'message': 'Minor differences within acceptable range - Sector secure',
                'color': 'green',
                'lantern_status': 'Ring stable'
            }
        elif score >= threshold - 0.05:
            return {
                'grade': 'B (Warning)',
                'message': 'Noticeable differences detected - Investigation recommended',
                'color': 'yellow',
                'lantern_status': 'Ring detecting anomalies'
            }
        else:
            return {
                'grade': 'F (Visual Threat)',
                'message': 'Significant visual regression detected - Alert Justice League!',
                'color': 'red',
                'lantern_status': 'Ring on high alert!'
            }

    def list_baselines(self) -> List[Dict[str, Any]]:
        """💚 List all stored baseline constructs"""
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
                'metadata': metadata,
                'guardian': '💚 Green Lantern'
            })

        return baselines

    def delete_baseline(self, test_name: str) -> Dict[str, Any]:
        """💚 Delete a stored baseline construct"""
        baseline_path = self.baseline_dir / f"{test_name}.png"
        meta_path = self.metadata_dir / f"{test_name}.json"

        if not baseline_path.exists():
            return {'error': f'No baseline construct found for {test_name}'}

        try:
            baseline_path.unlink()
            if meta_path.exists():
                meta_path.unlink()

            logger.info(f"💚 Green Lantern deleted construct: {test_name}")

            return {
                'status': 'success',
                'message': f'Baseline construct {test_name} deleted',
                'guardian': '💚 Green Lantern'
            }

        except Exception as e:
            return {'error': str(e)}

    def generate_report(self, comparisons: List[Dict]) -> Dict[str, Any]:
        """
        💚 Generate Green Lantern's summary report for multiple comparisons

        Args:
            comparisons: List of comparison results

        Returns:
            Summary report from the Visual Guardian
        """
        total = len(comparisons)
        if total == 0:
            return {'message': 'No comparisons to report - All quiet in this sector'}

        passed = sum(1 for c in comparisons if not c.get('is_regression', False))
        failed = total - passed

        avg_similarity = sum(c.get('similarity_score', 0) for c in comparisons) / total

        report = {
            'summary': {
                'total_tests': total,
                'passed': passed,
                'failed': failed,
                'pass_rate': (passed / total) * 100,
                'average_similarity': avg_similarity,
                'guardian': '💚 Green Lantern - Visual Guardian'
            },
            'failed_tests': [c for c in comparisons if c.get('is_regression')],
            'passed_tests': [c for c in comparisons if not c.get('is_regression')],
            'generated_at': datetime.now().isoformat(),
            'verdict': self._get_sector_status(passed, total)
        }

        return report

    def _get_sector_status(self, passed: int, total: int) -> str:
        """Get overall sector status"""
        rate = (passed / total) * 100 if total > 0 else 100

        if rate == 100:
            return "✅ All sectors protected - Visual integrity at 100%"
        elif rate >= 90:
            return "⚠️ Most sectors protected - Minor visual anomalies detected"
        elif rate >= 75:
            return "⚠️ Multiple visual threats detected - Ring power needed"
        else:
            return "🚨 ALERT: Major visual regressions detected - Justice League assistance required!"

    # Missing methods for audit compatibility
    def create_baseline(self, image_path: str, test_name: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Alias for store_baseline"""
        return self.store_baseline(image_path, test_name, metadata)

    def batch_compare(self, image_paths: List[tuple], threshold: float = 0.95) -> Dict[str, Any]:
        """
        💚 Batch compare multiple screenshots to their baselines

        Args:
            image_paths: List of tuples [(image_path, test_name), ...]
            threshold: Similarity threshold

        Returns:
            Batch comparison results
        """
        results = []
        for image_path, test_name in image_paths:
            try:
                comparison = self.compare_to_baseline(image_path, test_name, threshold)
                results.append({
                    'test_name': test_name,
                    'comparison': comparison
                })
            except Exception as e:
                results.append({
                    'test_name': test_name,
                    'error': str(e)
                })

        passed = sum(1 for r in results if not r.get('comparison', {}).get('is_regression', True))
        total = len(results)

        return {
            'total_tests': total,
            'passed': passed,
            'failed': total - passed,
            'pass_rate': (passed / total * 100) if total > 0 else 0,
            'results': results
        }

    def _calculate_ssim(self, img1_array: np.ndarray, img2_array: np.ndarray) -> tuple:
        """
        Calculate SSIM (Structural Similarity Index) between two images

        Args:
            img1_array: First image as numpy array
            img2_array: Second image as numpy array

        Returns:
            Tuple of (ssim_score, ssim_diff_matrix)
        """
        try:
            from skimage.metrics import structural_similarity as ssim
            ssim_score, ssim_diff = ssim(img1_array, img2_array, channel_axis=2, full=True)
            return (float(ssim_score), ssim_diff)
        except Exception as e:
            logger.error(f"SSIM calculation failed: {e}")
            return (0.0, np.zeros_like(img1_array[:, :, 0]))

    def _calculate_green_lantern_score(self, comparison_results: Dict) -> Dict[str, Any]:
        """
        💚 Calculate Green Lantern's visual integrity score

        Args:
            comparison_results: Comparison results

        Returns:
            Green Lantern score with grade
        """
        similarity = comparison_results.get('similarity_score', 0) * 100
        is_regression = comparison_results.get('is_regression', True)

        # Base score from similarity
        score = similarity

        # Penalty for regression
        if is_regression:
            score -= 10

        # Ensure score is 0-100
        score = max(0, min(100, score))

        # Grade
        if score >= 99:
            grade = "S+ (Perfect Match)"
            verdict = "💚 IN BRIGHTEST DAY! Visual integrity at 100%!"
        elif score >= 95:
            grade = "S (Exceptional)"
            verdict = "💚 EXCELLENT! Minimal visual changes detected!"
        elif score >= 90:
            grade = "A+ (Outstanding)"
            verdict = "💚 VERY GOOD! Minor visual differences!"
        elif score >= 85:
            grade = "A (Great)"
            verdict = "💚 GOOD! Some visual changes present!"
        elif score >= 75:
            grade = "B (Acceptable)"
            verdict = "💚 ACCEPTABLE! Noticeable visual changes!"
        else:
            grade = "C or below (Regression)"
            verdict = "💚 IN BLACKEST NIGHT! Major visual regression detected!"

        return {
            'score': score,
            'grade': grade,
            'verdict': verdict,
            'similarity_percent': similarity,
            'is_regression': is_regression
        }

    def _generate_willpower_recommendations(self, comparison: Dict) -> List[Dict[str, Any]]:
        """
        💚 Generate Green Lantern's willpower recommendations

        Args:
            comparison: Comparison results

        Returns:
            List of recommendations
        """
        recommendations = []

        is_regression = comparison.get('is_regression', False)
        similarity = comparison.get('similarity_score', 1.0) * 100

        if is_regression:
            recommendations.append({
                'priority': 'high',
                'area': 'Visual Regression',
                'issue': f'Visual regression detected (similarity: {similarity:.1f}%)',
                'recommendation': 'Review visual changes and update baseline if intentional',
                'green_lantern_says': 'The Ring detects unauthorized visual changes!'
            })

        if similarity < 90:
            recommendations.append({
                'priority': 'medium',
                'area': 'Visual Consistency',
                'issue': f'Low visual similarity ({similarity:.1f}%)',
                'recommendation': 'Investigate significant visual differences',
                'green_lantern_says': 'Visual constructs are unstable!'
            })

        if not recommendations:
            recommendations.append({
                'priority': 'low',
                'area': 'Visual Quality',
                'issue': 'No visual regressions detected',
                'recommendation': 'Maintain current visual quality',
                'green_lantern_says': 'All sectors protected! Visual integrity maintained!'
            })

        return recommendations

    def _load_baseline(self, test_name: str) -> Optional[Dict]:
        """Load baseline metadata from JSON file"""
        metadata_file = self.baseline_dir / f"{test_name}_metadata.json"

        if not metadata_file.exists():
            return None

        try:
            with open(metadata_file, 'r') as f:
                import json
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load baseline metadata {test_name}: {e}")
            return None

    def _save_baseline(self, test_name: str, metadata: Dict) -> None:
        """Save baseline metadata to JSON file"""
        metadata_file = self.baseline_dir / f"{test_name}_metadata.json"

        try:
            with open(metadata_file, 'w') as f:
                import json
                json.dump(metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save baseline metadata {test_name}: {e}")


# Main entry points - Green Lantern's Mission Interface
def green_lantern_store_baseline(image_path: str, test_name: str,
                                 metadata: Optional[Dict] = None,
                                 baseline_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    💚 Green Lantern stores screenshot as baseline construct

    Args:
        image_path: Path to screenshot
        test_name: Unique test name
        metadata: Optional metadata
        baseline_dir: Optional custom baseline directory

    Returns:
        Storage result
    """
    gl = GreenLanternVisual(baseline_dir)
    return gl.store_baseline(image_path, test_name, metadata)


def green_lantern_compare_screenshots(new_image_path: str, test_name: str,
                                      threshold: float = 0.95,
                                      baseline_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    💚 Green Lantern compares screenshot to baseline

    Args:
        new_image_path: Path to new screenshot
        test_name: Test name to compare against
        threshold: Similarity threshold (default 0.95)
        baseline_dir: Optional custom baseline directory

    Returns:
        Comparison results with diff image
    """
    gl = GreenLanternVisual(baseline_dir)
    return gl.compare_to_baseline(new_image_path, test_name, threshold)


def green_lantern_list_baselines(baseline_dir: Optional[str] = None) -> List[Dict]:
    """💚 Green Lantern lists all stored baseline constructs"""
    gl = GreenLanternVisual(baseline_dir)
    return gl.list_baselines()


def green_lantern_delete_baseline(test_name: str, baseline_dir: Optional[str] = None) -> Dict[str, Any]:
    """💚 Green Lantern deletes a baseline construct"""
    gl = GreenLanternVisual(baseline_dir)
    return gl.delete_baseline(test_name)


def green_lantern_visual_regression(new_image_path: str, test_name: str,
                                    threshold: float = 0.95,
                                    baseline_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    💚 Green Lantern's complete visual regression testing workflow

    Alias for green_lantern_compare_screenshots - provides complete visual regression analysis

    Args:
        new_image_path: Path to new screenshot to test
        test_name: Test name to compare against baseline
        threshold: Similarity threshold (0.0-1.0, default 0.95)
        baseline_dir: Optional custom baseline directory

    Returns:
        Complete visual regression analysis from Green Lantern
    """
    return green_lantern_compare_screenshots(new_image_path, test_name, threshold, baseline_dir)
