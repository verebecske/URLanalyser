from src.malaut import Malaut
from main import ManagerRob


class ManTestMain(ManagerRob):
    def test_malaut(self) -> None:
        malaut = Malaut({}, self.logger)
        malaut.start()

    def test_virustotal(self) -> None:
        connector = self.get_connector()
        ans = connector.send_request_to_virustotal("napszemuveg.be")
        self.logger.error(ans)

    def test_analyser(self) -> None:
        connector = self.get_connector()
        analyser = self.get_analyser(connector)
        ans = analyser.is_malware("test")
        self.logger.error(ans)

    def test_urlhaus(self) -> None:
        connector = self.get_connector()
        ans = connector.send_request_to_urlhaus("www.example.com")
        self.logger.error(ans)


if __name__ == "__main__":
    rob = ManTestMain()
    rob.test_urlhaus()
