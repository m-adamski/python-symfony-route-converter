import os.path

import click
import yaml


@click.command()
@click.argument("source")
def main(source):
    if os.path.exists(source) and os.path.isfile(source):
        content = parse_yaml(source)

        for name, data in content.items():
            data: dict = data

            if name != "controllers":
                path: str = data.get("path")
                methods: list = data.get("methods")
                defaults: dict = data.get("defaults")
                requirements: dict = data.get("requirements")

                # Define string parts
                part_defaults = ""
                part_requirements = ""

                if defaults is not None:
                    part_defaults = f", defaults: [{convert(defaults)}]"

                if requirements is not None:
                    part_requirements = f", requirements: [{convert(requirements)}]"

                # Generate result
                result: str = f"#[Route('{path}', name: '{name}'{part_requirements}{part_defaults}, methods: {methods})]"
                click.echo(result.replace("'", '"'))


def parse_yaml(source) -> dict:
    with open(source, "r") as file:
        return yaml.safe_load(file)


def convert(content: dict) -> str:
    result: str = ""

    for index, value in content.items():
        if type(value) is list:
            result += f"'{index}' => {value}, "
        else:
            result += f"'{index}' => '{value}', "

    return result.rstrip(", ")


if __name__ == "__main__":
    main()
