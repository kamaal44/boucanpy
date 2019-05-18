from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from bountydns.core import logger
from bountydns.broadcast import make_redis, make_broadcast_url

from .base import Base


class Zone(Base):
    __tablename__ = "zones"
    __searchable__ = ["domain", "ip"]

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    ip = Column(String, unique=False, index=True)
    is_active = Column(Boolean(), default=True)

    dns_server_id = Column(ForeignKey("dns_servers.id"), nullable=True)
    dns_server = relationship(
        "bountydns.db.models.dns_server.DnsServer",
        foreign_keys="bountydns.db.models.zone.Zone.dns_server_id",
        back_populates="zones",
    )

    dns_requests = relationship(
        "bountydns.db.models.dns_request.DnsRequest",
        foreign_keys="bountydns.db.models.dns_request.DnsRequest.zone_id",
        back_populates="zone",
    )

    @staticmethod
    async def on_after_insert(mapper, connection, target):
        logger.warning("on_after_insert: Zone")
        # print("on_after_insert", mapper, connection, target)
        try:
            publisher = await make_redis()
            res = await publisher.publish_json(
                "channel:auth",
                {"type": "MESSAGE", "name": "ZONE_CREATED", "payload": ""},
            )
        except Exception as e:
            log.warning(f"on_after_insert error: {str(e)}")

    def __repr__(self):
        return f"<{str(self.__class__.__name__)}(id={str(self.id)},ip={str(self.ip)},domain={str(self.domain)},dns_server_id={str(self.dns_server_id)})>"
