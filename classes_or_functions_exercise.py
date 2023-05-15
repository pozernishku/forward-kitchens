from dataclasses import dataclass


@dataclass
class Laptop:
    machine_name: str = "DULL"

    def install_os(self) -> None:
        print("Installing OS")

    def format_hd(self) -> None:
        print("Formatting the hard drive")

    def create_admin_user(self, password: str) -> None:
        print(f"Creating admin user with password {password}.")

    def reset_to_factory_settings(self):
        self.format_hd()
        if self.machine_name == "DULL":
            self.install_os()
            self.create_admin_user("admin")


def reset_to_factory_settings(laptop: Laptop):
    laptop.format_hd()
    if laptop.machine_name == "DULL":
        laptop.install_os()
        laptop.create_admin_user("admin")


if __name__ == "__main__":
    ltp = Laptop()
    ltp.reset_to_factory_settings()
    reset_to_factory_settings(ltp)
    print(ltp)
