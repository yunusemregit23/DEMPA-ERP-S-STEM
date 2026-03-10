import json
import threading
import time
import unittest
from urllib.request import urlopen

from app.main import create_server


class AppServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server(host="127.0.0.1", port=0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=1)

    def test_read_root(self) -> None:
        with urlopen(f"http://127.0.0.1:{self.port}/") as response:
            body = json.loads(response.read().decode("utf-8"))
            self.assertEqual(response.status, 200)
            self.assertEqual(body, {"message": "DEMPA ERP S STEM API is running"})

    def test_health_check(self) -> None:
        with urlopen(f"http://127.0.0.1:{self.port}/health") as response:
            body = json.loads(response.read().decode("utf-8"))
            self.assertEqual(response.status, 200)
            self.assertEqual(body, {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
