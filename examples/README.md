# Examples

This directory contains usage examples for the `costs` AI cost tracking library.

Each example is in its own directory with:
- `README.md` - Explanation of the example
- `main.py` or script file - The example code
- `run.sh` - Script to run the example

## Directory Structure

```
examples/
├── 01_tokenizer_basic/
│   ├── README.md
│   ├── main.py
│   └── run.sh
├── 02_multi_model_cost/
│   ├── README.md
│   ├── main.py
│   └── run.sh
├── 03_batch_processing/
│   ├── README.md
│   ├── main.py
│   └── run.sh
├── 04_basic_usage/
│   ├── README.md
│   └── run.sh
├── 05_badge_generation/
│   ├── README.md
│   └── run.sh
├── 06_diff_estimation/
│   ├── README.md
│   └── run.sh
├── 07_pre-commit-hook/
│   ├── README.md
│   ├── pre-commit
│   ├── install.sh
│   └── run.sh
├── 08_github-actions/
│   ├── README.md
│   ├── workflow.yml
│   └── run.sh
├── 09_gitlab-ci/
│   ├── README.md
│   ├── .gitlab-ci.yml
│   └── run.sh
├── 10_custom_pricing/
│   ├── README.md
│   ├── main.py
│   └── run.sh
├── 11_custom_roi/
│   ├── README.md
│   ├── main.py
│   └── run.sh
├── 12_multi_repo/
│   ├── README.md
│   ├── main.py
│   └── run.sh
├── 13_cost_trends/
│   ├── README.md
│   ├── main.py
│   └── run.sh
└── README.md
```

# Run basic tokenizer example
cd examples/01_tokenizer_basic
./run.sh

### CLI Examples

```bash
cd examples/04_basic_usage
./run.sh
```

# Install pre-commit hook
cd examples/07_pre-commit-hook
./install.sh
```

### Advanced Examples

```bash
cd examples/10_custom_pricing
./run.sh
```

## Examples by Category

| Example | Category | Description |
|---------|----------|-------------|
| `01_tokenizer_basic/` | API | Basic token counting with different models |
| `02_multi_model_cost/` | API | Compare costs across providers |
| `03_batch_processing/` | API | Process multiple commits in batch |
| `04_basic_usage/` | CLI | Common CLI commands |
| `05_badge_generation/` | CLI | Badge and report generation |
| `06_diff_estimation/` | CLI | Single diff estimation |
| `07_pre-commit-hook/` | Integration | Auto-update badge on commit |
| `08_github-actions/` | Integration | GitHub Actions workflow |
| `09_gitlab-ci/` | Integration | GitLab CI configuration |
| `10_custom_pricing/` | Advanced | Add custom model pricing |
| `11_custom_roi/` | Advanced | Custom ROI calculations |
| `12_multi_repo/` | Advanced | Analyze multiple repositories |
| `13_cost_trends/` | Advanced | Cost analytics and projections |

## Running Examples

All examples can be run using the provided `run.sh` script:

```bash
cd examples/<example>
./run.sh
```

Or run Python examples directly:

```bash
cd examples/01_tokenizer_basic
python3 main.py
```

## Notes

- API examples use the `costs` Python package
- CLI examples show shell commands (bash/sh compatible)
- Integration examples may need customization for your environment
- Advanced examples demonstrate extending the library
- Each example has its own README with detailed explanation
