import logging
import logging.handlers

__all__ = ["get_handler"]

class LogFormatter(logging.Formatter):

    DEFAULT_FORMAT = (
        "%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]"
        "%(end_color)s %(message)s"
    )
    DEFAULT_DATE_FORMAT = "%y%m%d %H:%M:%S"

    def __init__(
        self,
        fmt=DEFAULT_FORMAT,
        datefmt=DEFAULT_DATE_FORMAT
    ):

        logging.Formatter.__init__(self, datefmt=datefmt)
        self._fmt = fmt

        self._colors = {}
        self._normal = ""

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        record.asctime = self.formatTime(record, self.datefmt)

        if record.levelno in self._colors:
            record.color = self._colors[record.levelno]
            record.end_color = self._normal
        else:
            record.color = record.end_color = ""

        formatted = self._fmt % record.__dict__

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            lines = [formatted.rstrip()]
            lines.extend(ln for ln in record.exc_text.split("\n"))
            formatted = "\n".join(lines)
        return formatted.replace("\n", "\n    ")


def get_handler():
    handler = logging.StreamHandler()
    handler.setFormatter(LogFormatter())
    return handler