from pathlib import Path
from ppadb.device import Device
from ppadb.client import Client as AdbClient


def get_device() -> Device:
    # Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037)
    return client.devices()[0]


device = get_device()


def get_new_name(name: str) -> str:
    """
    9. Symbols and Quote - 6.001 SICP (2004) [1SwPKtAIEwA].webm

    to

    09. Symbols and Quote.webm
    """
    new_name = name.split("-")[0].strip()
    index, new_name = new_name.split(". ", 1)
    new_name = f"{int(index):02}. {new_name}"
    print("new_name:", new_name)
    return new_name


def ls(folder: Path):
    filenames = device.shell(f"cd {str(folder)}; ls").split("\n")
    filenames = map(str.strip, filenames)
    filenames = filter(lambda name: name != "", filenames)
    filenames = map(lambda name: name.replace("\\", ""), filenames)
    return filenames


if __name__ == "__main__":
    folder = Path("/sdcard/Afiles/courses/sicp-2004")

    for old_name in ls(folder):
        """
        output is like:

        new_name: 9. Symbols and Quote
        /sdcard/Afiles/courses/sicp-2004/9. Symbols and Quote - 6.001 SICP (2004) [1SwPKtAIEwA].webm
        ->
        /sdcard/Afiles/courses/sicp-2004/09. Symbols and Quote.webm
        """

        new_name = get_new_name(old_name)

        before = folder / old_name
        after = before.with_stem(new_name)

        print(before)
        print("->")
        print(after)

        device.shell(f"mv '{str(before)}' '{after}'")
