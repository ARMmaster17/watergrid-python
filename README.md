# WaterGrid-Python
[![WaterGrid Tests](https://github.com/ARMmaster17/watergrid-python/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ARMmaster17/watergrid-python/actions/workflows/ci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/5ecd1367c30a9a8a5c59/maintainability)](https://codeclimate.com/github/ARMmaster17/watergrid-python/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/5ecd1367c30a9a8a5c59/test_coverage)](https://codeclimate.com/github/ARMmaster17/watergrid-python/test_coverage)
![PyPI](https://img.shields.io/pypi/v/watergrid)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Watergrid is a lightweight, distributed framework for data stream processing.

## Why Watergrid

- Watergrid lets developers write their ETL pipelines as applications, not 
scripts or jobs. This lets you re-use your existing CI/CD infrastructure and
deployment practices.
- Watergrid encourages you to write your ETL operations as modular "steps",
making it easy to isolate and test atomic parts of your pipelines.
- Watergrid lets you scale up to multi-node clusters by changing only a few
lines of Python code.
- Watergrid is minimalistic, and easy to use.
- Watergrid does not depend on complicated software setups that execute jobs.
Everything is self-contained in the library itself.
- Watergrid lets you use your existing Redis infrastructure for distributed
jobs instead of a proprietary data storage/transmission solution.
- Watergrid includes an API for interfacing with an APM of your choice out of
the box.

## Getting Started

Creating an ETL pipeline with Watergrid is very easy.

1. Install Python 3.6 or later (other versions may be supported, but are not tested regularly).
1. Run `pip install watergrid`
1. Paste the following code into a file named `main.py`:

```python
from watergrid.pipelines.standalone_pipeline import StandalonePipeline
from watergrid.steps import Step
from watergrid.context import DataContext

class SampleStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    def run(self, context: DataContext):
        print("Hello World!")

def main():
   pipeline = StandalonePipeline('hello_world_pipeline')
   pipeline.add_step(SampleStep())
   while True:
    pipeline.run()

if __name__ == '__main__':
   main()
```

Then run `python main.py` to run the pipeline. You should see Hello World!
printed to the console.

Check out the [getting started section of the documentation site](https://armmaster17.github.io/watergrid-python/getting_started.html)
to build more advanced pipelines with multiple steps and high-availability.

## Getting Help

There are plenty of places to get help with Watergrid.

- Check the in-line documentation in the Python source.
- Read the online documentation on [GitHub Pages](https://armmaster17.github.io/watergrid-python/index.html).
- Make a post in the [Discussions Tab](https://github.com/ARMmaster17/watergrid-python/discussions).
- Open an issue if you think the problem is with Watergrid, or if you have a
feature to suggest.

## Example Projects

- [RSSMQ](https://github.com/ARMmaster17/rssmq/tree/126-refactor-to-use-watergrid) - Forwards RSS feed items to various HTTP APIs.
- [atc-metrics-streamer](https://github.com/ARMmaster17/atc-metrics-streamer) - Streams metrics from Apache Traffic Control to Kafka.
