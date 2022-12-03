# Storytime

<div>

[![Build status](https://github.com/myrontuttle/storytime/workflows/build/badge.svg?branch=main&event=push)](https://github.com/myrontuttle/storytime/actions?query=workflow%3Abuild)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/myrontuttle/storytime/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/myrontuttle/storytime/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/myrontuttle/storytime/releases)
[![License](https://img.shields.io/github/license/myrontuttle/storytime)](https://github.com/myrontuttle/storytime/blob/main/LICENSE)
<!-- [![codecov](https://codecov.io/gh/myrontuttle/storytime/branch/main/graph/badge.svg)](https://codecov.io/gh/myrontuttle/storytime) -->
<!-- [![Python Version](https://img.shields.io/pypi/pyversions/storytime.svg)](https://pypi.org/project/storytime/) -->

Storytime is an experiment in continuous storytelling. It is mainly a demonstration of using large language models (LLM) and other machine learning techniques to generate entertainment.

</div>


## Installation

```bash
pip install -U storytime
```

or install with `Poetry`

```bash
poetry add storytime
```

## Dependencies

- [Python](https://www.python.org/) 3.7.2+
- [openai-python](https://github.com/openai/openai-python) Requires an [OpenAI API key](https://beta.openai.com/docs/api-reference/authentication) for story and image generation.
- [googleapis/python-texttospeech](https://github.com/googleapis/python-texttospeech) Requires a [Google Cloud Platform API key](https://cloud.google.com/docs/authentication/getting-started) for narration

## Usage

```python
import storytime

# Generate a story with images
fairy_tale = generate_story(
        "fairy tale",
        with_images=True,
    )

# Save the story to a file
fairy_tale.save_as_json()

# Download the images
fairy_tale.download_image_set()

# Add narration for the story
fairy_tale.add_narration()

# Print the story
print(fairy_tale)
```

### Makefile usage

[`Makefile`](https://github.com/myrontuttle/storytime/blob/master/Makefile) contains a lot of functions for faster development.

<details>
<summary>1. Download and remove Poetry</summary>
<p>

To download and install Poetry run:

```bash
make poetry-download
```

To uninstall

```bash
make poetry-remove
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks coulb be installed after `git init` via

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>3. Codestyle</summary>
<p>

Automatic formatting uses `pyupgrade`, `isort` and `black`.

```bash
make codestyle

# or use synonym
make formatting
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

> Note: `check-codestyle` uses `isort`, `black` and `darglint` library

Update all dev libraries to the latest version using one comand

```bash
make update-dev-deps
```

</p>
</details>

<details>
<summary>4. Code security</summary>
<p>

```bash
make check-safety
```

This command launches `Poetry` integrity checks as well as identifies security issues with `Safety` and `Bandit`.

```bash
make check-safety
```

</p>
</details>

<details>
<summary>5. Type checks</summary>
<p>

Run `mypy` static type checker

```bash
make mypy
```

</p>
</details>

<details>
<summary>6. Tests with coverage badges</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>7. All linters</summary>
<p>

Of course there is a command to ~~rule~~ run all linters in one:

```bash
make lint
```

the same as:

```bash
make test && make check-codestyle && make mypy && make check-safety
```

</p>
</details>

<details>
<summary>8. Docker</summary>
<p>

```bash
make docker-build
```

which is equivalent to:

```bash
make docker-build VERSION=latest
```

Remove docker image with

```bash
make docker-remove
```

More information [about docker](https://github.com/myrontuttle/storytime/tree/master/docker).

</p>
</details>

<details>
<summary>9. Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/myrontuttle/storytime/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

## 🛡 License

[![License](https://img.shields.io/github/license/myrontuttle/storytime)](https://github.com/myrontuttle/storytime/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/myrontuttle/storytime/blob/master/LICENSE) for more details.

## 📃 Citation

```bibtex
@misc{storytime,
  author = {Myron Tuttle},
  title = {Storytime is an experiment in continuous storytelling.},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/myrontuttle/storytime}}
}
```

## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)

Title font: MangabeyRegular Niskala Huruf
license: Freeware
link: https://www.fontspace.com/mangabey-font-f68391
