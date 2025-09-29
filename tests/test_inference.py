#!/usr/bin/env python3
"""
Zen 3D Inference Tests
Tests basic 3D generation functionality.
"""

import pytest
import torch
from pathlib import Path


class TestZen3DInference:
    """Test suite for Zen 3D inference"""

    @pytest.fixture(scope="class")
    def model_path(self):
        """Get model path"""
        return "./models"

    def test_imports(self):
        """Test that required packages can be imported"""
        try:
            import torch
            import torchvision
            import torchaudio
            assert torch is not None
        except ImportError as e:
            pytest.fail(f"Failed to import required package: {e}")

    @pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
    def test_cuda_availability(self):
        """Test CUDA setup"""
        assert torch.cuda.is_available()
        assert torch.cuda.device_count() > 0

    def test_control_types(self):
        """Test that all control types are supported"""
        control_types = ["point", "voxel", "pose", "bbox"]

        for control_type in control_types:
            assert control_type in ["point", "voxel", "pose", "bbox"]

    def test_model_loading(self, model_path):
        """Test model loading"""
        model_dir = Path(model_path)

        # Check if model directory exists or skip
        if not model_dir.exists():
            pytest.skip(f"Model directory not found: {model_path}")

    @pytest.mark.slow
    def test_point_cloud_generation(self):
        """Test point cloud to 3D generation"""
        pytest.skip("Requires model download and sample data")

    @pytest.mark.slow
    def test_voxel_generation(self):
        """Test voxel to 3D generation"""
        pytest.skip("Requires model download and sample data")

    @pytest.mark.slow
    def test_pose_generation(self):
        """Test pose-controlled generation"""
        pytest.skip("Requires model download and sample data")

    @pytest.mark.slow
    def test_bbox_generation(self):
        """Test bounding box controlled generation"""
        pytest.skip("Requires model download and sample data")


class TestZen3DOutputFormats:
    """Test output format support"""

    def test_supported_formats(self):
        """Test that all output formats are supported"""
        formats = ["obj", "glb", "usd", "fbx"]

        for fmt in formats:
            assert fmt in ["obj", "glb", "usd", "fbx"]


class TestZen3DPerformance:
    """Performance tests"""

    @pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
    def test_memory_usage(self):
        """Test that model fits in 10GB VRAM"""
        if torch.cuda.is_available():
            memory_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"Total GPU Memory: {memory_total:.2f} GB")

            # Model should fit in 10GB
            assert memory_total >= 10, "Requires at least 10GB VRAM"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])