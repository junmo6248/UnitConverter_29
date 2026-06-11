from boundary.input.errors import ParseError
from application.app_factory import create_app


def main() -> None:
    app = create_app()

    try:
        raw = input(
            "Insert value for converting (ex: meter:2.5) "
            "or register (ex: 1 cubit = 0.4572 meter): "
        )
        print(app.controller.run_once(raw))
    except ParseError as exc:
        print(str(exc))


if __name__ == "__main__":
    main()
