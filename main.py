from log.server_log_config import logger


def main(func_ser_cli):
    logger.info(f"Функция {func_ser_cli.__name__} вызвана из функции {main.__name__}")
    func_ser_cli("127.0.0.1", 7777)
