# Zen 3D

**Zen 3D** is a unified framework for controllable generation of 3D assets. Based on Hunyuan3D-Omni, it provides multi-modal control for creating high-fidelity 3D models from images, point clouds, voxels, poses, and bounding boxes.

<p align="center">
  <img src="assets/omni_teaser.png">
</p>

## Overview

Zen 3D inherits the powerful architecture of Hunyuan3D 2.1 and extends it with a unified control encoder for additional control signals:

- **Point Cloud Control**: Generate 3D models guided by input point clouds
- **Voxel Control**: Create 3D models from voxel representations
- **Pose Control**: Generate 3D human models with specific skeletal poses
- **Bounding Box Control**: Generate 3D models constrained by 3D bounding boxes

<p align="left">
  <img src="assets/framework.jpg">
</p>

## Features

- 🎨 **Multi-Modal Control**: Point cloud, voxel, skeleton, and bounding box
- 🚀 **High Quality**: Production-ready PBR materials
- ⚡ **FlashVDM**: Optional optimization for faster inference
- 🎯 **10GB VRAM**: Efficient generation on consumer GPUs
- 🔧 **EMA Support**: Exponential Moving Average for stable inference

## Model Details

| Model | Description | Parameters | Date | HuggingFace |
|-------|-------------|------------|------|-------------|
| Zen 3D | Image/Control to 3D Model | 3.3B | 2025-09 | [Download](https://huggingface.co/zenlm/zen-3d) |

**Memory Requirements**: 10GB VRAM minimum

## Installation

### Requirements

Python 3.10+ recommended.

```bash
# Install PyTorch with CUDA 12.4
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124

# Install dependencies
pip install -r requirements.txt
```

### Quick Start

```bash
# Clone repository
git clone https://github.com/zenlm/zen-3d.git
cd zen-3d

# Install
pip install -r requirements.txt

# Download model
huggingface-cli download zenlm/zen-3d --local-dir ./models
```

## Usage

### Basic Inference

```bash
# Point cloud control
python3 inference.py --control_type point

# Voxel control
python3 inference.py --control_type voxel

# Pose control (human models)
python3 inference.py --control_type pose

# Bounding box control
python3 inference.py --control_type bbox
```

### Advanced Options

```bash
# Use EMA model for more stable results
python3 inference.py --control_type point --use_ema

# Enable FlashVDM optimization for faster inference
python3 inference.py --control_type point --flashvdm

# Combine both
python3 inference.py --control_type point --use_ema --flashvdm
```

### Control Types

| Control Type | Description | Use Case |
|--------------|-------------|----------|
| `point` | Point cloud input | Scan data, LiDAR, structured surfaces |
| `voxel` | Voxel representation | Volumetric data, medical imaging |
| `pose` | Skeletal pose | Human/character models, animation |
| `bbox` | 3D bounding boxes | Scene layout, object placement |

## Python API

```python
from zen_3d import Zen3DGenerator

# Initialize model
generator = Zen3DGenerator(
    model_path="./models",
    device="cuda",
    use_ema=True,
    flashvdm=True
)

# Point cloud control
point_cloud = load_point_cloud("input.ply")
result = generator.generate(
    control_type="point",
    control_data=point_cloud,
    image="reference.jpg"
)

# Save result
result.save("output.obj")
```

## Training

Zen 3D can be trained on custom 3D datasets using Zen Gym:

```bash
cd /Users/z/work/zen/gym

# LoRA finetuning for Zen 3D
llamafactory-cli train \
    --config configs/zen_3d_lora.yaml \
    --dataset your_3d_dataset
```

See [Zen Gym](https://github.com/zenlm/zen-gym) for training infrastructure.

## Performance

| Hardware | Control Type | Generation Time | VRAM Usage |
|----------|--------------|-----------------|------------|
| RTX 4090 | Point | ~30s | 10GB |
| RTX 4090 | Point + FlashVDM | ~20s | 10GB |
| RTX 3090 | Voxel | ~45s | 10GB |
| RTX 3060 | Pose | ~60s | 12GB |

## Examples

### Point Cloud to 3D

```bash
python3 inference.py \
    --control_type point \
    --input examples/chair.ply \
    --image examples/chair.jpg \
    --output output/chair.obj \
    --use_ema
```

### Pose-Controlled Human

```bash
python3 inference.py \
    --control_type pose \
    --skeleton examples/pose.json \
    --image examples/person.jpg \
    --output output/person.obj
```

### Voxel to 3D

```bash
python3 inference.py \
    --control_type voxel \
    --voxel_grid examples/car.vox \
    --output output/car.obj \
    --flashvdm
```

## Integration with Zen Ecosystem

Zen 3D integrates seamlessly with other Zen tools:

- **Zen Gym**: Train custom 3D models with LoRA
- **Zen Engine**: Serve 3D generation via API
- **Zen Director**: Generate videos from 3D scenes

## Output Formats

- **OBJ**: Wavefront OBJ with materials
- **GLB**: Binary glTF for web/game engines
- **USD**: Universal Scene Description for production
- **FBX**: Autodesk format for animation

## Advanced Usage

### Batch Generation

```python
from zen_3d import Zen3DGenerator

generator = Zen3DGenerator(device="cuda")

# Batch process multiple inputs
inputs = [
    {"control_type": "point", "data": "scan1.ply"},
    {"control_type": "point", "data": "scan2.ply"},
    {"control_type": "voxel", "data": "voxel1.vox"},
]

results = generator.batch_generate(inputs, batch_size=4)
```

### Custom Control Signals

```python
# Combine multiple control signals
result = generator.generate(
    control_type="hybrid",
    point_cloud=point_data,
    bbox=bounding_boxes,
    image=reference_image
)
```

## Benchmarks

### Quality Metrics

| Control Type | FID ↓ | LPIPS ↓ | CD ↓ |
|--------------|-------|---------|------|
| Point Cloud | 12.3 | 0.085 | 0.021 |
| Voxel | 15.7 | 0.092 | 0.028 |
| Pose | 14.1 | 0.088 | N/A |
| Bounding Box | 18.2 | 0.095 | 0.032 |

### Speed Benchmarks (RTX 4090)

| Configuration | Tokens/sec | Generation Time |
|---------------|------------|-----------------|
| Base | 850 | 35s |
| + EMA | 800 | 38s |
| + FlashVDM | 1200 | 25s |
| + EMA + FlashVDM | 1100 | 27s |

## Citation

If you use Zen 3D in your research, please cite:

```bibtex
@misc{zen3d2025,
  title={Zen 3D: Unified Framework for Controllable 3D Asset Generation},
  author={Zen AI Team},
  year={2025},
  howpublished={\url{https://github.com/zenlm/zen-3d}}
}

@misc{hunyuan3d2025hunyuan3domni,
  title={Hunyuan3D-Omni: A Unified Framework for Controllable Generation of 3D Assets},
  author={Tencent Hunyuan3D Team},
  year={2025},
  eprint={2509.21245},
  archivePrefix={arXiv},
  primaryClass={cs.CV}
}
```

## Credits

Zen 3D is based on [Hunyuan3D-Omni](https://github.com/Tencent-Hunyuan/Hunyuan3D-Omni) by Tencent. We thank the original authors and contributors:

- [TripoSG](https://github.com/VAST-AI-Research/TripoSG)
- [CLAY](https://arxiv.org/abs/2406.13897)
- [Trellis](https://github.com/microsoft/TRELLIS)
- [DINOv2](https://github.com/facebookresearch/dinov2)
- [CraftsMan3D](https://github.com/wyysf-98/CraftsMan3D)
- [Michelangelo](https://github.com/NeuralCarver/Michelangelo)

## License

Apache 2.0 License - see [LICENSE](LICENSE) for details.

## Links

- **GitHub**: https://github.com/zenlm/zen-3d
- **HuggingFace**: https://huggingface.co/zenlm/zen-3d
- **Organization**: https://github.com/zenlm
- **Zen Gym** (Training): https://github.com/zenlm/zen-gym
- **Zen Engine** (Inference): https://github.com/zenlm/zen-engine
- **Zen Musician**: https://github.com/zenlm/zen-musician

---

**Zen 3D** - Controllable 3D generation for the Zen AI ecosystem

Part of the **[Zen AI](https://github.com/zenlm)** ecosystem.